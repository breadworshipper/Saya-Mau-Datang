import json

from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from SPARQLWrapper import SPARQLWrapper, JSON
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['GET'])
def search_query_by_model(request):
    if request.method == 'GET':
        params = QueryDict(request.META['QUERY_STRING'])
        query = params.get('query', '')
        page = params.get('page', 1)
        page = int(page)
        page = (page - 1) * 20
        page = str(page)

        sparql = SPARQLWrapper("http://localhost:7200/repositories/CarPriceDB")
        # Query berdasarkan model
        sparql.setQuery("""
                    PREFIX : <http://saya-akan-datang.org/data#>
                    SELECT DISTINCT ?CarID ?price ?currency
                    WHERE {
                    ?CarID :hasMachinetype [:hasModel ?model] .
                    ?CarID :Price [
                        :amount ?price;
                        :currency ?currency
                    ] .
                    FILTER regex(str(?model), "%s", "i")
                    }
                    LIMIT 20
                    OFFSET %s
                """ % (query, page))

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return JsonResponse(results, safe=False)

    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
def search_query_by_category(request):
    if request.method == 'GET':
        params = QueryDict(request.META['QUERY_STRING'])
        query = params.get('query', '')
        page = params.get('page', 1)
        page = int(page)
        page = (page - 1) * 20
        page = str(page)

        sparql = SPARQLWrapper("http://localhost:7200/repositories/CarPriceDB")
        # Query berdasarkan model
        sparql.setQuery("""
                    PREFIX : <http://saya-akan-datang.org/data#>
                    SELECT DISTINCT ?CarID ?price ?currency
                    WHERE {
                    ?CarID :hasMachinetype [:hasCarCategory ?category] .
                    ?CarID :Price [
                        :amount ?price;
                        :currency ?currency
                    ] .
                    FILTER regex(str(?category), "%s", "i")
                    }
                    LIMIT 20
                    OFFSET %s
                """ % (query, page))

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return JsonResponse(results, safe=False)

    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
