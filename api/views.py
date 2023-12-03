from django.shortcuts import render

# from SPARQLWrapper import SPARQLWrapper, JSON
#
# sparql = SPARQLWrapper("http://localhost:7200/repositories/CarPriceDB")
# sparql.setQuery("""
#     SELECT ?s ?o
#     WHERE {
#         ?s ?p ?o .
#     } limit 50
# """)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
#
# for result in results["results"]["bindings"]:
#     print(result["s"]['value'], result["o"]['value'])
# Create your views here.
