# -*- coding: utf-8 -*-
"""
Useful function to extract words and calculate the sentiment of a page thanks to AFINN-111 dictionary
"""

import wikipedia
from nltk import *

stopwords = corpus.stopwords.words('english')

average_sentiment = []


# put word and their sentiment into a dictionary
def open_dictionary():
    word=[]
    sentScore=[]
    with open('AFINN/AFINN-111.txt', 'r') as in_file:
        for line in in_file.readlines():
            # word and values are separated by a tab
            word.append(line.split('\t')[0]) 
            sentScore.append(line.split('\t')[1].split('\n')[0])
            
        return dict(zip(word, sentScore))
       

#normalize the text
#tokenize, remove stopwords, lemmatize
def normalize_text(text):
    #put the text in words
    tokenized_text = word_tokenize(text)
    #remove stopwords
    no_stopwords_text= [w for w in tokenized_text if w.lower() not in stopwords]
    #lemmatize    
    lemmatized_text = [WordNetLemmatizer().lemmatize(t) for t in no_stopwords_text]
    
    return lemmatized_text


#evaluate the sentiment of a list of words
def sentiment(words, sentiment_dictionary):
    count = 0
    sentiment_value = 0
    average_sentiment = 0
    for word in words:
        for key in sentiment_dictionary: # check if word appears in the dictionary
            # we count the number of words and sum their sentiment
            if word.lower() == key:   
                count += 1
                sentiment_value += float(sentiment_dictionary[key])
            if count > 0:
                average_sentiment = sentiment_value/count
                
    return average_sentiment

#evalute the average sentiment of a company
def company_sentiment(company):
    #we load the page and extract content
    page = wikipedia.page(company)
    text = page.content

    sentiment_dictionary = open_dictionary()
    
    normalized_text = normalize_text(text)
    
    #average_sentiment = sentiment(normalized_text,sentiment_dictionary)
    average_sentiment.append(sentiment(normalized_text,sentiment_dictionary))              
    #print "The average sentiment of " + company + ' page is: '+str(average_sentiment)
    #return str(average_sentiment)
    return average_sentiment


def empty_sentiments_list():
    global average_sentiment
    average_sentiment = []
    
    