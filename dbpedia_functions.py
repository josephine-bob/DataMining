"""
Useful functions to extract data on dbdata
"""

from SPARQLWrapper import SPARQLWrapper, JSON

sentiment_list = []
revenues_list = []
employees_list = []
foundingYears_list = []
foundationPlaces_list = []
branch_list = []


def get_employees(company):
    """
    Extract employees information
    """
    company_index = company.replace(" ", "_")
    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {
            <http://dbpedia.org/resource/"""+company_index+""">
            dbpedia-owl:numberOfEmployees ?label .
        }
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        employees_list.append(result["label"]["value"])

    return employees_list


def get_revenue(company):
    """
    Extract revenue information
    """
    company_index = company.replace(" ", "_")
    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {
            <http://dbpedia.org/resource/"""+company_index+""">
            dbpedia-owl:revenue ?label .
        }
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        # revenue values in DBPEDIA are like 0.478E10, we want float
        converted_value = '{0:.2f}'.format(float(result["label"]["value"]))
        revenues_list.append(converted_value)

    return revenues_list


def get_branch(company):
    """
    Extract industry information
    """
    company_index = company.replace(" ", "_")
    # sublist because each company could belong to different branches
    sublist = []

    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {
            <http://dbpedia.org/resource/"""+company_index+""">
            dbpedia-owl:industry ?label .
        }
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        temp_value = str(result["label"]["value"])
        # slicing the string to extract just the relevant information
        final_value = temp_value[28:]
        sublist.append(final_value)

    branch_list.append(sublist)

    return branch_list
