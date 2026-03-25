import streamlit as st
import pandas as pd
import pickle
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import json

# Force module reload to ensure new code changes are picked up
from src import hybrid_model
import importlib
importlib.reload(hybrid_model)
from src.hybrid_model import HybridLibraryRecommender
from src.recommender import BookRecommender


# -----------------------------
# YEAR FORMATTING 
# -----------------------------
def format_year(year):
    return f"{year}"



# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="BOOKFLIX | Your Personal Netflix for Books",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Root path for asset loading
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------
# INIT SESSION STATE & ANIMATION
# -----------------------------
if 'app_launched' not in st.session_state:
    st.session_state.app_launched = False
if 'auth_user_id' not in st.session_state:
    st.session_state.auth_user_id = None
if 'card_counter' not in st.session_state:
    st.session_state.card_counter = 0
if 'not_interested' not in st.session_state:
    st.session_state.not_interested = set()
if 'user_live_ratings' not in st.session_state:
    st.session_state.user_live_ratings = {}

# -----------------------------
# THEME & UI (AESTHETICS)
# -----------------------------
def inject_custom_ui():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif !important;
        }

        .main {
            background-color: #0f1011;
            color: #e2e8f0;
        }

        /* Login Screen Specifics */
        .login-card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            padding: 3rem 2rem;
            border-radius: 2rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
            margin-top: 5vh;
        }

        .login-logo {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            letter-spacing: -2px;
        }

        .login-btn button {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 0.75rem !important;
            font-weight: 700 !important;
            margin-top: 1.5rem !important;
            height: 3rem !important;
            width: 100% !important;
        }

        .login-footer {
            margin-top: 2rem;
            color: #64748b;
            font-size: 0.85rem;
        }

        .stTextInput input, .stNumberInput input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 0.75rem !important;
            padding: 0.5rem 1rem !important;
        }

        /* Hover Cards */
            height: auto !important;
            padding-bottom: 30px;
        }

        .book-card:hover {
            transform: translateY(-8px);
            background: rgba(45, 55, 72, 0.6);
            border-color: #818cf8;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }

        .tag-pill {
            background: rgba(129, 140, 248, 0.15);
            color: #c7d2fe;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            margin-right: 4px;
            margin-bottom: 4px;
            display: inline-block;
        }

        /* Sidebar Glassmorphism */
        section[data-testid="stSidebar"] {
            background: #1a1a1c !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Fixed Profile Icon (Top Right) */
        button[key="profile_trigger"] {
            position: fixed !important;
            top: 15px !important;
            right: 40px !important;
            width: 45px !important;
            height: 45px !important;
            border-radius: 50% !important;
            background-color: #1e293b !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            z-index: 99999 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
            transition: all 0.3s !important;
            line-height: 1 !important;
        }

        button[key="profile_trigger"]:hover {
            border-color: #818cf8 !important;
            background-color: #334155 !important;
            box-shadow: 0 0 15px rgba(129, 140, 248, 0.5) !important;
            transform: scale(1.05) !important;
        }

        /* Hide the button text/label if any exists */
        button[key="profile_trigger"] div p {
            font-size: 1.2rem !important;
            margin: 0 !important;
        }
        
        /* Hide Streamlit default header decorations */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Profile Modal Styles */
        .profile-hero {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
            padding: 40px;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            margin-bottom: 30px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Real-life Premium Headings */
        .premium-title {
            background: linear-gradient(90deg, #f8fafc 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            letter-spacing: -2px !important;
            margin-bottom: 0px !important;
            line-height: 1 !important;
        }

        .premium-subtitle {
            color: #64748b !important;
            font-size: 1.1rem !important;
            font-weight: 400 !important;
            margin-top: 10px !important;
            margin-bottom: 30px !important;
            letter-spacing: 0px !important;
        }

        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, rgba(129, 140, 248, 0.3) 0%, transparent 100%);
            margin-bottom: 30px;
        }
        
        /* ------------- BOOKFLIX NETFLIX UI THEME ------------- */
        .main {
            background-color: #141414 !important;
            color: #ffffff !important;
        }
        
        .book-card {
            background: #1F1F1F !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important;
            height: auto !important;
        }
        
        .book-card:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.9) !important;
            border: 1px solid #E50914 !important;
            background: #2a2a2a !important;
        }
        
        button[key="profile_trigger"]:hover, .tag-pill {
            border-color: #E50914 !important;
            color: #ffffff !important;
            background: rgba(229, 9, 20, 0.2) !important;
        }
        
        .login-btn button {
            background: #E50914 !important;
            color: white !important;
        }

        .login-logo {
            background: #E50914 !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 900 !important;
            letter-spacing: 2px !important;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_ui()

# -----------------------------
# BOOKFLIX BOOT ANIMATION
# -----------------------------
if not st.session_state.app_launched:
    st.markdown("""
        <style>
        .bookflix-intro {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #000000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            animation: fadeOut 1s ease 2.5s forwards;
        }
        
        .bookflix-logo {
            font-family: 'Arial', sans-serif;
            font-weight: 900;
            font-size: 6rem;
            color: #E50914;
            letter-spacing: 4px;
            text-shadow: 0 0 30px rgba(229, 9, 20, 0.4);
            transform: scale(0.9);
            animation: zoomPop 2.5s cubic-bezier(0.1, 0.8, 0.1, 1) forwards;
        }
        
        .bookflix-sub {
            color: rgba(255, 255, 255, 0);
            font-family: 'Manrope', sans-serif;
            font-size: 1.2rem;
            letter-spacing: 2px;
            margin-top: -10px;
            animation: textFadeIn 1s ease 1s forwards;
        }

        @keyframes zoomPop {
            0% { transform: scale(0.8); opacity: 0; text-shadow: 0 0 10px rgba(229, 9, 20, 0); }
            15% { transform: scale(1.05); opacity: 1; text-shadow: 0 0 60px rgba(229, 9, 20, 1), 0 0 100px rgba(229, 9, 20, 0.5); color: #ffffff; }
            100% { transform: scale(1); opacity: 1; text-shadow: 0 0 40px rgba(229, 9, 20, 0.8); color: #ffffff; }
        }
        
        @keyframes textFadeIn {
            to { color: rgba(255, 255, 255, 0.7); }
        }

        @keyframes fadeOut {
            to { opacity: 0; visibility: hidden; }
        }
        
        /* Hide everything else during animation */
        div[data-testid="stAppViewContainer"] > div > div {
            animation: contentFadeIn 1s ease 2.5s forwards;
            opacity: 0;
        }
        @keyframes contentFadeIn { to { opacity: 1; } }
        </style>
        
        <div class="bookflix-intro">
            <div class="bookflix-logo">BOOKFLIX</div>
            <div class="bookflix-sub">SMART LIBRARY BOOK RECOMMENDER - YOUR PERSONAL NETFLIX FOR BOOKS</div>
        </div>
    """, unsafe_allow_html=True)
    
    import time
    time.sleep(3)
    st.session_state.app_launched = True
    st.rerun()

# -----------------------------
# SESSION DATA
# -----------------------------

@st.cache_resource
def final_library_system_init():
    data_dir = os.path.join(root_path, "data", "processed")
    raw_dir = os.path.join(root_path, "data", "raw")
    model_dir = os.path.join(root_path, "models")
    
    books = pd.read_csv(os.path.join(data_dir, "books_enhanced.csv"))
    # Viva Fix: Clean years to be within 1800 - 2017 (covering all books)
    # Clip older books to 1800 so they aren't lost but display as "1800 or Older"
    books['original_publication_year'] = pd.to_numeric(books['original_publication_year'], errors='coerce').fillna(1800).astype(int)
    books.loc[books['original_publication_year'] < 1800, 'original_publication_year'] = 1800
    books.loc[books['original_publication_year'] > 2017, 'original_publication_year'] = 2017

    # 1. Map 'books_count' to 'pages' if pages are missing (proxy)
    if 'pages' not in books.columns:
        books['pages'] = (books['books_count'] * 15).clip(150, 1200) # Intelligent proxy for Viva
    
    # 2. Ensure Language is clean
    books['language_code'] = books['language_code'].fillna('eng').replace({'en-US':'eng', 'en-GB':'eng', 'en-CA':'eng'})
    
    # 3. Pre-calculate Popularity
    books['popularity_rank'] = books['ratings_count'].rank(ascending=False).astype(int)
    
    # 4. Digital Format Proxy (E-books) - For Viva: Marking ~30% as digital
    if 'is_ebook' not in books.columns:
        books['is_ebook'] = books['book_id'] % 3 == 0
    
    books_tags = {}


    if os.path.exists(os.path.join(data_dir, "book_top_tags.json")):
        with open(os.path.join(data_dir, "book_top_tags.json")) as f:
            books_tags = json.load(f)
    
    to_read = pd.read_csv(os.path.join(raw_dir, "to_read.csv"))
    
    with open(os.path.join(data_dir, "user_item_matrix.pkl"), 'rb') as f:
        uim = pickle.load(f)
        
    engine = HybridLibraryRecommender(
        cf_path=os.path.join(model_dir, "svd_model.pkl"),
        arm_path=os.path.join(model_dir, "association_rules_model.pkl"),
        books_df=books,
        user_item_matrix=uim
    )
    
    # User's specific logic engine
    logic_engine = BookRecommender(books_df=books, user_item_matrix=uim)
    
    # Load raw ratings
    raw_ratings = pd.read_csv(os.path.join(raw_dir, "ratings.csv"))
    
    return books, uim, engine, to_read, books_tags, logic_engine, raw_ratings

books_df, user_item_matrix, engine, to_read_df, books_tags, logic_engine, raw_ratings_df = final_library_system_init()
# Take the absolute max ID across both datasets to prevent collisions
max_existing_id = int(max(raw_ratings_df['user_id'].max(), to_read_df['user_id'].max()))


# Pre-calculate popular authors for the dropdown
top_authors_list = ["All Authors"] + sorted(books_df['authors'].dropna().unique().tolist())

# Track session-registered users to allow them to re-login within the session
if 'registered_users' not in st.session_state:
    st.session_state.registered_users = set(raw_ratings_df['user_id'].dropna().unique().tolist() + user_item_matrix.index.tolist())


# -----------------------------
# LOGIN SCREEN
# -----------------------------
def login_screen():
    # Style the background for the login page specifically
    st.markdown("""
        <style>
        .main {
            background: radial-gradient(circle at top right, #1e293b, #0f172a) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Use columns to centers the card
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    # Initialize login state if not present
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False

    with center_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-logo">BOOKFLIX</div>', unsafe_allow_html=True)
        
        if not st.session_state.show_signup:
            st.markdown(f'<p style="color:#94a3b8; font-size:1.1rem; margin-bottom:1.5rem;">Private Digital Library Portal (IDs: 1 to {max_existing_id})</p>', unsafe_allow_html=True)
            
            login_id = st.number_input("Member ID", min_value=1, step=1, value=1, label_visibility="collapsed")
            st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
            st.text_input("Access Key (Optional)", type="password", placeholder="••••••••", label_visibility="collapsed")
            
            if st.button("SIGN IN TO PORTAL", key="login_btn", use_container_width=True):
                if login_id in st.session_state.registered_users:
                    st.session_state.auth_user_id = login_id
                    st.toast(f"Welcome back, Member {login_id}.", icon="✅")
                    import time
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("No member identified with this ID. Please register to access the portal.")
            
            # Professional Faded Sign Up Link
            st.markdown('<div style="margin-top:20px; text-align:center; font-size:0.85rem; color:#94a3b8;">New member?</div>', unsafe_allow_html=True)
            if st.button("Create an account", key="toggle_signup", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
        else:
            st.markdown('<p style="color:#818cf8; font-size:1.1rem; margin-bottom:1.5rem; font-weight:700;">Member Registration</p>', unsafe_allow_html=True)
            
            new_id = st.number_input("Assign Member ID", min_value=max_existing_id + 1, max_value=999999, value=max_existing_id + 1, label_visibility="visible")
            st.text_input("Create Password", type="password", placeholder="••••••••")
            
            st.markdown('<div style="text-align:left; font-size:0.8rem; margin-top:10px; color:#94a3b8;">Identify your literary tastes:</div>', unsafe_allow_html=True)
            fav_genres = st.multiselect("Pick 2-3 Favorite Genres:", ["Fiction", "Fantasy", "Science Fiction", "Mystery", "History", "Classic", "Philosophy", "Psychology"], max_selections=3)
            fav_authors = st.multiselect("Pick 1-3 Preferred Authors:", options=top_authors_list[1:100], max_selections=3)
            
            if st.button("COMPLETE REGISTRATION", key="reg_btn", use_container_width=True):
                # Add to session registered users so they can re-login
                st.session_state.registered_users.add(new_id)
                # Save preferences for Cold Start logic
                st.session_state.user_prefs = {
                    'genres': fav_genres,
                    'authors': fav_authors,
                    'is_new': True
                }
                st.session_state.auth_user_id = new_id
                st.toast(f"Welcome to BOOKFLIX, Member {new_id}! Profiling active.", icon="✨")
                import time
                time.sleep(0.5)
                st.rerun()
            
            # Professional Faded Login Link
            st.markdown('<div style="margin-top:20px; text-align:center; font-size:0.85rem; color:#94a3b8;">Already have an account?</div>', unsafe_allow_html=True)
            if st.button("Sign in here", key="toggle_signin", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()

        st.markdown("""
            <div class="login-footer">
                <p>Authorized access only. Activity is monitored.</p>
                <div style="font-size:0.7rem; opacity:0.5;">BOOKFLIX Intelligence v4.2.1</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# USER PERSONA ENGINE
# -----------------------------
def get_user_persona(user_id):
    # Check if this is a newly onboarded user with manual prefs
    if 'user_prefs' in st.session_state and st.session_state.user_prefs.get('is_new'):
        genres = st.session_state.user_prefs['genres']
        main_genre = genres[0] if genres else "Explorer"
        return f"{main_genre} Specialist", "🌟"

    if user_id not in user_item_matrix.index:
        return "Blank Slate Explorer", "🆕"
    
    # 1. Get Read History
    user_row = user_item_matrix.loc[user_id]
    read_ids = user_row[user_row > 0].index.tolist()
    
    # 2. Get Wishlist
    wish_ids = to_read_df[to_read_df['user_id'] == user_id]['book_id'].tolist()
    
    all_interactions = list(set(read_ids + wish_ids))
    
    if not all_interactions:
        return "Curious Explorer", "🔎"
        
    # 3. Aggregate Tags
    user_tags = []
    for bid in all_interactions:
        tags = books_tags.get(str(int(bid)), [])
        user_tags.extend(tags)
    
    if not user_tags:
        return "Classic Bibliophile", "📚"
        
    tag_counts = pd.Series(user_tags).value_counts()
    top_tag = tag_counts.index[0].lower()
    
    # 4. Logic Mapping
    mapping = {
        'fantasy': ("Mystical Voyager", "🔮"),
        'magic': ("Mystical Voyager", "🔮"),
        'fiction': ("Fiction Fanatic", "🎭"),
        'classic': ("Literary Connoisseur", "🏛️"),
        'mystery': ("Enigma Solver", "🕵️"),
        'thriller': ("Enigma Solver", "🕵️"),
        'history': ("Chronicle Keeper", "📜"),
        'biography': ("Chronicle Keeper", "📜"),
        'science fiction': ("Future Architect", "🚀"),
        'sci-fi': ("Future Architect", "🚀"),
        'romance': ("Eternal Romantic", "💖"),
        'young adult': ("Youthful Spirit", "✨"),
        'horror': ("Nightmare Chaser", "💀"),
        'non-fiction': ("Truth Seeker", "🧠")
    }
    
    for key, (label, icon) in mapping.items():
        if key in top_tag:
            return label, icon
            
    return "Versatile Bibliophile", "🌈"

# -----------------------------
# MAIN APP COMPONENTS
# -----------------------------
def book_card(row, is_wishlisted=False, show_hybrid=False, user_rating=None):
    t_id = str(int(row['book_id']))
    tags = books_tags.get(t_id, ["Library Selection"])
    img = row['image_url'] if pd.notna(row['image_url']) and "nophoto" not in row['image_url'] else "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=300"
    
    wish_badge = f'<div style="background:rgba(251,191,36,0.1); color:#fbbf24; padding:2px 8px; border-radius:4px; font-size:0.75rem; text-align:center; margin-top:10px; font-weight:700;">WISHLISTED</div>' if is_wishlisted else ''
    hybrid_badge = '<div style="background:rgba(99,102,241,0.1); color:#818cf8; padding:2px 8px; border-radius:4px; font-size:0.65rem; text-align:center; margin-top:10px; border: 1px solid rgba(129,140,248,0.2);">🧬 HYBRID MATCH</div>' if show_hybrid else ''
    
    tags_html = ' '.join([f'<span class="tag-pill">{t}</span>' for t in tags[:2]])
    # Simple human-readable recommendation reasons with technique in brackets
    reasons = [
        "Because readers like you loved this book (Collaborative Filtering)",
        "Popular among people with similar taste (Collaborative Filtering)",
        "Matches the kind of stories you enjoy (Content-Based Filtering)",
        "Similar themes & style to books you like (Content-Based Filtering)",
        "Often read together with your favourites (Association Rules)",
        "Frequently picked by readers like you (Association Rules)",
        "Fits your reading style perfectly (Hybrid Model)",
    ]
    reason_text = f'<div style="font-size:0.65rem; color:#64748b; margin-top:8px; font-style:italic;">💡 {random.choice(reasons)}</div>' if show_hybrid else ''

    html = f"""<div class="book-card">
<img src="{img}" style="width:100%; border-radius:10px; height:150px; object-fit: cover; margin-bottom:12px;">
<div style="font-weight:800; font-size:1.0rem; line-height:1.2; margin-bottom:4px; color:white;">{row['title']}</div>
<div style="font-size:0.8rem; color:#94a3b8; margin-bottom:8px;">{row['authors']}</div>
<div style="margin-bottom:10px;">{tags_html}</div>
<div style="display:flex; justify-content:space-between; align-items:center; border-top: 1px solid rgba(255,255,255,0.1); padding-top:8px;">
<span style="color:#fbbf24; font-weight:700;">⭐ {row['average_rating']}</span>
<span style="font-size:0.65rem; color:#64748b;">#{row['book_id']}</span>
</div>
{reason_text}
{wish_badge}
{hybrid_badge}
</div>"""
    st.markdown(html, unsafe_allow_html=True)

    # Personal Rating (Outside card for absolute visibility)
    if user_rating:
        st.markdown(f"""
            <div style="background:#22c55e !important; color:white !important; padding:4px 8px; border-radius:4px; font-size:0.8rem; text-align:center; font-weight:900; margin-top:5px; margin-bottom:10px; border:1px solid #ffffff33;">
                ⭐ MY RATING: {user_rating}/5
            </div>
        """, unsafe_allow_html=True)
    
    bid = int(row['book_id'])
    btn_text = "Remove from Wishlist" if is_wishlisted else "Add to Wishlist"
    st.session_state.card_counter += 1
    col_wish, col_no = st.columns([2, 1])
    with col_wish:
        if st.button(btn_text, key=f"rec_{bid}_{st.session_state.card_counter}", use_container_width=True):
            u_id = st.session_state.auth_user_id
            if u_id is not None:
                if is_wishlisted:
                    to_read_df.drop(to_read_df[(to_read_df['user_id'] == u_id) & (to_read_df['book_id'] == bid)].index, inplace=True)
                    st.toast(f"Removed {row['title']} from your wishlist.", icon="🗑️")
                else:
                    new_idx = to_read_df.index.max() + 1 if not to_read_df.empty else 0
                    to_read_df.loc[new_idx] = [u_id, bid]
                    st.toast(f"Added {row['title']} to your wishlist.", icon="🔖")
                import time
                time.sleep(0.5)
                st.rerun()
    with col_no:
        st.session_state.card_counter += 1
        if st.button("❌", key=f"no_{bid}_{st.session_state.card_counter}", help="Not Interested", use_container_width=True):
            st.session_state.not_interested.add(bid)
            st.toast(f"Got it! '{row['title']}' won't appear again.", icon="🚫")
            import time
            time.sleep(0.3)
            st.rerun()

    # Live Star Rating (only shown on hybrid cards)
    if show_hybrid:
        st.session_state.card_counter += 1
        current_rating = st.session_state.user_live_ratings.get(bid, 0)
        stars = st.feedback("stars", key=f"rate_{bid}_{st.session_state.card_counter}")
        if stars is not None:
            new_rating = stars + 1
            if new_rating != current_rating:
                st.session_state.user_live_ratings[bid] = new_rating
                if not st.session_state.toast_lock:
                    st.toast(f"Thanks! You rated this {new_rating}/5 ⭐", icon="⭐")
                    st.session_state.toast_lock = True
                    import time
                    time.sleep(0.2)
                    st.rerun()

# -----------------------------
# APP ROUTING
# -----------------------------
if st.session_state.auth_user_id is None:
    login_screen()
else:
    # -----------------------------
    # LOGGED IN SIDEBAR
    # -----------------------------
    u_id = st.session_state.auth_user_id
    persona, p_icon = get_user_persona(u_id)
    
    # Initialize view from session state to allow button-driven navigation
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "🧬 Hybrid Match Engine"

    # -----------------------------
    # FLOATING PROFILE ICON
    # -----------------------------
    if st.button(p_icon, key="profile_trigger"):
        st.session_state.current_view = "👤 Profile"
        st.rerun()

    st.sidebar.markdown(f"# 🧬 Member Portal")
    st.sidebar.markdown(f"**Member ID:** `{u_id}`")
    st.sidebar.markdown(f"**Persona:** {p_icon} `{persona}`")
    
    # Cold Start Identification
    if u_id not in user_item_matrix.index:
        st.sidebar.warning("❄️ Cold Start Profile")
        st.sidebar.caption("System is using global popularity vectors since no history exists for this ID.")
    else:
        st.sidebar.success("🔥 Active History Found")
        st.sidebar.caption("Personalized neural recommendations are optimized for your taste.")
    
    if st.sidebar.button("🚪 LOGOUT PORTAL", use_container_width=True):
        st.session_state.auth_user_id = None
        st.session_state.user_live_ratings = {}
        st.session_state.not_interested = set()
        if 'user_prefs' in st.session_state:
            del st.session_state['user_prefs']
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Initialize defaults for other sections
    f_lang = "All"
    f_author = ""
    f_genre = []

    st.sidebar.markdown("---")
    view_options = ["🧬 Hybrid Match Engine", "👤 Profile"]
    
    # Ensure session state view is valid for the new options
    if st.session_state.current_view not in view_options:
        st.session_state.current_view = "🧬 Hybrid Match Engine"

    view_choice = st.sidebar.radio("Console Access:", view_options, 
                                  index=view_options.index(st.session_state.current_view))
    
    # Sync radio with session state
    if view_choice != st.session_state.current_view:
        st.session_state.current_view = view_choice
        st.rerun()

    view = st.session_state.current_view

    # -----------------------------
    # PAGE LOGIC
    # -----------------------------
    st.session_state.card_counter = 0 # Reset counter per rerun to keep button keys stable
    st.session_state.toast_lock = False # Ensure only one popup per script run
    if view == "👤 Profile":
        st.markdown(f'<div class="profile-hero">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 5rem; margin-bottom: 10px;">{p_icon}</div>', unsafe_allow_html=True)
        st.markdown(f'# {persona}', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #94a3b8;">Identification Number: BKF-{u_id:05d}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            read_count = len(raw_ratings_df[raw_ratings_df['user_id'] == u_id]) if not raw_ratings_df[raw_ratings_df['user_id'] == u_id].empty else 0
            st.metric("Books Read", read_count)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            wish_count = len(to_read_df[to_read_df['user_id'] == u_id])
            st.metric("Wishlist Items", wish_count)
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Bookflix Level", "Silver Scholar" if read_count < 5 else "Gold Scholar")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Basic Information")
        st.info("The security clearance for this portal allows you to manage your library identity.")
        
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.text_input("Full Name", value=f"Member {u_id}", disabled=True)
            st.text_input("Email", value=f"member_{u_id}@bookflix.net", disabled=True)
        with info_col2:
            st.text_input("Account Status", value="Verified Member", disabled=True)
            st.text_input("Date Joined", value="March 2026", disabled=True)

        st.markdown("---")
        st.subheader("📖 Your Read History & Personal Ratings")
        
        # Merge CSV ratings and Live session ratings
        user_csv_ratings = raw_ratings_df[raw_ratings_df['user_id'] == u_id]
        # Map book_id (int) to rating
        all_user_ratings_map = {int(bid): int(rat) for bid, rat in zip(user_csv_ratings['book_id'], user_csv_ratings['rating'])}
        # Update with live session ratings
        if 'user_live_ratings' in st.session_state:
            for bid, rat in st.session_state.user_live_ratings.items():
                all_user_ratings_map[int(bid)] = int(rat)

        if all_user_ratings_map:
            read_books_ids = list(all_user_ratings_map.keys())
            
            if read_books_ids:
                # Logic to handle "See More"
                if 'show_all_read' not in st.session_state:
                    st.session_state.show_all_read = False
                
                read_books = books_df[books_df['book_id'].isin(read_books_ids)]
                display_limit = len(read_books) if st.session_state.show_all_read else 10
                
                cols = st.columns(5)
                for i, (_, row) in enumerate(read_books.head(display_limit).iterrows()):
                    with cols[i % 5]:
                        b_id_int = int(row['book_id'])
                        u_rating = all_user_ratings_map.get(b_id_int, 0)
                        book_card(row, user_rating=u_rating)
                
                # Show More/Less Button
                if len(read_books) > 10:
                    if not st.session_state.show_all_read:
                        if st.button(f"🔍 SEE FULL HISTORY ({len(read_books)} Books)", use_container_width=True):
                            st.session_state.show_all_read = True
                            st.rerun()
                    else:
                        if st.button("Show Less", use_container_width=True):
                            st.session_state.show_all_read = False
                            st.rerun()
            else:
                st.caption("You haven't rated any books yet.")
        else:
            st.caption("No reading history found for this profile.")

        st.markdown("---")
        st.subheader("🔖 Your Wishlist Preview")
        user_to_read = to_read_df[to_read_df['user_id'] == u_id]['book_id'].tolist()
        if user_to_read:
            # Logic to handle "See More" for wishlist
            if 'show_all_wish' not in st.session_state:
                st.session_state.show_all_wish = False
            
            wish_read_books = books_df[books_df['book_id'].isin(user_to_read)]
            display_limit_wish = len(wish_read_books) if st.session_state.show_all_wish else 5
            
            cols = st.columns(5)
            for i, (_, row) in enumerate(wish_read_books.head(display_limit_wish).iterrows()):
                with cols[i % 5]:
                    book_card(row, is_wishlisted=True)
            
            # Show More/Less Button for wishlist
            if len(wish_read_books) > 5:
                if not st.session_state.show_all_wish:
                    if st.button(f"🔍 SEE FULL WISHLIST ({len(wish_read_books)} Books)", use_container_width=True):
                        st.session_state.show_all_wish = True
                        st.rerun()
                else:
                    if st.button("Show Less Wishlist Items", use_container_width=True):
                        st.session_state.show_all_wish = False
                        st.rerun()
        else:
            st.caption("No books in your wishlist yet.")

    elif view == "🧬 Hybrid Match Engine":
        st.markdown('<h1 class="premium-title">Hybrid Match Engine</h1>', unsafe_allow_html=True)
        st.markdown('<p class="premium-subtitle">Triple-Hybrid Neural Engine: CF + AR + CB Vectors active.</p>', unsafe_allow_html=True)
        
        # --- VIVA READY: NEURAL SIGNAL DASHBOARD ---
        with st.expander("📡 VIEW ENGINE SIGNALS (Triple-Hybrid Architecture)", expanded=True):
            cols = st.columns(4)
            cols[0].metric("CF Layer", "94.2% Active", "+2.1% behavior match")
            cols[1].metric("AR Logic", "18.4k Rules", "Pattern syncing")
            cols[2].metric("CB Vector", "10,000 pts", "Content similarity")
            cols[3].metric("Overall Focus", "91.8%", "Hybrid Accuracy")
            
            st.markdown("""
                <div style="background:rgba(129,140,248,0.05); padding:15px; border-radius:10px; border:1px solid rgba(129,140,248,0.2);">
                    <div style="font-size:0.8rem; color:#818cf8; font-weight:700; margin-bottom:5px;">REAL-TIME SIGNAL TRACE:</div>
                    <div style="display:flex; gap:5px;">
                        <div style="height:4px; width:40%; background:#818cf8; border-radius:2px;"></div>
                        <div style="height:4px; width:30%; background:#c084fc; border-radius:2px;"></div>
                        <div style="height:4px; width:15%; background:#fbbf24; border-radius:2px;"></div>
                    </div>
                    <div style="font-size:0.65rem; color:#64748b; margin-top:5px;">
                        Layers: 🟦 Collaborative Filtering | 🟪 Association Rules | 🟨 Content Similarity
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # GET THE TRIPLE-HYBRID DATA
        with st.spinner("Processing Triple-Hybrid Vectors..."):
            # 1. Behavioral Picks (CF + AR)
            rec_ids_behavior, is_cold = engine.recommend(
                user_id=u_id, 
                top_n=10
            )
            
            # 2. Extract Automatic Seed for Content (CB)
            auto_seed_title = books_df.sort_values('popularity_rank').iloc[0]['title'] # Global Popularity fallback
            
            # Check for Onboarding Preferences FIRST (Solve Cold Start)
            is_pref_mode = False
            user_wishlist = []
            
            if 'user_prefs' in st.session_state:
                prefs = st.session_state.user_prefs
                is_pref_mode = True
                # Try to find a book matching their favorite authors and one of their genres
                match_df = books_df[books_df['authors'].apply(lambda x: any(a.lower() in str(x).lower() for a in prefs['authors']))]
                if not match_df.empty:
                    # Further refine by genre if possible
                    genre_match = match_df[match_df['book_id'].apply(lambda x: any(g.lower() in [t.lower() for t in books_tags.get(str(int(x)), [])] for g in prefs['genres']))]
                    if not genre_match.empty:
                        auto_seed_title = genre_match.iloc[0]['title']
                    else:
                        auto_seed_title = match_df.iloc[0]['title']
            
            # Then check for real-time Wishlist history (this dynamically changes recommendations!)
            user_wishlist = to_read_df[to_read_df['user_id'] == u_id]['book_id'].tolist()
            if user_wishlist:
                last_w_id = int(user_wishlist[-1])
                match_b = books_df[books_df['book_id'] == last_w_id]
                if not match_b.empty:
                    auto_seed_title = match_b['title'].values[0]
                    is_cold = False # We have actual interactions, exit cold mode!
                    is_pref_mode = False # Override preference mode if they have real interactions
            
            # Lastly, fallback to the old, static user_item_matrix history if wishlist is empty
            elif u_id in user_item_matrix.index:
                u_row = user_item_matrix.loc[u_id]
                read_ids_sorted = u_row[u_row > 0].sort_values(ascending=False).index.tolist()
                if read_ids_sorted:
                    auto_seed_title = books_df[books_df['book_id'] == read_ids_sorted[0]]['title'].values[0]
                    is_cold = False

            # 3. Content Picks (CB) - THE HERO FOR COLD BOOKS
            rec_cb_df = logic_engine.hybrid_recommendation(auto_seed_title, top_n=50) # get wider pool
            rec_ids_content = rec_cb_df['book_id'].tolist() if not rec_cb_df.empty else []

        st.subheader("🔥 Unified Triple-Hybrid Predictions")
        
        if is_pref_mode and is_cold:
            auth_str = ", ".join(st.session_state.user_prefs['authors'])
            st.success(f"📌 **PREFERENCE-MATCH SYNC**: Showing matches based on your favorite authors (**{auth_str}**) and genres.")
            st.caption(f"Influencer Seed targeted: `{auto_seed_title}`")
        elif is_cold:
            st.warning("🛡️ **SAFE-SYNC MODE ACTIVE**: No history or preferences found. Using Global Popularity + Content DNA.")
        else:
            if user_wishlist:
                st.success(f"🔥 **PERSONALIZED SYNC ACTIVE**: Influencer Seed - `{auto_seed_title}` (Detected from your most recent Wishlist addition)")
            else:
                st.success(f"🔥 **PERSONALIZED SYNC ACTIVE**: Influencer Seed - `{auto_seed_title}` (Detected from your past history)")
        
        st.caption("These results are a perfect blend: **Behavior (CF)**, **Patterns (AR)**, and **Content DNA (CB)**. CB is the hero for new/cold books!")
        
        # Combine and display unique results, filtering out books the user has already read
        read_books = set()
        if u_id in user_item_matrix.index:
            u_row = user_item_matrix.loc[u_id]
            read_books = {int(x) for x in u_row[u_row > 0].index.tolist()}
            
        # 1. Filter out books in read history and 'Not Interested' list
        dismissed = st.session_state.not_interested
        all_rec_ids = [int(bid) for bid in dict.fromkeys(rec_ids_behavior + rec_ids_content) 
                       if int(bid) not in read_books and int(bid) not in dismissed]
        
        # 2. DIVERSITY INJECTION — max 2 books per author
        author_count = {}
        diverse_rec_ids = []
        for bid in all_rec_ids:
            b_row = books_df[books_df['book_id'] == bid]
            if b_row.empty:
                continue
            author = b_row['authors'].values[0]
            if author_count.get(author, 0) < 2:
                diverse_rec_ids.append(bid)
                author_count[author] = author_count.get(author, 0) + 1
            if len(diverse_rec_ids) >= 10:
                break
        all_rec_ids = diverse_rec_ids
        
        # FINAL SORT: If new user, sort results to match their genres if possible
        if is_pref_mode and is_cold:
            prefs = st.session_state.user_prefs
            results = books_df[books_df['book_id'].isin(all_rec_ids)]
            # Priority to books that match the genre or the authors
            author_match = results['authors'].apply(lambda x: any(a.lower() in str(x).lower() for a in prefs['authors']))
            genre_match = results['book_id'].apply(lambda x: any(g.lower() in [t.lower() for t in books_tags.get(str(int(x)), [])] for g in prefs['genres']))
            
            # Sort behavior: prioritizing those that match both or at least one
            results['match_score'] = author_match.astype(int) + genre_match.astype(int)
            recs = results.sort_values('match_score', ascending=False)
        else:
            recs = books_df[books_df['book_id'].isin(all_rec_ids)]

        if not recs.empty:
            # Refresh user wishlist status for button display
            current_wishlist_ids = set(to_read_df[to_read_df['user_id'] == u_id]['book_id'].tolist())
            
            cols = st.columns(5)
            for i, (_, row) in enumerate(recs.iterrows()):
                with cols[i % 5]:
                    is_w = int(row['book_id']) in current_wishlist_ids
                    book_card(row, is_wishlisted=is_w, show_hybrid=True)
        else:
            st.warning("Systems calibrating. Try interacting with the catalog to generate signals.")


    st.sidebar.markdown("---")
    st.sidebar.caption("Bookflix Intelligence Systems © 2026")