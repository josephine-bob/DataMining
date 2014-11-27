# -*- coding: utf-8 -*-
"""
Main code of the application
using flask
enables the user to see companies information an plots
"""

from flask import Flask
from flask import request
from flask import render_template
import wikipedia_functions as wiki_fun
import dbpedia_functions as db

company_name_list = []

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template("my-form.html")


@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']

    sentiment_list = wiki_fun.company_sentiment(text)
    revenues_list = db.get_revenue(text)
    foundingYears_list = db.get_foundingYear(text)
    foundationPlaces_list = db.get_foundationPlace(text)
    employees_list = db.get_employees(text)
    company_name_list.append(text)

    return render_template(
        "my-form.html", sentiments=sentiment_list,
        revenues=revenues_list, foundingYears=foundingYears_list,
        foundationPlaces=foundationPlaces_list,
        employees=employees_list, company_names=company_name_list
    )


if __name__ == '__main__':
    app.run(debug=True)
