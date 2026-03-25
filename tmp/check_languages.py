import pandas as pd
import os

data_path = r'c:\Users\Vishal\Smart-Book-Recommender-System\data\processed\books_enhanced.csv'
if not os.path.exists(data_path):
    data_path = r'c:\Users\Vishal\Smart-Book-Recommender-System\data\raw\books.csv'

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    if 'language_code' in df.columns:
        languages = df['language_code'].dropna().unique()
        print(f"Total Unique Languages: {len(languages)}")
        print("Languages found:")
        print(languages)
    else:
        print("Column 'language_code' not found in dataset.")
else:
    print("Dataset file not found.")
