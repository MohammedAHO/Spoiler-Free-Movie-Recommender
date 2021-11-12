#!/usr/bin/env python
# coding: utf-8

# # Movies Recommender App

# This file contains the recommendation system together with the Web App and API codes.

# In order to run this file, download the file as (.py) then open it using this command on Anaconda Prompt:
# * streamlit run Movies_Recommender_App.py

# In[1]:


import pandas as pd
import streamlit as st
import csv
import json, requests
from collections import defaultdict
from collections import Counter


# ## API

# Using api, we will get the movie ID using its name. And get the movie names from the movie ID.

# In[ ]:


def get_title(mov_id):
    url = "https://imdb-api.com/en/API/Title/k_4vhtmp5e/" + mov_id
    response = requests.get(url)
    json_from_id = json.loads(response.text)
    return json_from_id


# In[ ]:


def get_id(mov_title):
    url = "https://imdb-api.com/en/API/SearchTitle/k_4vhtmp5e/" + mov_title
    response = requests.get(url)
    json_from_title = json.loads(response.text)
    return json_from_title['results'][0]['id']


# ## Recomender

# In[4]:


movie_user_map = defaultdict(list)
user_movie_map = defaultdict(list)


# In[5]:


with open('df_reviews_web.csv', 'r', encoding="utf8") as csvfile:
    w = csv.reader(csvfile)
    for row in w:
        user_movie_map[row[1]].append(row[2])
        movie_user_map[row[2]].append(row[1])


# In[6]:


def get_similar_movie(user_movie_map,movie_user_map,m):
    biglist = []
    for u in user_movie_map[m]:                 # get all users that liked this movie
        biglist.extend(movie_user_map[u])       # find all other movies those users liked and add to biglist
    return Counter(biglist).most_common(4)[1:]  # use counter to 'count' the other movies that show up most common


# In[7]:


def get_movie_recommendation(user_movie_map,movie_user_map,u1):
    biglist = []
    for m in movie_user_map[u1]:                # for the movies a specific user likes
        for u in user_movie_map[m]:             # get other users who liked those movies
            biglist.extend(movie_user_map[u1])  # find the other movies those "similar folks" most liked
    return Counter(biglist).most_common(3)      # return tuples of (most common id, count)


# # HTML

# * There will be two approaches of our app
# * Get personal recommendations  ---> take (user ID) as input ---> use API to get mov_name
# * Get movies similar to a movie ---> take (movie name) as input ---> API to get movie id ---> use API to get mov_name

# In[3]:


df_reviews = pd.read_csv('df_reviews_web.csv', index_col=0)


# In[21]:


st.title("Movies Recommender \n(Spoiler Free Reviews)")
st.markdown("This web app will take a movie and suggest three movies that are similar to it.")
st.header("Please choose one of the recommendation approaches")
option = st.selectbox('Select from here.',
                      ('Get personal recommendations',
                       'Get movies similar to a movie'))


# In[1]:


if option == 'Get personal recommendations':
    st.text_input('Enter your user_id.', key="user_id")
    # We can access the value at any point with: st.session_state.user_id
    similar_movies = get_movie_recommendation(user_movie_map,movie_user_map, st.session_state.user_id)
    for i in range(3):
        recommended_movie = similar_movies[i][0] # movies ids
        json_from_id = get_title(recommended_movie)
        st.header(f"#{i+1}: " + json_from_id['title'])
        st.subheader('Some reviews about the movies')
        st.caption(df_reviews[df_reviews.movie_id == recommended_movie]['review_text'].sample().values[0])
        st.caption(df_reviews[df_reviews.movie_id == recommended_movie]['review_text'].sample().values[0])
        st.image(json_from_id['image'], width=720)


# In[2]:


if option == 'Get movies similar to a movie':
    st.text_input('Enter a movie name.', key="movie_name")
    # We can access the value at any point with: st.session_state.movie_name
    movie_id = get_id(st.session_state.movie_name)
    similar_movies = get_similar_movie(user_movie_map,movie_user_map, movie_id)
    for i in range(3):
        recommended_movie = similar_movies[i][0] # movies ids
        json_from_id = get_title(recommended_movie)
        st.header(f"#{i+1}: " + json_from_id['title'])
        st.subheader('Some reviews about the movies')
        st.caption(df_reviews[df_reviews.movie_id == recommended_movie]['review_text'].sample().values[0])
        st.caption(df_reviews[df_reviews.movie_id == recommended_movie]['review_text'].sample().values[0])
        st.image(json_from_id['image'], width=720)

