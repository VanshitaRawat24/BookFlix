import pandas as pd
import json

def process_tags():
    # Load tags mapping
    tags = pd.read_csv('data/raw/tags.csv')
    book_tags = pd.read_csv('data/raw/book_tags.csv')
    books = pd.read_csv('data/processed/books_enhanced.csv')
    
    # Filter for useful tags (simple heuristic: more than 2 chars, no numbers only)
    tags = tags[tags['tag_name'].str.len() > 2]
    tags = tags[~tags['tag_name'].str.isdigit()]
    
    # List of junk patterns to exclude
    junk = ['to-read', 'favorites', 'owned', 'currently-reading', 'books-i-own', 'read-in-', 'default', 'finished']
    for pattern in junk:
        tags = tags[~tags['tag_name'].str.contains(pattern)]

    # Join book_tags with tags
    merged = book_tags.merge(tags, on='tag_id')
    
    # Map goodreads_book_id to book_id
    id_map = books.set_index('goodreads_book_id')['book_id'].to_dict()
    merged['book_id'] = merged['goodreads_book_id'].map(id_map)
    merged = merged.dropna(subset=['book_id'])
    merged['book_id'] = merged['book_id'].astype(int)
    
    # Get top 5 tags per book
    top_tags = merged.sort_values(['book_id', 'count'], ascending=[True, False]).groupby('book_id').head(5)
    
    res = top_tags.groupby('book_id')['tag_name'].apply(list).to_dict()
    
    with open('data/processed/book_top_tags.json', 'w') as f:
        json.dump(res, f)

if __name__ == "__main__":
    process_tags()
