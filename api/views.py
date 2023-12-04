import json

from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from SPARQLWrapper import SPARQLWrapper, JSON


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
        # Query berdasarkan Manufacturer
        sparql.setQuery("""
                    PREFIX : <http://saya-akan-datang.org/data#>
                    SELECT DISTINCT ?CarID ?price ?currency
                    WHERE {
                    ?CarID :hasMachinetype [:hasManufacturer ?manufacturer] .
                    ?CarID :Price [
                        :amount ?price;
                        :currency ?currency
                    ] .
                    FILTER regex(str(?manufacturer), "%s", "i")
                    }
                    LIMIT 20
                    OFFSET %s
                """ % (query, page))

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return JsonResponse(results, safe=False)

    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

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

        return JsonResponse(results, safe=False)
    return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
