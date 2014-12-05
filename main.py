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

# variables for the analysis
company_name_list = []
sentiment_list = []
revenues_list = []
employees_list = []
branches_list = []
correlation_sent_empl_rev = []
graph_relation_sent_rev = []

# variables if there is not enough information
company_name_list_bis = []
sentiment_list_bis = []

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template("my-form.html", option_list=option_list)


@app.route('/', methods=['POST'])
def my_form_post():

    global sentiment_list
    global sentiment_list_bis
    global revenues_list
    global employees_list
    global branches_list
    global company_name_list
    global company_name_list_bis
    global error_message
    global graph_relation_sent_rev
    global correlation_sent_empl_rev

    comp = request.form['option']

    # saving the former revenue list
    revenues_temp = []
    revenues_temp = list(revenues_list)

    # trying to extract information
    revenues_list = db.get_revenue(comp)

    # if no revenue information is added we compute only the sentiment
    if (len(revenues_list) == 0):
        sentiment_list_bis.append(wiki_fun.company_sentiment(comp))
        company_name_list_bis.append(comp)

        return render_template(
            "my-form.html", option_list=option_list,

        )

    elif(revenues_temp == revenues_list):
        sentiment_list_bis.append(wiki_fun.company_sentiment(comp))
        company_name_list_bis.append(comp)

        return render_template(
            "my-form.html", option_list=option_list,
            sentiments=sentiment_list,
            sentiments_bis=sentiment_list_bis,
            revenues=revenues_list,
            employees=employees_list,
            company_names=company_name_list,
            company_names_bis=company_name_list_bis,
            branches=branches_list,
            sent_empl_rev_mx=correlation_sent_empl_rev,
            plot_sent_rev=graph_relation_sent_rev
        )

    else:
        sentiment_list.append(wiki_fun.company_sentiment(comp))
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
        graph_relation_sent_rev = ge.scatter_plot(
            revenues_list, sentiment_list
        )

        return render_template(
            "my-form.html", option_list=option_list,
            sentiments=sentiment_list,
            sentiments_bis=sentiment_list_bis,
            revenues=revenues_list,
            employees=employees_list,
            company_names=company_name_list,
            company_names_bis=company_name_list_bis,
            branches=branches_list,
            sent_empl_rev_mx=correlation_sent_empl_rev,
            plot_sent_rev=graph_relation_sent_rev
        )


if __name__ == '__main__':
    app.run(debug=True)
