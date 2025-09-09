import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
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
# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="🎬 Gemini Movie Recommendation", layout="centered")
st.title("🎬 Movie Recommendation System (Gemini)")
st.write("Get movie recommendations powered by Google Gemini AI.")

query = st.text_input("Enter a movie name or description:", placeholder="e.g. A sci-fi movie about space and AI")

if st.button("Recommend"):
    if query.strip():
        with st.spinner("Asking Gemini for recommendations..."):
            prompt = f"""
You are an intelligent movie recommendation engine.

Task:
Given a movie title or description: "{query}", recommend exactly 5 movies.

Rules:
1. If "{query}" belongs to a known franchise (e.g., Marvel, Harry Potter, Fast & Furious, etc.):
   - If the user explicitly asks for movies from the same franchise, recommend 5 movies from that franchise.
   - Otherwise, recommend 5 movies similar in genre, theme, or vibe.
2. If "{query}" is not from a franchise, always recommend 5 movies similar in genre, tone, and audience.
3. Avoid repeating the same movie as "{query}".
4. Prioritize popular, critically acclaimed, or audience-loved movies.
5. Output only the movie titles as a clean, numbered list.

Example Output:
1. Movie Title One
2. Movie Title Two
3. Movie Title Three
4. Movie Title Four
5. Movie Title Five
"""

            response = model.generate_content(prompt)
            response_text = response.text
            st.subheader("🎥 Recommended Movies")
            movies = [line.split("**")[1] for line in response_text.splitlines() if "**" in line]
            if movies == []:
                import re
                movies = re.findall(r"\d+\.\s*(.*)", response_text)

            print(movies)
            print(response_text)
            import movie_details as md
            for movie in movies:
                details = md.search_movie(movie)
                if details.get("error"):
                    st.write(f"**{movie}** - Not found in database.")
                else:
                    st.write(f"### {details['title']} ({details['release_date'][:4]})")
                    if details.get("poster_url"):
                        st.image(details["poster_url"], width=200)
                    st.write(f"**Overview:** {details['overview']}")
                    st.write(f"**Rating:** {details['rating']} | Budget:`$` {details['budget']} | Revenue:`$` {details['revenue']}")
                    genres = ", ".join([g['name'] for g in details.get('genres', [])])
                    st.write(f"**Genres:** {genres}")
                    if details.get("trailer_url"):
                        st.write(f"[Watch Trailer]({details['trailer_url']})")
                    st.markdown("---")
    else:
        st.warning("Please enter a movie name or description.")