def search_query_by_manufacturer(request):
    if request.method == 'GET':
        params = QueryDict(request.META['QUERY_STRING'])
        query = params.get('query', '')
        page = params.get('page', 1)
        page = int(page)
        page = (page - 1) * 20
        page = str(page)

        sparql = SPARQLWrapper("http://localhost:7200/repositories/CarPriceDB")

        sparql.setQuery("""
        PREFIX : <http://saya-akan-datang.org/data#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX bd: <http://www.bigdata.com/rdf#>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>                        

        SELECT DISTINCT ?manufacturer ?manufacturerLabel
WHERE {
        {
    SELECT DISTINCT ?manufacturer
    WHERE {
      ?CarID :hasMachinetype [:hasManufacturer ?manufacturer] .
    }
        }
        # Optional: Query Wikidata for English labels
   SERVICE <https://query.wikidata.org/sparql> { 
     SERVICE wikibase:label {
       bd:serviceParam wikibase:language "en" .
     }    
     ?manufacturer rdfs:label ?manufacturerLabel
     FILTER(lang(?manufacturerLabel) = "en" && regex(str(?manufacturerLabel), "%s", "i"))
   }
  }
""" % query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        manufacturer_info = results['results']['bindings'][0]
        manufacturer_uri = manufacturer_info['manufacturer']['value']
        manufacturer_label = manufacturer_info['manufacturerLabel']['value']

        manufacturer_id = manufacturer_uri.split("/")[-1]
        print(manufacturer_id)

        print(manufacturer_label, manufacturer_uri)

        sparql.setQuery("""
        PREFIX : <http://saya-akan-datang.org/data#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX bd: <http://www.bigdata.com/rdf#>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>


        SELECT DISTINCT ?CarID ?price ?currency ?manufacturer ?manufacturerLabel
            WHERE {
            ?CarID :hasMachinetype [:hasManufacturer ?manufacturer] .
            ?CarID :Price [
                :amount ?price;
                :currency ?currency
            ] .
            FILTER(?manufacturer = wd:%s)
            BIND(str("%s") AS ?manufacturerLabel)
            } 
        LIMIT 20
        OFFSET %s
        """ % (manufacturer_id, manufacturer_label, page))

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return JsonResponse(results, safe=False)

    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
def search_query_by_price_range(request):
    if request.method == 'GET':
        params = QueryDict(request.META['QUERY_STRING'])
        min_price = params.get('min', '0')
        max_price = params.get('max', '999999999')
        page = params.get('page', 1)
        page = int(page)
        page = (page - 1) * 20
        page = str(page)

        sparql = SPARQLWrapper("http://localhost:7200/repositories/CarPriceDB")
        # Query berdasarkan model
        sparql.setQuery("""
                    PREFIX : <http://saya-akan-datang.org/data#>
                    SELECT DISTINCT ?CarID ?price ?currency
                    WHERE {
                    ?CarID :Price [
                        :amount ?price;
                        :currency ?currency
                    ] .
                    FILTER (?price >= %s && ?price <= %s)
                    }
                    LIMIT 20
                    OFFSET %s
                """ % (min_price, max_price, page))

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return JsonResponse(results, safe=False)

    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
def get_detail_by_id(request, car_id):
    if request.method == 'GET':
        sparql = SPARQLWrapper("http://localhost:7200/repositories/CarPriceDB")
        # Query berdasarkan Manufacturer
        sparql.setQuery("""
                    PREFIX : <http://saya-akan-datang.org/data#>

                    SELECT DISTINCT ?CarID ?price ?currency ?Cylinders ?Doors ?engineVolumeAmount ?isEngineTurbo ?engineUnit ?isLeatherInterior ?levyAmount ?levyCurrency ?mileageAmount ?mileageUnit ?prodYear ?airbagsAmount ?color ?driveWheels ?fuelType ?gearBoxType ?carCategory ?carManufacturer ?carModel ?wheel
                    WHERE {
                      ?CarID
                        :Cylinders         ?Cylinders ;
                        :Doors             ?Doors ;
                        :Engine_volume     [ :amount   ?engineVolumeAmount ;
                                             :isTurbo  ?isEngineTurbo ;
                                             :unit    ?engineUnit
                                           ] ;
                        :Leather_interior  ?isLeatherInterior ;
                        :Mileage           [ :amount  ?mileageAmount ;
                                             :unit    ?mileageUnit
                                           ] ;
                         :Price            [ :amount    ?price ;
                                             :currency  ?currency
                                           ] ;
                        :Prod._year        ?prodYear ;
                        :airbagsAmount     ?airbagsAmount ;
                        :hasColor          ?color ;
                        :hasDriveWheels    ?driveWheels ;
                        :hasFuelType       ?fuelType ;
                        :hasGearBoxType    ?gearBoxType ;
                        :hasMachinetype    [ :hasCarCategory   ?carCategory ;
                                             :hasManufacturer  ?carManufacturer ;
                                             :hasModel         ?carModel
                                           ] ;
                        :hasWheel          ?wheel .
                        OPTIONAL {
                          ?CarID :Levy [ :amount    ?levyAmount ;
                                         :currency  ?levyCurrency
                                       ] ;
                        }
                      FILTER regex(str(?CarID), "%s", "i")
                    }
                    """ % car_id)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        manufacturer_info = results['results']['bindings'][0]
        manufacturer_uri = manufacturer_info['carManufacturer']['value']
        manufacturer_id = manufacturer_uri.split("/")[-1]
        sparql.setQuery("""
        PREFIX : <http://saya-akan-datang.org/data#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX bd: <http://www.bigdata.com/rdf#>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>


        SELECT DISTINCT ?manufacturerLabel
        WHERE {
                # Optional: Query Wikidata for English labels
        SERVICE <https://query.wikidata.org/sparql> { 
            SERVICE wikibase:label {
            bd:serviceParam wikibase:language "en" .
            }    
            wd:%s rdfs:label ?manufacturerLabel
        }
            FILTER(lang(?manufacturerLabel) = "en")
        }
        LIMIT 1
        """ % (manufacturer_id))

        sparql.setReturnFormat(JSON)
        manufacturer_label_result = sparql.query().convert()

        manufacturer_label = manufacturer_label_result['results']['bindings'][0]['manufacturerLabel']['value']

        manufacturer_info["manufacturerLabel"] = {
                    "type": "literal",
                    "value": manufacturer_label
                }
        

        return JsonResponse(results, safe=False)
    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
