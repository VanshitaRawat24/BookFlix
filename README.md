
# 📚 BOOKFLIX – Smart Library Book Recommender System

# 🚀 Overview

BOOKFLIX is a hybrid book recommendation system designed to help users discover relevant books from large digital libraries. It combines multiple machine learning techniques to deliver personalized, diverse, and explainable recommendations.

The system uses a triple-hybrid approach:

Collaborative Filtering (SVD)

Content-Based Filtering (TF-IDF)

Association Rule Mining (FP-Growth)



---

# 🎯 Problem Statement

With thousands of books available, users face:

Information overload

Cold-start problem (new users)

Sparse ratings data

Generic recommendations

Lack of explainability



---

# 💡 Key Features

🔁 Hybrid Recommendation Engine (CF + CBF + ARM)

👤 Personalized Recommendations based on user behavior

🆕 Cold-Start Handling via onboarding preferences

🧠 Explainable AI (why a book is recommended)

❤️ Wishlist & User History Tracking

🎬 Netflix-style UI (Bookflix Interface)

⚡ Fast Performance using pre-trained models



---

# 🛠️ Tech Stack

Category	Tools

Language	Python
Framework	Streamlit
Data Processing	Pandas, NumPy
ML Algorithms	SVD (Surprise), TF-IDF (Scikit-learn)
Pattern Mining	MLxtend (Apriori / FP-Growth)
Visualization	Matplotlib, Seaborn
Storage	Pickle, JSON
Version Control	Git, GitHub



---

# 📊 Dataset

Goodbooks-10K Dataset

📚 10,000 books

👥 53,000+ users

⭐ ~6 million ratings




---

# ⚙️ System Architecture

1. Data Layer

Stores books, ratings, and wishlist data

Preprocessed using Pandas


2. Recommendation Engine

Collaborative Filtering (SVD) → user behavior

Content-Based Filtering → book similarity

Association Rules → frequently read together


3. Application Layer

Streamlit-based interactive UI

Real-time recommendations



---

# 🧠 Methodology

1. Data Cleaning & Preprocessing


2. Model Training (SVD, TF-IDF, FP-Growth)


3. Hybrid Recommendation using Rank Fusion


4. UI Development (Streamlit)


5. Testing & Evaluation




---

# 📈 Results

🔹 Collaborative Filtering

Precision@10: 0.26

Recall@10: 0.155


🔹 Hybrid Model

Precision@15: 0.0051

Recall@15: 0.0431

Diversity Score: 1.0

Catalog Coverage: 7.92%


👉 Hybrid model improves diversity & discovery, not just accuracy.


---

# 🏆 Achievements

Built a triple-hybrid recommendation system

Solved cold-start problem for new users

Achieved high diversity in recommendations

Developed interactive Bookflix UI



---

# ⚠️ Challenges Solved

Data sparsity

Cold-start problem

Lack of trust (added explainability)

Over-reliance on popular books



---

# 🔮 Future Scope

Deep Learning models (NCF, BERT)

Real-time recommendation updates

API integration (Google Books)

Cloud deployment (Docker/Kubernetes)

Multilingual support



---

# 📌 How to Run

**Clone the repository**
git clone https://github.com/your-username/bookflix.git

**Navigate to project folder**
cd bookflix

**Install dependencies**
pip install -r requirements.txt

**Run the app**
streamlit run app.py


---

# 📚 References

Hybrid Recommender Systems – Burke (2002)

Collaborative Filtering – Koren et al.

Association Rule Mining – Agrawal & Srikant

Content-Based Filtering – Pazzani & Billsus



---

# 🙌 Author

Tamanna Arora , Vanshita Rawat
Data Science | Machine Learning Enthusiast



