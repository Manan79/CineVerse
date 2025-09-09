import streamlit as st
import streamlit.components.v1 as components
import streamlit as st
import google.generativeai as genai
import os
import re
import streamlit as st
import matplotlib.pyplot as plt
from movie_sumariser import search_movie, get_movie_details, get_cast_with_images, get_release_info, get_movie_composers, IMG_BASE
import movie_details as md
from movie_chatbot import chatbot
from dotenv import load_dotenv

load_dotenv()
API_KEY = st.secrets.get("TMDB_API_KEY", os.getenv("TMDB_API_KEY"))
# Debug print
st.write("API key loaded:", bool(API_KEY))

# Page configuration
st.set_page_config(
    page_title="CineVerse",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for modern, colorful theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f7ff 100%);
        color: #1a3a5f;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #1a3a5f;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .app-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: #5f7a9d;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Movie cards */
    .movie-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 25px;
        height: 100%;
        box-shadow: 0 8px 25px rgba(26, 115, 232, 0.15);
        border: 1px solid rgba(66, 133, 244, 0.2);
    }
    
    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(26, 115, 232, 0.25);
        z-index: 10;
    }
    
    /* Rating stars */
    .rating {
        color: #f4b400;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Chat bubbles */
    .user-bubble {
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        color: white;
        border-radius: 20px 20px 5px 20px;
        padding: 15px 20px;
        margin: 12px 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #e8f0fe 0%, #d2e3fc 100%);
        color: #1a3a5f;
        border-radius: 20px 20px 20px 5px;
        padding: 15px 20px;
        margin: 12px 0;
        max-width: 75%;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.15);
        font-size: 0.95rem;
        line-height: 1.4;
        border: 1px solid rgba(66, 133, 244, 0.2);
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        height: 500px;
        overflow-y: auto;
        box-shadow: 0 10px 30px rgba(26, 115, 232, 0.15);
        border: 1px solid rgba(66, 133, 244, 0.2);
        margin-bottom: 20px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1967d2 0%, #3367d6 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.4);
    }
    
    .secondary-btn {
        background: linear-gradient(135deg, #34a853 0%, #2e8b57 100%) !important;
        box-shadow: 0 4px 15px rgba(52, 168, 83, 0.3) !important;
    }
    
    .secondary-btn:hover {
        background: linear-gradient(135deg, #2e8b57 0%, #1e7e34 100%) !important;
        box-shadow: 0 6px 20px rgba(52, 168, 83, 0.4) !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.95);
        color: #1a3a5f;
        border: 2px solid #d2e3fc;
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #1a73e8;
        box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 30px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0 8px 25px rgba(26, 115, 232, 0.1);
        border: 1px solid rgba(66, 133, 244, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 15px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        color: #5f7a9d;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    
    /* Game image */
    .game-image {
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(26, 115, 232, 0.2);
        margin-bottom: 25px;
        transition: all 0.3s ease;
        border: 1px solid rgba(66, 133, 244, 0.2);
    }
    
    .game-image:hover {
        transform: scale(1.02);
    }
    
    /* Score display */
    .score-display {
        background: linear-gradient(135deg, #e8f0fe 0%, #d2e3fc 100%);
        border-radius: 20px;
        padding: 20px 30px;
        box-shadow: 0 8px 25px rgba(26, 115, 232, 0.15);
        margin-bottom: 25px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a73e8;
        border: 1px solid rgba(66, 133, 244, 0.2);
    }
    

    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Landing page */

    /* Fix for white patches in images */
    img {
        border-radius: 12px;
        background-color: #f8fbff;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8fbff 0%, #e8f0fe 100%);
    }
    
    /* Remove white patches from expanders */
    .stExpander {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid rgba(66, 133, 244, 0.2);
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)



# ---------------------------
# HELPER FUNCTIONS
# ---------------------------


def get_chatbot_response(user_input):
    try:
        return chatbot(user_input)
    except Exception as e:
        return "Sorry, I'm having trouble processing your request right now."


# Navigation
def show_landing_page():
    st.markdown('<h1 class="app-title">CineVerse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Your ultimate movie companion - Discover, Chat, Play</p>', unsafe_allow_html=True)
    
    # Hero Section
    with st.container():
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown("## 🎬 Explore the World of Movies")
            st.markdown("Dive into a universe of cinematic wonders. Get personalized recommendations, chat with our AI movie expert, and test your movie knowledge with fun games!")
            if st.button("🚀 Get Started", key="get_started_top"):
                st.session_state.current_page = "recommendations"
                st.rerun()
        with col2:
            st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80", use_container_width=True)
    # Features Grid
    st.markdown("## ✨ Features")
    cols = st.columns(3)
    
    with cols[0]:
        # st.markdown('<div class="
        # ">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">🎭</div>', unsafe_allow_html=True)
        st.markdown("### Smart Recommendations")
        st.markdown("Discover new movies tailored to your taste with our advanced recommendation system.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">💬</div>', unsafe_allow_html=True)
        st.markdown("### AI Movie Assistant")
        st.markdown("Chat with our intelligent assistant to get movie information, trivia, and personalized suggestions.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">🎮</div>', unsafe_allow_html=True)
        st.markdown("### Movie Recognition")
        st.markdown("Test your movie knowledge with our fun guessing game and compete for high scores.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Get Started Button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True, key="get_started"):
            st.session_state.current_page = "recommendations"
            st.rerun()

st.cache_data(ttl=3600)
def get_movie_recommendations(query):
    """Get movie recommendations from Gemini AI"""
    prompt = f"""
        You are an intelligent movie recommendation engine.
        
        Task:
        Given a movie title or description: "{query}", recommend exactly 5 movies.
        
        Rules:
        1. If "{query}" belongs to a known franchise (e.g., Marvel, Harry Potter, Fast & Furious, etc.):
           - If the user explicitly asks for movies from the same franchise, recommend 8 movies from that franchise.
           - Otherwise, recommend 8 movies similar in genre, theme, or vibe.
        2. If "{query}" is not from a franchise, always recommend 8 movies similar in genre, tone, and audience.
        3. Avoid repeating the same movie as "{query}".
        4. Prioritize popular, critically acclaimed, or audience-loved movies.
        5. Output only the movie titles as a clean, numbered list.
        
        Example Output:
        1. Movie Title One
        2. Movie Title Two
        3. Movie Title Three
        4. Movie Title Four
        5. Movie Title Five
        6. Movie Title six
        7. Movie Title seven
        8. Movie Title eight
"""

    response = model.generate_content(prompt)
    response_text = response.text
    
    # Extract movie titles from the response
    movies = [line.split("**")[1] for line in response_text.splitlines() if "**" in line]
    if movies == []:
        movies = re.findall(r"\d+\.\s*(.*)", response_text)
    
    return movies

# Main app navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

# Sidebar navigation
with st.sidebar:
    st.markdown("  # 🎬 CineVerse")
    st.markdown("---")
    
    nav_options = {
        "🏠 Landing": "landing",
        "🎭 Recommendations": "recommendations", 
        "🎮 Movie Summarizer": "game",
        "💬 Movie Chatbot": "chatbot"
    }
    
    for option, page in nav_options.items():
        if st.button(option, use_container_width=True, key=page):
            st.session_state.current_page = page
            st.rerun()
    

    

# Page routing
if st.session_state.current_page == "landing":
    show_landing_page()


# ---------------------------
# CONFIGURATION
# ---------------------------

# Put your Gemini API key here (or set as env var)
gemin_api = os.getenv("GOOGLE_API_KEY")
if gemin_api:
    print("Gemini API key loaded successfully")

genai.configure(api_key=gemin_api)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")



# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Home page with search
if st.session_state.current_page == "home":
    query = st.text_input("Enter a movie name or description:", placeholder="e.g. A sci-fi movie about space and AI")

    if st.button("Recommend"):
        if query.strip():
            with st.spinner("Asking Gemini for recommendations..."):
                movies = get_movie_recommendations(query)
                st.session_state.recommended_movies = movies
                st.session_state.search_query = query
                st.session_state.current_page = "recommendations"
                st.rerun()
        else:
            st.warning("Please enter a movie name or description.")

# Recommendations page
elif st.session_state.current_page == "recommendations":
    st.markdown("## 🎭 Movie Recommendations")
    
    # Search box
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search movies...", 
                                   placeholder="Type a movie title, genre, or actor...",
                                   value=st.session_state.get("search_query", ""))
    with col2:
        if st.button("Search"):
            if search_query.strip():
                with st.spinner("Asking Gemini for recommendations..."):
                    movies = get_movie_recommendations(search_query)
                    st.session_state.recommended_movies = movies
                    st.session_state.search_query = search_query
                    st.rerun()
            
    
    # Display recommended movies in a grid
    if "recommended_movies" in st.session_state and st.session_state.recommended_movies:
            st.markdown(f"### Recommendations for: *{st.session_state.search_query}*")

            if "recommended_movies" in st.session_state:
                movies = st.session_state.recommended_movies
                movie_details_list = []

                # Get details for all movies
                with st.spinner("Fetching movie details..."):
                    for movie in movies:
                        details = md.search_movie(movie)
                        movie_details_list.append(details)

                # Display movies in a grid
                cols = st.columns(4)

                for i, details in enumerate(movie_details_list):
                    with cols[i % 4]:

                        if details.get("error"):
                            st.write(f"**{movies[i]}** - Not found in database.")
                        else:
                            if details.get("poster_url"):
                                st.image(details["poster_url"], use_container_width=True)

                            st.markdown(f"### {details['title']} ({details.get('release_date', 'N/A')[:4] if details.get('release_date') else 'N/A'})")

                            if details.get('genres'):
                                genres = ", ".join([g['name'] for g in details.get('genres', [])])
                                st.markdown(f"**Genre:** {genres}")

                            if details.get("rating"):
                                st.markdown(f'<p class="rating">⭐ {details["rating"]}/10</p>', unsafe_allow_html=True)

                            if details.get("overview"):
                                st.markdown(f"**Description:** {details['overview'][:100]}..." if len(details['overview']) > 100 else f"**Description:** {details['overview']}")

                            if details.get("budget") and details.get("revenue"):
                                st.markdown(f"**Budget:** `${details['budget']}` | **Revenue:** `${details['revenue']}`")

                            if details.get("trailer_url"):
                                st.markdown(f"[Watch Trailer]({details['trailer_url']})")

                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown("---")
            # Back button
            if st.button("← Back to Search"):
                st.session_state.current_page = "home"
                st.rerun()
    
elif st.session_state.current_page == "chatbot":
    st.markdown("## 💬 Movie Chatbot")
    st.markdown("Ask me anything about movies!")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "content": "Hi there! I'm your movie assistant. I can help you find information about movies, actors, or make recommendations. What would you like to know?"}
        ]
    
    # Chat container
    # st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Type your message...", label_visibility="collapsed", placeholder="Ask about movies...", key="chat_input")
    with col2:
        if st.button("Send", use_container_width=True) and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            bot_response = get_chatbot_response(user_input)
            st.session_state.chat_history.append({"role": "bot", "content": bot_response})
            st.rerun()

elif st.session_state.current_page == "game":
    
    st.subheader("🔎 Search for a Movie")
    query = st.text_input("Enter movie name:")
    if st.button("Search") and query:
        movie = search_movie(query)
        if movie:
            details = get_movie_details(movie["id"])
            # --- Main Info ---
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(IMG_BASE + details["poster_path"], use_container_width=True)
            with col2:
                st.markdown(f"## {details['title']} ({details['release_date'][:4]})")
                st.write(f"⭐ {details['vote_average']} | 🎭 {', '.join([g['name'] for g in details['genres']])}")
                st.write(f"📅 Release: {details['release_date']} | ⏱️ Runtime: {details['runtime']} min")
                st.write(f"💰 Budget: ${details['budget']:,} | Revenue: ${details['revenue']:,}")
                st.write("### Overview")
                st.write(details["overview"])


            # Ai generated OVerview
            st.write("### AI Generated Overview")
            # button_clicked = st.button("Generate Overview")
          
            answer = chatbot(f"Provide a concise and engaging overview of the movie '{details['title']}' in 200 words.")
            st.write(answer)
            
            # --- Cast ---
            st.write("### 🎭 Top Cast")
            cast = get_cast_with_images(details["credits"])
            cols = st.columns(5)
            for i, actor in enumerate(cast):
                with cols[i % 5]:
                    if actor["profile"]:
                        st.image(actor["profile"], use_container_width=True)
                    st.caption(f"**{actor['name']}**\n({actor['character']})")

            # --- Composers ---
            composers = get_movie_composers(details["title"])[1]
            if composers:
                st.subheader(f"🎬 Music Team")
                cols = st.columns(len(composers))
                for i, comp in enumerate(composers):
                    with cols[i % len(composers)]:
                        if comp["profile"]:
                            st.image(comp["profile"], caption=comp["name"], use_container_width=True)
                        else:
                            st.write(f"👤 {comp['name']} (No photo)")
            else:
                st.warning("No composer info found on TMDb.")
            # --- Regional Certifications ---
            st.write("### 🌍 Regional Ratings")
            release_info = get_release_info(details)
            if release_info:
                countries = [r["country"] for r in release_info]
                certs = [r["certification"] for r in release_info]
                fig, ax = plt.subplots()
                ax.bar(countries, range(len(countries)))  # simple bar just to show
                ax.set_xticks(range(len(countries)))
                ax.set_xticklabels(countries, rotation=90)
                ax.set_ylabel("Certification Index")
                st.pyplot(fig)
                st.write("Certifications:", release_info)
            
            
            # --- Popularity Chart ---
            st.write("### 📈 Popularity & Revenue")
            fig, ax = plt.subplots()
            ax.bar(["Popularity", "Budget", "Revenue"], 
                   [details["popularity"], details["budget"]/1e6, details["revenue"]/1e6])
            ax.set_ylabel("Value (popularity units / millions $)")
            st.pyplot(fig)
            # --- Backdrops ---
            st.write("### 🖼️ Posters")
            for img in details["images"]["backdrops"][:5]:
                st.image(IMG_BASE + img["file_path"], use_container_width=True)
            
        else:
            st.error("❌ Movie not found. Try another name.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #5f7a9d; padding: 30px 0 10px 0;">
        <p>© 2025 CineVerse | Made with ❤️ for movie lovers</p>
    </div>
    """,
    unsafe_allow_html=True
)
