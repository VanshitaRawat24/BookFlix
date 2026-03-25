import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
import pickle
import os

class CollaborativeFiltering:
    def __init__(self, model_path=None):
        self.reconstructed_df = None
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def load_model(self, path):
        with open(path, 'rb') as f:
            self.reconstructed_df = pickle.load(f)

    def recommend(self, user_id, user_item_matrix, top_n=20):
        """
        Logic: Find items with high predicted 'borrow probability' for this user.
        Theme: 'Users like you also borrowed...'
        """
        if self.reconstructed_df is None:
            return []
        
        if user_id not in self.reconstructed_df.index:
            return []

        # Get predicted scores
        user_preds = self.reconstructed_df.loc[user_id]
        
        # Filter out books already 'borrowed' (in user_item_matrix)
        already_borrowed = user_item_matrix.loc[user_id] > 0
        
        recommendations = user_preds[~already_borrowed] \
            .sort_values(ascending=False) \
            .head(top_n).index.tolist()
            
        return recommendations
