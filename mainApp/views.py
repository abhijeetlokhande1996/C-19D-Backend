from django.shortcuts import render
from django.http import JsonResponse
import requests
import csv
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
import os
import json
from collections import defaultdict

# Create your views here.
CWD = os.getcwd()


def index(request):
    return JsonResponse({"name": "Abhijeet"})


@csrf_exempt
def getCountryRegionMapping(request):
    responseDict = defaultdict(list)
    url = "https://restcountries.eu/rest/v2/all"
    response = requests.request("GET", url)
    for item in json.loads(response.text):
        countryName:str = item["name"]
        regionName:str = item["region"]
        if not regionName: continue
        if countryName.lower() == "united states of america":
            countryName = "USA"
        if countryName.lower() == "united kingdom of great britain and northern ireland":
            countryName = "UK"
        if not regionName in responseDict:
            responseDict[regionName]= []
        responseDict[regionName].append(countryName)

    return JsonResponse(responseDict)

    # responseDict = defaultdict(list)
    # try:
    #     with open('country-region-mapping.csv', 'r') as file:
    #         reader = csv.reader(file)
    #         for idx, row in enumerate(reader):
    #             if idx == 0:
    #                 continue
    #             regionName = row[5]
    #             if not regionName:
    #                 continue
    #             countryName = row[0]
    #             try:
    #                 responseDict[regionName].append(countryName)
    #             except KeyError:
    #                 responseDict[regionName] = []
    # except Exception as e:
    #     print(e)
    # finally:
    #     pass
    # return JsonResponse(responseDict)


@csrf_exempt
def getAggregatedCsv(request):
    responseDict = defaultdict()
    url = "https://covid-19-data.p.rapidapi.com/country/all"
    querystring = {"format":"undefined"}
    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "297c7f49b8mshbe42867157733dap15a767jsn6d9220c33424"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    for idx, item in enumerate(json.loads(response.text)):
        countryName = item["country"]
        confirmedCases = int(item["confirmed"])
        recoveredCases = int(item["recovered"])
        deaths = int(item["deaths"])
        critical = int(item["critical"])
        if not countryName in responseDict:
            responseDict[countryName] = {}

        responseDict[countryName]["confirmed"] = confirmedCases
        responseDict[countryName]["recovered"] = recoveredCases
        responseDict[countryName]["deaths"] = deaths
        responseDict[countryName]["critical"] = critical
    return JsonResponse(responseDict)
