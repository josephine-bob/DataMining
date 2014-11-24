from SPARQLWrapper import SPARQLWrapper, JSON

sentiment_list = []
revenues_list = []
employees_list = []
foundingYears_list = []
foundationPlaces_list = []


def get_employees(company):
    
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


def get_revenue(company):
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
        revenues_list.append(result["label"]["value"])
    
    return revenues_list


def get_foundingYear(company):
    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE { 
        <http://dbpedia.org/resource/"""+company+"""> dbpedia-owl:foundingYear ?label .
        }"""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        foundingYear = result["label"]["value"]
        foundingYear = foundingYear[:-12]
        foundingYears_list.append(foundingYear)
    
    return foundingYears_list


def get_foundationPlace(company):
    
    query_string = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE { 
        <http://dbpedia.org/resource/"""+company+"""> dbpedia-owl:foundationPlace ?label .
        }"""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        place = result["label"]["value"]
        place = place[28:]
        foundationPlaces_list.append(place)
    return foundationPlaces_list


def empty_lists():
    global sentiment_list
    global revenues_list
    global foundationPlaces_list
    global foundingYears_list
    sentiment_list = []
    revenues_list = []
    foundingYears_list = []
    foundationPlaces_list = []
