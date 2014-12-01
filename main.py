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

option_list = wiki_fun.load_companies_list()

company_name_list = []

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("my-form.html", option_list=option_list)

@app.route('/', methods=['POST'])
def my_form_post():

    comp = request.form['option']

    sentiment_list = wiki_fun.company_sentiment(comp)
    revenues_list = db.get_revenue(comp)
    employees_list = db.get_employees(comp)
    branches_list = db.get_branch(comp)
    company_name_list.append(comp)
    
    # parsing and converting the employees list taken from dbpedia
    employees_int_list = ge.convert_into_integer(employees_list)

    # correlation between employees, revenue, and sentiment
    correlation_sent_empl_rev = ge.triple_correlate(
        sentiment_list,
        employees_int_list,
        revenues_list
    )

    # scatter plot
    graph_relation_sent_rev = ge.scatter_plot(revenues_list, sentiment_list)
    
    return render_template(
        "my-form.html", option_list=option_list,
        sentiments=sentiment_list,
        revenues=revenues_list,
        employees=employees_list, company_names=company_name_list, 
        branches=branches_list, 
        sent_empl_rev_mx=correlation_sent_empl_rev, 
        plot_sent_rev=graph_relation_sent_rev
    )


if __name__ == '__main__':
    app.run(debug=True)
