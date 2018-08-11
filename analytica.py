# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 17:26:30 2018

@author: 13pra
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
import os

import nltk
nltk.download('punkt')
nltk.download('stopwords')
import math
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk import ngrams
from nltk.stem.porter import *
import os

#df1 = pd.read_csv('Ameriprise Financial 08-05-18 20.43.46.csv')
#df2 = pd.read_csv('deloitte 08-05-18 16.02.31.csv')
#df3 = pd.read_csv('facebook 08-05-18 15.58.14.csv')
#df4 = pd.read_csv('General Mills 08-05-18 20.36.59.csv')
#df5 = pd.read_csv('Google 08-05-18 15.25.58.csv')
#df6 = pd.read_csv('kpmg 08-05-18 16.01.04.csv')
#df7 = pd.read_csv('Land O Lakes 08-05-18 20.42.50.csv')
#df8 = pd.read_csv('pwc 08-05-18 15.55.24.csv')
#df9 = pd.read_csv('Slalom Consulting 08-05-18 20.45.08.csv')
#df10 = pd.read_csv('Wallmart 08-05-18 15.51.20.csv')
#, df2, df3, df4, df5, df6,df7, df8, df9, df10
files = [s for s in os.listdir() if s.endswith('.csv')]
filename = files

categories_df = pd.read_csv('../KeywordCategory.csv')
categories_df=categories_df.drop_duplicates()
categories =pd.Series(categories_df.iloc[:,1])
categories.index =pd.Series(categories_df.iloc[:,0])

b = pd.DataFrame()
for file in filename:

    d = pd.read_csv(file).dropna()
    if not(d.empty):
       d= d.sort_values(by = 'Location')
    else:
        continue
    print(file)
    d = d.reset_index(drop=True)

    countlist = []


    # initial cleaning
    def get_tokens(text):
      lowers = text.lower()
      #remove the punctuation
      remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
      no_punctuation = lowers.translate(remove_punctuation_map)
      tokens = nltk.word_tokenize(no_punctuation)
      return tokens
    loctn = list(d['Location'])
    #industry = list(d['Industry'])
    l=set(loctn)
    l = list(l)

    # original count overall frequency
    for locat in l:
        file = d[d['Location']==locat]
        comp_name = d[d['Location']==locat]['Company Name'].values[0]
        ind = d[d['Location']==locat]['Industry'].values[0]
        state = d[d['Location']==locat]['State'].values[0]
        tokens = get_tokens(str(file['Job Title']))
        count = Counter(tokens)
        count.most_common(5)
                # get rid of stop words/ numbers
        filtered = [w for w in tokens if not w in stopwords.words('english')]
        filtered = [w for w in filtered if not w.isdigit() == True]
        filtered = [w for w in filtered if not len(w) <= 2]

        # get rid of stemming
#        stemmer = PorterStemmer()
#        stemmed = stem_tokens(filtered, stemmer)

        count = Counter(filtered)
#        count.most_common(5)

#        count_st = Counter(stemmed)
#        count_st.most_common(5)

        #countlist.append(count)

        twicegrams = ngrams(filtered, 2)
        lst_combine = list()
        for grams in twicegrams:
            grams = grams[0] +" "+ grams[1]
            lst_combine.append(grams)

        count_twicegram = Counter(lst_combine)
        countlist.append(count_twicegram)


        a = count.most_common(len(count))
        c = count_twicegram.most_common(len(count_twicegram))

        a=pd.DataFrame(a)
        a.columns = ['Keyword','count']
        a['Company'] = comp_name
        a['Location'] = locat
        a['State'] = state
        c = pd.DataFrame(c)
        c.columns = ['Keyword','count']
        c['Company'] = comp_name
        c['Location'] = locat
        c['State'] = state
        b = b.append(a)
        b['Industry'] = ind
        b=b.append(c)

        #scores = {word: tfidf(word, count, countlist) for word in count}





    def stem_tokens(tokens, stemmer):
      stemmed = []
      for item in tokens:
        stemmed.append(stemmer.stem(item))
      return stemmed


b['Category']=b.apply(lambda x: categories.get(x[2], x[2]).title(), axis=1)
b.to_csv('Fortune500_bigrms.csv', sep=',', encoding='utf-8')

##################################

#### without stemming
#TF-IDF(t)=TF(t)×IDF(t)
def tf(word, count):
  return count[word] / sum(count.values())

def n_containing(word, countlist):
    return sum(1 for count in countlist if word in count)

def idf(word, countlist):
  return math.log(len(countlist) / (1 + n_containing(word, countlist)))

def tfidf(word, count, countlist):
  return tf(word, count) * idf(word, countlist)

#for i, count in enumerate(countlist):
#  print("Top words")
#  scores = {word: tfidf(word, count, countlist) for word in count}
#  sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#
#  for word, score in sorted_words[:10]:
#    print("\tWord: {}, TF-IDF: {}".format(word, score))
