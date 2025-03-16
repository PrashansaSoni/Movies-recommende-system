import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests

# Function to fetch movie posters
def fetch_posters(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ec7b00d32bb8baa8028cf2e20b07a974&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data.get('poster_path', '')

# Load the dataset and similarity matrix
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies_df['title'].values  # Extract movie titles

# Function to recommend movies
def recommend(movie):
    try:
        if movie not in movies_df['title'].values:
            return ["Movie not found in dataset!"], []

        # Get the index of the selected movie
        movie_index = movies_df[movies_df['title'] == movie].index[0]

        # Validate the similarity matrix
        if not isinstance(similarity, np.ndarray) or len(similarity.shape) != 2:
            return ["Error: Invalid similarity matrix!"], []

        # Get similarity scores for the selected movie
        distances = similarity[movie_index]

        # Sort movies based on similarity and get top 5 recommendations
        movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

        # Collect recommended movie titles and posters
        recommended_movies = []
        recommended_posters = []
        
        for i in movies_list:
            movie_title = movies_df.iloc[i[0]]['title']
            movie_id = movies_df.iloc[i[0]]['movie_id']  # Ensure your dataset has a 'movie_id' column
            recommended_movies.append(movie_title)
            recommended_posters.append(fetch_posters(movie_id))
        
        return recommended_movies, recommended_posters

    except Exception as e:
        return [f"Error: {e}"], []

# Streamlit UI
st.title("Movie Recommender System")

# Dropdown for movie selection
option = st.selectbox("Select a movie:", movies_list)

if st.button("Recommend"):
    names, posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)  # Create 5 columns for displaying movies

    for i in range(len(names)):
        with [col1, col2, col3, col4, col5][i]:  # Dynamically place in columns
            st.image(posters[i], caption=names[i], use_container_width=True)
