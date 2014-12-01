# -*- coding: utf-8 -*-
"""
Useful function to extract words and calculate the sentiment of a page
use AFINN-111 dictionary
"""

import wikipedia
from nltk import word_tokenize, WordNetLemmatizer, corpus

stopwords = corpus.stopwords.words('english')

average_sentiment = []
companies = []


def open_dictionary():
    word=[]
    sentScore=[]
    try:
        with open('AFINN/AFINN-111.txt', 'r') as in_file:
            for line in in_file.readlines():
                # word and values are separated by a tab
                word.append(line.split('\t')[0]) 
                sentScore.append(line.split('\t')[1].split('\n')[0])
            
            return dict(zip(word, sentScore))
    except IOError:
        print "ERROR: CAN NOT FIND THE FILE"
        return


def normalize_text(text):
    """
    Normalize the text
    tokenize, remove stopwords, and lemmatize
    >>> normalize_text('the carrots are orange')
    ['carrot', 'orange']
    """
    # put the text in words
    tokenized_text = word_tokenize(text)
    # remove stopwords
    no_stopwords_text = [
        w for w in tokenized_text if w.lower() not in stopwords
    ]
    # lemmatize
    lemmatized_text = [
        WordNetLemmatizer().lemmatize(t) for t in no_stopwords_text
    ]

    return lemmatized_text


def sentiment(words, sentiment_dictionary):
    """
    Evaluate the average sentiment of a list of words
    >>> sentiment(['kill', 'cry'], open_dictionary())
    -2.0
    """
    count = 0
    sentiment_value = 0
    average_sentiment = 0
    for word in words:
        # check if word appears in the dictionary
        for key in sentiment_dictionary:
            # count the number of words and sum their sentiment
            if word.lower() == key:
                count += 1
                sentiment_value += float(sentiment_dictionary[key])
            if count > 0:
                # if there is at least one word,
                # calculate the average sentiment
                # dividing the sum by the number of words
                average_sentiment = sentiment_value/count

    return average_sentiment


def company_sentiment(company):
    """
    Evaluate the average sentiment of a company from its wikipedia page
    """
    # load the page and extract content
    page = wikipedia.page(company)
    text = page.content

    # load the dictionary
    sentiment_dictionary = open_dictionary()

    # normalize the text
    normalized_text = normalize_text(text)

    # calculate the average sentiment
    average_sentiment.append(sentiment(normalized_text, sentiment_dictionary))

    # stock the companies
    companies.append(company)

    return average_sentiment


def load_companies_list():    
    """
    return the list of the multinational companies on wikipedia
    """
    page = wikipedia.page('List_of_multinational_corporations')
    companies_list = page.links

    return companies_list


def reinitialize():
    """
    Put the data collected to empty list,
    if you want to start another comparison
    """
    global average_sentiment
    average_sentiment = []

    global companies
    companies = []

if __name__ == "__main__":
    import doctest
    doctest.testmod()
