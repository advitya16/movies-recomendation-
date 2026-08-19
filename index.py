import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Watchlist",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    /* Hide Streamlit default components */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Background styling */
    .stApp {
        background: #080a10;
        color: #e0e6ed;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        padding-top: 1rem;
    }

    /* Top Navigation Bar */
    .nav-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 2rem 1.5rem 2rem;
    }

    .nav-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: 0.5px;
    }

    .account-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        color: #cbd5e1;
    }

    /* Results Header */
    .results-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #f8fafc;
        margin-left: 2rem;
        margin-bottom: 1.5rem;
    }

    /* Streamlit Selectbox Override to match glowing pill search */
    div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 24px !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.15);
        color: #e2e8f0 !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: rgba(56, 189, 248, 0.6) !important;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.3);
    }

    /* Movie Poster Cards */
    .poster-card {
        position: relative;
        width: 100%;
        height: 310px;
        border-radius: 16px;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 20px;
    }

    .poster-card:hover {
        transform: translateY(-6px);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.8), 0 0 15px rgba(56, 189, 248, 0.25);
    }

    /* Gradient overlay on bottom of card */
    .card-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 12px 14px;
        background: linear-gradient(to top, rgba(0, 0, 0, 0.92) 0%, rgba(0, 0, 0, 0.4) 60%, transparent 100%);
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    .rating-badge {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #ffffff;
    }

    .heart-btn {
        font-size: 1.1rem;
        cursor: pointer;
    }

    .movie-fallback-title {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 85%;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_dataset():
    dataset = pickle.load(open("movies_list.pkl", "rb"))
    similarity_matrix = pickle.load(open("similarity.pkl", "rb"))
    return dataset, similarity_matrix


movies, similarity = load_dataset()


def fetch_recommendations(selected_title, limit=10):
    match_index = movies[movies["title"] == selected_title].index[0]
    scores = similarity[match_index]

    top_matches = sorted(
        list(enumerate(scores)), reverse=True, key=lambda item: item[1]
    )[1 : limit + 1]

    results = []
    for item in top_matches:
        results.append(movies.iloc[item[0]]["title"])
    return results


demo_poster_map = {
    "Superman": "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=600",
    "Batman": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=600",
    "Joker": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=600",
    "Deadpool": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=600",
    "Harry Potter": "https://images.unsplash.com/photo-1514539079130-25950c84af65?q=80&w=600",
}


def get_poster_style(title_text):
    for key, url in demo_poster_map.items():
        if key.lower() in title_text.lower():
            return f"background-image: url('{url}');"

    return "background: linear-gradient(145deg, #1e293b, #0f172a);"


nav_left, nav_center, nav_right = st.columns([1.5, 3, 1.5])

with nav_left:
    st.markdown(
        """
        <div class="nav-logo">
            <span>🗑️</span> Watchlist
        </div>
    """,
        unsafe_allow_html=True,
    )

with nav_center:
    movie_list = movies["title"].values
    user_selection = st.selectbox(
        "",
        movie_list,
        index=0,
        placeholder="🔍 What would you like to watch?",
        label_visibility="collapsed",
    )

with nav_right:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end;">
            <div class="account-badge">
                👤 Account
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

recommendations = fetch_recommendations(user_selection, limit=10)
st.markdown(
    f'<div class="results-title">{len(recommendations)} Movie Results</div>',
    unsafe_allow_html=True,
)


row1_cols = st.columns(5)
for index in range(5):
    movie_name = recommendations[index]
    bg_style = get_poster_style(movie_name)
    rating_score = round(4.0 + (index % 10) * 0.1, 1)
    is_liked = "❤️" if index in [2, 4] else "🤍"

    with row1_cols[index]:
        st.markdown(
            f"""
            <div class="poster-card" style="{bg_style}">
                <div class="movie-fallback-title">{movie_name}</div>
                <div class="card-overlay">
                    <div class="rating-badge">⭐ {rating_score}</div>
                    <div class="heart-btn">{is_liked}</div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )


row2_cols = st.columns(5)
for index in range(5, 10):
    movie_name = recommendations[index]
    bg_style = get_poster_style(movie_name)
    rating_score = round(3.7 + (index % 10) * 0.1, 1)
    is_liked = "❤️" if index in [6, 9] else "🤍"

    with row2_cols[index - 5]:
        st.markdown(
            f"""
            <div class="poster-card" style="{bg_style}">
                <div class="movie-fallback-title">{movie_name}</div>
                <div class="card-overlay">
                    <div class="rating-badge">⭐ {rating_score}</div>
                    <div class="heart-btn">{is_liked}</div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )