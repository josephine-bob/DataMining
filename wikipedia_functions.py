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
    """
    Put words and their sentiment into a dictionary
    From the AFINN-111 word list
    """
    words = []
    sentiment_words = []
    with open('AFINN/AFINN-111.txt', 'r') as in_file:
        for line in in_file.readlines():
            # word and values are separated by a tab
            words.append(line.split('\t')[0])
            sentiment_words.append(line.split('\t')[1].split('\n')[0])

    return dict(zip(words, sentiment_words))


def normalize_text(text):
    """
    Normalize the text
    tokenize, remove stopwords, and lemmatize
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


def reinitialize():
    """
    Put the data collected to empty list,
    if you want to start another comparison
    """
    global average_sentiment
    average_sentiment = []

    global companies
    companies = []
