#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
import ast
get_ipython().system('pip install nltk')
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[2]:


movies = pd.read_csv('tmdb_5000_credits.csv')
credits = pd.read_csv('tmdb_5000_movies.csv')


# In[3]:


#Movies Dataset
movies.head()


# In[4]:


credits.head()


# In[5]:


#Merge movies and credits dataset based on title
movies.merge(credits,on='title').shape


# In[6]:


#Save the merged dataset in movies dataframe
movies =movies.merge(credits,on='title')


# In[7]:


movies.head(2)


# In[8]:


#Select only related columns for the system
movies= movies[['movie_id','vote_average','title','overview','genres','keywords','cast','crew']]


# In[9]:


movies.info()


# In[10]:


movies.isnull().sum()


# In[11]:


movies.duplicated().sum()


# In[12]:


movies.iloc[0].genres


# In[13]:


def my_convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


# In[14]:


movies['genres']=movies['genres'].apply(my_convert)


# In[15]:


movies['keywords']=movies['keywords'].apply(my_convert)


# In[16]:


movies.head(2)


# In[17]:


def my_convert2(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter !=10:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L


# In[18]:


movies['cast']=movies['cast'].apply(my_convert2)


# In[19]:


def my_fetch_crew(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
    return L


# In[20]:


movies['crew']=movies['crew'].apply(my_fetch_crew)


# In[21]:


movies.head()


# In[22]:


movies['overview'][0]


# In[23]:


movies['overview']=movies['overview'].apply(lambda x:str(x).split())


# In[24]:


movies.head()


# In[25]:


movies.dtypes


# In[26]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(' ','') for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(' ','') for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(' ','') for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(' ','') for i in x])


# In[27]:


movies.head()


# In[28]:


#Create a new column named tags to store all necessary info about each movies
movies['tags']= movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']


# In[29]:


movies.head()


# In[30]:


movies['tags'][0]


# In[31]:


#Create a new dataframe with columns 'movie_id','vote_average','title' and 'tags'
new_df=movies[['movie_id','vote_average','title','tags']]


# In[32]:


new_df.head()


# In[33]:


#Convert tags to string from list
new_df['tags']=new_df['tags'].apply(lambda x:' '.join(x))


# In[34]:


new_df.head()


# In[35]:


new_df['tags'][0]


# In[36]:


#Convert the string to lowercase
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())


# In[37]:


new_df.head()


# In[38]:


#Use CountVectorizer to eliminate stop words from the tags column
cv= CountVectorizer(max_features=5000,stop_words='english')


# In[39]:


#Transform every word into a vector
vectors=cv.fit_transform(new_df['tags']).toarray()


# In[40]:


vectors


# In[41]:


vectors[0]


# In[42]:


cv.get_feature_names()


# In[43]:


#Calculate the cosine distance between each vectors
similarity=cosine_similarity(vectors)


# In[44]:


similarity[2]


# In[45]:


sorted(list(enumerate(similarity[0])) , reverse = True, key=lambda x:x[1])[1:6]


# In[47]:


#Function for Content Based Recommendation
def recommend_content(movie):
    movie_index= new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)), reverse=True,key=lambda x:x[1])[0:5]
    title=[]
    rating=[]
    for i in movies_list:
        title.append(new_df.iloc[i[0]].title)
        rating.append(new_df.iloc[i[0]].vote_average)
    df = pd.DataFrame(list(zip(title, rating)),
               columns =['title', 'rating'])
    return df
    
   


# In[48]:


#Pass a movie name through the function and get 5 movies recommended by content
recommended_movies=recommend_content('Batman')
recommended_movies


# In[50]:


def recommend_content(movie):
    movie_index= new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)), reverse=True,key=lambda x:x[1])[0:5]
    title=[]
    rating=[]
    for i in movies_list:
        title.append(new_df.iloc[i[0]].title)
        rating.append(new_df.iloc[i[0]].vote_average)
    df = pd.DataFrame(list(zip(title, rating)),
               columns =['title', 'rating'])
    return df
    


# In[51]:


recommended_movies=recommend_content('Avatar')
recommended_movies


# In[52]:


def recommend_content(movie):
    movie_index= new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)), reverse=True,key=lambda x:x[1])[0:5]
    title=[]
    rating=[]
    for i in movies_list:
        title.append(new_df.iloc[i[0]].title)
        rating.append(new_df.iloc[i[0]].vote_average)
    df = pd.DataFrame(list(zip(title, rating)),
               columns =['title', 'rating'])
    return df
    


# In[53]:


recommended_movies=recommend_content('The Dark Knight Rises')
recommended_movies


# In[55]:


import pickle


# In[56]:


pickle.dump(new_df, open('movies.pkl','wb'))


# In[57]:


new_df['title'].values


# In[58]:


pickle.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:




