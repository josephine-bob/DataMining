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


def get_employees(comp):
    """
    Extract employees information
    """
    company = comp.replace (" ", "_")
    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {
        <http://dbpedia.org/resource/"""+company+"""> dbpedia-owl:numberOfEmployees ?label .
        }"""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        employees_list.append(result["label"]["value"])

    return employees_list


def get_revenue(comp):
    """
    Extract revenue information
    """
    company = comp.replace (" ", "_")
    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {
        <http://dbpedia.org/resource/"""+company+"""> dbpedia-owl:revenue ?label .
        }"""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        #revenue values in DBPEDIA are like 0.478E10, so I convert them into float
        converted_value = '{0:.2f}'.format(float(result["label"]["value"]))
        revenues_list.append(converted_value)

    return revenues_list


def get_branch(comp):
    """
    Extract industry information
    """
    company = comp.replace (" ", "_")
    #I create a sublist because each company could belong to different branches
    sublist = []

    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {
        <http://dbpedia.org/resource/"""+company+"""> dbpedia-owl:industry ?label .
        }"""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        temp_value = str(result["label"]["value"])
        #slicing the string to extract just the relevant information
        final_value = temp_value[28:]
        sublist.append(final_value)
    
    branch_list.append(sublist)

    return branch_list


def empty_lists():
    """
    Reinitialize all the data to start another study
    """
    global sentiment_list
    global revenues_list
    global foundationPlaces_list
    global foundingYears_list
    sentiment_list = []
    revenues_list = []
    foundingYears_list = []
    foundationPlaces_list = []


if __name__ == "__main__":
    import doctest
    doctest.testmod()
