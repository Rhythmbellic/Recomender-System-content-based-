import numpy as np
import pandas as pd
movies=pd.read_csv("tmdb_5000_movies.csv")
credits=pd.read_csv("tmdb_5000_credits.csv")
movies.head()
credits.head(5)
#lets merge both the dataframw
data=movies.merge(credits,on='title')
data.describe()
data.info()
#drop unnecessary tags for recomender system
#we dont want following tags
#budget,homepage,orignal language(as most of movies are in english so notjing is important),orignal title(we are keeping one title already),popularit(as it is content based,prodution countries,etc)
data1=data[['movie_id','title','overview','genres','keywords','production_companies','cast','crew']]
#checking null values
data1.isnull().sum()
#dropping null values
data1.dropna(inplace=True)
#checking duplicacy
data1.duplicated().sum()
data1.iloc[0].genres
import ast
def converter(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l
data1['genres']=data1['genres'].apply(converter)
data1['keywords']=data1['keywords'].apply(converter)
data1['production_companies']=data1['production_companies'].apply(converter)
def converterpro(obj):
    l=[]
    a=1
    for i in ast.literal_eval(obj):
        if a==4:
            break
        else:
            l.append(i['name'])
            a=a+1
    return l
data1['cast']=data1['cast'].apply(converterpro)
def converter2(obj):
  l=[]
  for i in ast.literal_eval(obj):
      if i['job']=='Director':
          l.append(i['name'])
          break
  return l
data1['crew']=data1['crew'].apply(converter2)
data1['overview']=data1['overview'].apply(lambda x:x.split())
data1['genres']=data1['genres'].apply(lambda x:[i.replace(' ','')for i in x])
data1['keywords']=data1['keywords'].apply(lambda x:[i.replace(' ','')for i in x])
data1['cast']=data1['cast'].apply(lambda x:[i.replace(' ','')for i in x])
data1['crew']=data1['crew'].apply(lambda x:[i.replace(' ','')for i in x])
data1['production_companies']=data1['production_companies'].apply(lambda x:[i.replace(' ','')for i in x])
data1['tags']=data1['overview']+data1['genres']+data1['keywords']+data1['cast']+data1['crew']+data1['production_companies']
moviedata=data1[['movie_id','title','tags']]
moviedata['tags']=moviedata['tags'].apply(lambda x:' '.join(x))
moviedata['tags']=moviedata['tags'].apply(lambda x:x.lower())
#our data preproessing is done now we will work on modelling
#now we will do textvectorization using bag of words technique
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return ' '.join(y)
moviedata['tags']=moviedata['tags'].apply(stem)
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
vec=cv.fit_transform(moviedata['tags']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vec)
def recommend(movie):
    movie_index=moviedata[moviedata['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print(moviedata.iloc[i[0]].title)
a=input("enter the name of movie")
b=recommend(a)
print(b)


