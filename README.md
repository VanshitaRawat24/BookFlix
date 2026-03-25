# 📚 BOOKFLIX – Smart Library Book Recommender System

## 🚀 Overview
BOOKFLIX is a **hybrid book recommendation system** designed to help users discover relevant books from large digital libraries using Machine Learning and NLP techniques.

The system combines multiple algorithms to deliver **personalized, diverse, and explainable recommendations** through an interactive Netflix-style interface.

---

## 🎯 Problem Statement
Modern digital libraries face several challenges:
- Information overload due to thousands of books  
- Cold-start problem for new users  
- Sparse user ratings  
- Generic recommendations  
- Lack of explainability  

---

## 💡 Key Features
- 🔁 **Triple Hybrid Recommendation Engine** (CF + CBF + ARM)  
- 👤 Personalized recommendations based on user behavior  
- 🆕 Cold-start handling using onboarding preferences  
- 🧠 Explainable AI ("Why this book?")  
- ❤️ Wishlist & user history tracking  
- 🎬 Netflix-style UI (Bookflix interface)  
- ⚡ Fast performance using pre-trained models  

---

## 🛠️ Tech Stack

| Category | Tools |
|--------|------|
| Language | Python |
| Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| ML Algorithms | SVD (Surprise), TF-IDF (Scikit-learn) |
| Pattern Mining | MLxtend (Apriori / FP-Growth) |
| Visualization | Matplotlib, Seaborn |
| Storage | Pickle, JSON |
| Version Control | Git, GitHub |

---

## 📊 Dataset

This project uses the **Goodbooks-10K dataset**:

- 📚 10,000 books  
- 👥 53,000+ users  
- ⭐ ~6 million ratings  

🔗 Dataset Source: https://www.kaggle.com/datasets/alexanderfrosati/goodbooks-10k-updated  

---

## ⚙️ System Architecture

### 1️⃣ Data Layer
- Stores books, ratings, and wishlist data  
- Preprocessed using Pandas  

### 2️⃣ Recommendation Engine
- **Collaborative Filtering (SVD)** → learns user behavior  
- **Content-Based Filtering (TF-IDF)** → finds similar books  
- **Association Rule Mining (FP-Growth)** → identifies co-reading patterns  

### 3️⃣ Application Layer
- Streamlit-based interactive UI  
- Real-time recommendation updates  

---

## 🧠 Methodology
1. Data Cleaning & Preprocessing  
2. Model Training (SVD, TF-IDF, FP-Growth)  
3. Hybrid Recommendation using Rank Fusion  
4. UI Development using Streamlit  
5. Testing & Evaluation  

---

## 📈 Results

### 🔹 Collaborative Filtering
- Precision@10 → **0.26**  
- Recall@10 → **0.155**  

### 🔹 Hybrid Model
- Precision@15 → **0.0051**  
- Recall@15 → **0.0431**  
- Diversity Score → **1.0**  
- Catalog Coverage → **7.92%**  

👉 Focus: **Better discovery + diversity**, not just accuracy.

---

## 🏆 Achievements
- Built a **triple-hybrid recommendation system**  
- Solved the **cold-start problem**  
- Achieved **high diversity in recommendations**  
- Developed an interactive **Bookflix UI**  

---

## ⚠️ Challenges Solved
- Data sparsity  
- Cold-start problem  
- Lack of explainability  
- Over-reliance on popular books  

---

## 🔮 Future Scope
- Deep Learning models (NCF, BERT)  
- Real-time recommendation updates  
- API integration (Google Books)  
- Cloud deployment (Docker/Kubernetes)  
- Multilingual support  

---

## 📌 How to Run

```bash
# Clone the repository
git clone https://github.com/VanshitaRawat24/bookflix.git

# Navigate to project folder
cd bookflix

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
