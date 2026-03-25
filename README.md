# 🔮 Lumina | Hybrid Book Recommender System

A premium, AI-powered book recommendation engine built with **Python** and **Streamlit**. Lumina leverages a hybrid filtering approach to provide highly personalized book suggestions.

## 🚀 Features
- **🏠 Intuitive Home**: Trending books and highly-rated classics.
- **🔍 Deep Search**: Explore a repository of 10,000+ books with real-time filtering.
- **🔮 Neural Recommendations**: Personalized suggestions using Triple-Engine logic:
  - **Engine 1 (SVD)**: Singular Value Decomposition for Collaborative Filtering.
  - **Engine 2 (TF-IDF)**: Content-Based Filtering analyzing authors and ratings.
  - **Engine 3 (AR)**: Association Rules (Frequent Itemset Mining) to find hidden patterns.
- **📊 Interactive Analytics**: Insights into library distribution and author trends.
- **💎 Premium UI**: Modern dark theme with glassmorphism and smooth animations.

## 🛠️ Installation

1. **Clone the repository** (or navigate to the folder).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App**:
   ```bash
   streamlit run app/App.py
   ```

## 🧠 Hybrid Logic Explained
Lumina calculates a hybrid score for each book based on:
- **70% Weight**: Collaborative Filtering (What similar users liked).
- **20% Weight**: Content Similarity (Books with similar authors/stats).
- **10% Weight**: Association Rules (Books frequently bought/read together).
- **Popularity Boost**: A small bias towards culturally significant books to solve the cold-start problem.

---
*Created with ❤️ for book lovers.*
