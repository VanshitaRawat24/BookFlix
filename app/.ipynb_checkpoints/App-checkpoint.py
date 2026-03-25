import streamlit as st
import pandas as pd
import pickle
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Smart Hybrid Book Recommender",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# BASE PATH FIX
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed")
MODEL_PATH = os.path.join(BASE_DIR, "models")

# -----------------------------
# LOAD DATA (CACHED)
# -----------------------------

@st.cache_data
def load_data():

    books = pd.read_csv(os.path.join(DATA_PATH, "books_enhanced.csv"))

    user_item_matrix = pickle.load(
        open(os.path.join(DATA_PATH, "user_item_matrix.pkl"), "rb")
    )

    similarity_matrix = pickle.load(
        open(os.path.join(MODEL_PATH, "similarity_matrix.pkl"), "rb")
    )

    reconstructed_df = pickle.load(
        open(os.path.join(MODEL_PATH, "svd_model.pkl"), "rb")
    )

    strong_rules = pickle.load(
        open(os.path.join(MODEL_PATH, "association_rules_model.pkl"), "rb")
    )

    return books, user_item_matrix, similarity_matrix, reconstructed_df, strong_rules


books, user_item_matrix, similarity_matrix, reconstructed_df, strong_rules = load_data()

popularity_score = books.set_index("book_id")["ratings_count"]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def recommend_books_svd(user_id, top_n=20):

    if user_id not in reconstructed_df.index:
        return []

    user_ratings = reconstructed_df.loc[user_id]

    already_rated = user_item_matrix.loc[user_id] > 0

    recs = user_ratings[~already_rated] \
        .sort_values(ascending=False) \
        .head(top_n).index.tolist()

    return recs


def recommend_books_content(book_id, top_n=20):

    if book_id not in similarity_matrix.columns:
        return []

    scores = similarity_matrix[book_id].sort_values(ascending=False)

    return scores.iloc[1:top_n+1].index.tolist()


def recommend_for_user(user_books, rules, top_n=20):

    filtered = rules[
        rules['antecedents'].apply(
            lambda x: any(book in x for book in user_books)
        )
    ]

    if filtered.empty:
        return []

    filtered = filtered.copy()

    filtered['score'] = (
        0.4 * filtered['confidence'] +
        0.6 * filtered['lift']
    )

    filtered = filtered.sort_values('score', ascending=False)

    recs = []

    for cons in filtered['consequents']:
        recs.extend(list(cons))

    recs = list(set(recs) - set(user_books))

    return recs[:top_n]


# -----------------------------
# HYBRID MODEL
# -----------------------------

def hybrid_recommend(user_id=None, book_id=None, top_n=5):

    if user_id is None or user_id not in user_item_matrix.index:

        return books.sort_values(
            "average_rating",
            ascending=False
        ).head(top_n)["book_id"].tolist()

    scores = {}

    CF_WEIGHT = 0.7
    CB_WEIGHT = 0.2
    AR_WEIGHT = 0.1

    # Collaborative filtering
    cf = recommend_books_svd(user_id, 20)

    for i, book in enumerate(cf):
        scores[book] = scores.get(book,0) + CF_WEIGHT*(1/(i+1))

    # Content based
    if book_id is not None:

        cb = recommend_books_content(book_id,20)

        for i,book in enumerate(cb):
            scores[book] = scores.get(book,0) + CB_WEIGHT*(1/(i+1))

    # Association rules
    user_books = user_item_matrix.loc[user_id]
    user_books = user_books[user_books>0].index.tolist()

    ar = recommend_for_user(user_books,strong_rules,20)

    for i,book in enumerate(ar):
        scores[book] = scores.get(book,0) + AR_WEIGHT*(1/(i+1))

    if not scores:
        return []

    # popularity boost
    for book in scores:
        scores[book] += 0.05 * popularity_score.get(book,0)

    sorted_books = sorted(scores.items(), key=lambda x:x[1], reverse=True)

    rec = []

    for book,_ in sorted_books:
        if book not in rec and book not in user_books:
            rec.append(book)

        if len(rec)>=top_n:
            break

    return rec


# -----------------------------
# UI HEADER
# -----------------------------

st.title("📚 Smart Hybrid Book Recommender System")
st.write("AI-powered recommendations using Hybrid Filtering")

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Settings")

user_id = st.sidebar.number_input(
    "Enter User ID",
    min_value=1,
    step=1
)

book_title = st.sidebar.selectbox(
    "Select a Book (optional)",
    books["title"].sort_values().unique()
)

book_id = books[books["title"]==book_title]["book_id"].values[0]

top_n = st.sidebar.slider(
    "Number of recommendations",
    5,
    20,
    10
)

# -----------------------------
# RECOMMEND BUTTON
# -----------------------------

if st.button("🔍 Get Recommendations"):

    rec_ids = hybrid_recommend(user_id, book_id, top_n)

    results = books[books["book_id"].isin(rec_ids)][
        ["title","authors","average_rating"]
    ]

    st.subheader("Recommended Books")

    cols = st.columns(2)

    for i,(idx,row) in enumerate(results.iterrows()):

        with cols[i%2]:

            st.markdown(f"""
            ### 📖 {row['title']}

            **Author:** {row['authors']}  
            ⭐ **Rating:** {row['average_rating']}
            """)