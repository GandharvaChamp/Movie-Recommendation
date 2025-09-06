import streamlit as st
import pandas as pd
import numpy as np

import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ff89232d74e126bbb487629da1ec4bd8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
with open("movies_title.pkl",'rb') as f:
    movies_title = pickle.load(f)



# selected_movie_name = st.selectbox("How would you like to be contacted?", movies_title['title'].values)

similarity = pickle.load(open('movies_dict.pkl','rb'))

def recommend(movie):
    movie_index = movies_title[movies_title['title'] == movie].index[0]
    # distances = similarity[movie_index]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    # movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies_title.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies_title.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies_title['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
    
