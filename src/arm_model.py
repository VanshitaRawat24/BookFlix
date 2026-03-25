import pandas as pd
import pickle
import os

class AssociationRules:
    def __init__(self, model_path=None):
        self.rules = None
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def load_model(self, path):
        with open(path, 'rb') as f:
            self.rules = pickle.load(f)

    def recommend(self, user_borrow_history, top_n=20):
        """
        Logic: Use Apriori/FP-Growth rules to find frequent co-occurring borrows.
        Theme: 'Books co-borrowed with your history'
        """
        if self.rules is None or not user_borrow_history:
            return []

        # Filter rules where antecedents are in the user's borrow history
        # We need to handle frozensets
        filtered_rules = self.rules[
            self.rules['antecedents'].apply(
                lambda x: any(item in x for item in user_borrow_history)
            )
        ]

        if filtered_rules.empty:
            return []

        # Score them (Lift * Confidence is a good metric)
        filtered_rules = filtered_rules.copy()
        filtered_rules['score'] = filtered_rules['confidence'] * filtered_rules['lift']
        filtered_rules = filtered_rules.sort_values('score', ascending=False)

        recommendations = []
        for cons in filtered_rules['consequents']:
            recommendations.extend(list(cons))

        # Remove duplicates and items already borrowed
        recommendations = list(dict.fromkeys(recommendations))
        final_recs = [item for item in recommendations if item not in user_borrow_history]

        return final_recs[:top_n]
