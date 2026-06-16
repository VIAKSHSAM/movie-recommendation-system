import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------- POSTER FUNCTION --------------------

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f351be27b76787cddc3a8a2646b33cb5"

        response = requests.get(
            url,
            verify=False,
            timeout=10
        )

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        # fallback image
        return "https://via.placeholder.com/500x750?text=No+Image"

    except Exception as e:
        print("Poster Error:", e)
        return "https://via.placeholder.com/500x750?text=Error"

# -------------------- RECOMMEND FUNCTION --------------------

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title

        poster = fetch_poster(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

# -------------------- LOAD DATA --------------------

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similariry.pkl', 'rb'))

# -------------------- STREAMLIT UI --------------------

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

# -------------------- BUTTON --------------------

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])