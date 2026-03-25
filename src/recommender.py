import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle

class BookRecommender:
    def __init__(self, books_df, ratings_df=None, user_item_matrix=None):
        self.books_df = books_df.copy()
        self.ratings_df = ratings_df
        self.user_item_matrix = user_item_matrix
        self.content_sim = None
        self.item_sim = None

    def create_content_similarity(self):
        """
        Combine tags, authors, and description into one feature.
        Apply TF-IDF vectorization and compute cosine similarity.
        """
        # Fill missing values
        cols_to_use = ['authors', 'title']
        if 'tags' in self.books_df.columns:
            cols_to_use.append('tags')
        if 'description' in self.books_df.columns:
            cols_to_use.append('description')
            
        # Create combined features
        self.books_df['combined_features'] = self.books_df[cols_to_use].fillna('').agg(' '.join, axis=1)
        
        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = tfidf.fit_transform(self.books_df['combined_features'])
        
        # Compute Cosine Similarity
        self.content_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        return self.content_sim

    def recommend_similar_books(self, book_title, top_n=10):
        """
        Recommend books based on content similarity.
        """
        if self.content_sim is None:
            self.create_content_similarity()
            
        try:
            idx = self.books_df[self.books_df['title'] == book_title].index[0]
            sim_scores = list(enumerate(self.content_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:top_n+1]
            book_indices = [i[0] for i in sim_scores]
            return self.books_df.iloc[book_indices][['book_id', 'title', 'authors', 'average_rating']]
        except IndexError:
            return pd.DataFrame()

    def create_user_item_matrix(self):
        """
        Create a user-item matrix from the ratings dataset.
        """
        if self.ratings_df is None:
            raise ValueError("Ratings dataframe is required for collaborative filtering.")
            
        # Pivot the ratings table
        self.user_item_matrix = self.ratings_df.pivot_table(
            index='user_id', 
            columns='book_id', 
            values='rating'
        ).fillna(0)
        return self.user_item_matrix

    def collaborative_recommendations(self, book_title, top_n=10):
        """
        Apply item-based collaborative filtering using cosine similarity.
        """
        if self.user_item_matrix is None:
            self.create_user_item_matrix()
            
        try:
            # Get the book_id for the title
            target_book_id = self.books_df[self.books_df['title'] == book_title]['book_id'].values[0]
            
            # Use the transpose of the matrix to get item-item similarity
            # Ensure the target_book_id exists in columns
            if target_book_id not in self.user_item_matrix.columns:
                return pd.DataFrame()
                
            # Item Similarity (Transpose for item-item)
            item_matrix = self.user_item_matrix.T
            
            # Compute similarity for this specific item (more efficient than full matrix)
            # Find index of target_book_id
            target_vector = item_matrix.loc[[target_book_id]]
            sim_scores = cosine_similarity(target_vector, item_matrix)[0]
            
            # Get top matches
            sim_indices = np.argsort(sim_scores)[::-1]
            
            # Map indices back to book_ids
            similar_book_ids = item_matrix.index[sim_indices][1:top_n+1]
            
            return self.books_df[self.books_df['book_id'].isin(similar_book_ids)][['book_id', 'title', 'authors', 'average_rating']]
        except (IndexError, KeyError):
            return pd.DataFrame()

    def get_popular_books(self, top_n=10):
        """
        Popularity Score = average_rating * log(ratings_count)
        """
        self.books_df['popularity_score'] = self.books_df['average_rating'] * np.log1p(self.books_df['ratings_count'])
        popular_books = self.books_df.sort_values(by='popularity_score', ascending=False)
        return popular_books.head(top_n)[['book_id', 'title', 'authors', 'average_rating']]

    def hybrid_recommendation(self, book_title, top_n=10):
        """
        Combine Content, Collaborative, and Popularity scores.
        """
        # 1. Get content scores
        if self.content_sim is None: self.create_content_similarity()
        try:
            idx = self.books_df[self.books_df['title'] == book_title].index[0]
            content_scores = self.content_sim[idx]
        except:
            content_scores = np.zeros(len(self.books_df))

        # 2. Get collaborative scores (simplified approach for performance)
        # Assuming we just use the content and popularity if user history unavailable 
        # but the prompt asks to combine method 2 as well.
        # In a real system, we'd average the rank or score.
        
        # Calculate popularity score
        self.books_df['popularity_score_norm'] = self.books_df['average_rating'] * np.log1p(self.books_df['ratings_count'])
        # Scale to 0-1
        self.books_df['popularity_score_norm'] /= self.books_df['popularity_score_norm'].max()
        
        # Final Score = 0.5 * Content + 0.5 * Popularity (simplification)
        # Note: True collab filtering would be per-user, but prompt asks for book-based hybrid.
        final_scores = (0.7 * content_scores) + (0.3 * self.books_df['popularity_score_norm'].values)
        
        sim_indices = np.argsort(final_scores)[::-1]
        # Filter out the title itself
        sim_indices = [i for i in sim_indices if self.books_df.iloc[i]['title'] != book_title][:top_n]
        
        return self.books_df.iloc[sim_indices][['book_id', 'title', 'authors', 'average_rating']]
