import json

from rest_framework import status
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from SPARQLWrapper import SPARQLWrapper, JSON


@api_view(['GET'])
def search_query(request):
    if request.method == 'GET':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        query = body['query']

        print(query)
        print("""
            SELECT DISTINCT ?CarID
            WHERE {
            ?CarID :hasMachinetype [:hasModel <http://saya-akan-datang.org/%s>] .
            }
            LIMIT 50
        """ % query)

        sparql = SPARQLWrapper("http://localhost:7200/repositories/CarPriceDB")
        sparql.setQuery("""
            PREFIX : <http://saya-akan-datang.org/data#>
            SELECT DISTINCT ?CarID
            WHERE {
            ?CarID :hasMachinetype [:hasModel <http://saya-akan-datang.org/%s>] .
            }
            LIMIT 50
        """ % query)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return JsonResponse(results, safe=False)

    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
