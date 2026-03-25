from .cf_model import CollaborativeFiltering
from .arm_model import AssociationRules
import pandas as pd

class HybridLibraryRecommender:
    def __init__(self, cf_path, arm_path, books_df, user_item_matrix):
        self.cf = CollaborativeFiltering(cf_path)
        self.arm = AssociationRules(arm_path)
        self.books_df = books_df
        self.user_item_matrix = user_item_matrix
        
        # Pre-calculate popular items for cold start
        self.popular_books = books_df.sort_values('ratings_count', ascending=False)

    def get_user_history(self, user_id):
        if user_id not in self.user_item_matrix.index:
            return []
        user_row = self.user_item_matrix.loc[user_id]
        return user_row[user_row > 0].index.tolist()

    def recommend(self, user_id, top_n=10, cf_weight=0.7, arm_weight=0.3, filters=None):
        """
        The Advanced Hybrid Logic with Dynamic Filters
        """
        history = self.get_user_history(user_id)
        
        # Candidate generation
        cf_recs = self.cf.recommend(user_id, self.user_item_matrix, top_n=100)
        arm_recs = self.arm.recommend(history, top_n=100)

        # Scorer
        scores = {}
        for i, book_id in enumerate(cf_recs):
            scores[book_id] = scores.get(book_id, 0) + cf_weight * (1 / (i + 1))
        for i, book_id in enumerate(arm_recs):
            scores[book_id] = scores.get(book_id, 0) + arm_weight * (1 / (i + 1))

        # Sort all
        sorted_recs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        final_ids = [item[0] for item in sorted_recs if item[0] not in history]
        
        is_cold = False
        # If no recs or cold start, use popular
        if not final_ids:
            final_ids = self.popular_books['book_id'].tolist()
            is_cold = True

        # Apply Filters (Language, Author, etc.)
        res_df = self.books_df[self.books_df['book_id'].isin(final_ids)]
        
        # Order by score/popularity
        if not is_cold:
            res_df = res_df.set_index('book_id').reindex(final_ids).reset_index()
        
        if filters:
            if filters.get('language') and filters['language'] != 'All':
                res_df = res_df[res_df['language_code'] == filters['language']]
            if filters.get('author') and filters['author']:
                res_df = res_df[res_df['authors'].str.contains(filters['author'], case=False, na=False)]
                
        return res_df.head(top_n)['book_id'].tolist(), is_cold

