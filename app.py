import streamlit as st
import pickle
import requests  #API call krne k liye

def fetch_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=751b59478b765f47f7f0411d4cf0f35b'.format(movie_id))

    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+ data['poster_path']              #data['poster path']

def recommend(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[movie_index]  # distances m given movie ka harek movie se cosine distance aa jayega
    movies_list_5 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                  1:6]  # first 5 closest movie nikalega

    recommended_movies = []
    recommended_movies_posters=[]

    for i in movies_list_5:
        movie_id=movie_list.iloc[i[0]].movie_id

        recommended_movies.append(movie_list.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = pickle.load(open('movies.pkl', 'rb'))
movie_list_chkbox = movie_list['title'].values

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Select a movie from the list",
    movie_list_chkbox)

if st.button("Recommend"):
    names,posters=recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(names[0])
        st.image(posters[0])

    with col2:
        st.write(names[1])
        st.image(posters[1])

    with col3:
        st.write(names[2])
        st.image(posters[2])

    with col4:
        st.write(names[3])
        st.image(posters[3])

    with col5:
        st.write(names[4])
        st.image(posters[4])