import pandas as pd
df = pd.read_csv('data/processed/books_enhanced.csv')
min_y = df['original_publication_year'].min()
max_y = df['original_publication_year'].max()
print(f'Minimum Year: {min_y}')
print(f'Maximum Year: {max_y}')
print(f'Total Books: {len(df)}')
