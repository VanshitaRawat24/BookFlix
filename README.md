# 📚 BOOKFLIX – Smart Library Book Recommender System

## 📖 Overview
BOOKFLIX is a **hybrid book recommendation system** that helps users discover books based on their preferences using Machine Learning and NLP techniques.

The system combines **Collaborative Filtering, Content-Based Filtering, and Association Rule Mining** to generate accurate, diverse, and personalized recommendations.

It also provides a **Netflix-style interactive interface** for an engaging user experience.

---

## 🎯 Objective
- Solve the problem of **book discovery in large libraries**
- Provide **personalized recommendations**
- Handle **cold-start problem for new users**
- Improve **diversity and accuracy** of recommendations
- Build an **interactive recommendation platform**

---

## ⚙️ System Architecture

### 🧩 3-Layer Architecture

1. **Data Layer**
   - Goodbooks-10K dataset
   - 6M ratings, 10K books, 53K users

2. **Recommendation Engine**
   - Collaborative Filtering (SVD)
   - Content-Based Filtering (TF-IDF)
   - Association Rule Mining (FP-Growth)

3. **Application Layer**
   - Streamlit-based web interface
   - Real-time recommendation updates

---

## 🧠 Approach

### 1. Data Preprocessing
- Removed duplicates & handled missing values
- Normalized ratings
- Created user-item matrix
- Generated content features (tags, authors)

### 2. Models Used

#### 🔹 Collaborative Filtering
- SVD (Matrix Factorization)
- Learns user behavior patterns

#### 🔹 Content-Based Filtering
- TF-IDF + Cosine Similarity
- Recommends similar books

#### 🔹 Association Rule Mining
- FP-Growth Algorithm
- Finds "frequently read together" books

---

## 🔥 Hybrid Recommendation System
- Uses **Reciprocal Rank Fusion (RRF)**
- Combines results from all models
- Dynamic weighting:
  - Active users → CF priority
  - New users → Content + Popularity

---

## 📊 Dataset
**Goodbooks-10K Dataset**
- 10,000 books
- 6 million ratings
- 53,000+ users
- Includes metadata, tags, wishlist data

---

## 📈 Results & Performance

### 📌 Collaborative Filtering
- Precision@10 → **0.26**
- Recall@10 → **0.155**

### 📌 Hybrid Model
- Precision@15 → **0.0051**
- Recall@15 → **0.0431**
- Catalog Coverage → **7.92%**
- Diversity Score → **1.0 (maximum)**

👉 Focus: Balanced **accuracy + discovery + diversity**

---

## 💡 Key Features
- Triple Hybrid Recommendation System
- Cold Start Solution (user onboarding)
- Explainable AI ("Why this book?")
- Wishlist & user history tracking
- Netflix-style UI (Bookflix)
- Real-time interaction updates

---

## 🛠️ Tech Stack

### 💻 Language
- Python

### ⚙️ Libraries
- Pandas, NumPy
- Scikit-learn
- Surprise (SVD)
- MLxtend (Apriori / FP-Growth)
- Matplotlib, Seaborn
- Streamlit

---

