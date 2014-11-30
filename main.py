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
import general_functions as ge

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
    branches_list = db.get_branch(text)
    company_name_list.append(text)
    
    #parsing and converting the employees list taken from dbpedia
    employees_int_list = ge.convert_into_integer(employees_list)

    correlation_sent_empl = ge.correlate(sentiment_list, employees_int_list)
    correlation_sent_rev = ge.correlate(sentiment_list, revenues_list)
    correlation_sent_empl_rev = ge.triple_correlate(sentiment_list, employees_int_list, revenues_list)

    #scatter plot
    graph_relation_sent_rev = ge.scatter_plot(sentiment_list, revenues_list)


    return render_template(
        "my-form.html", sentiments=sentiment_list,
        revenues=revenues_list, foundingYears=foundingYears_list,
        foundationPlaces=foundationPlaces_list,
        employees=employees_list, company_names=company_name_list, 
        branches=branches_list, sent_empl_mx=correlation_sent_empl, 
        sent_rev_mx=correlation_sent_rev, 
        sent_empl_rev_mx=correlation_sent_empl_rev, 
        plot_sent_rev=graph_relation_sent_rev
    )


if __name__ == '__main__':
    app.run(debug=True)
