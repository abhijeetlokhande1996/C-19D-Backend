from django.shortcuts import render
from django.http import JsonResponse
import requests
import csv
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
import os
# Create your views here.
CWD = os.getcwd()


def index(request):
    return JsonResponse({"name": "Abhijeet"})


@csrf_exempt
def getCountryRegionMapping(request):
    responseDict = defaultdict(list)
    try:
        with open('country-region-mapping.csv', 'r') as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                if idx == 0:
                    continue
                regionName = row[5]
                if not regionName:
                    continue
                countryName = row[0]
                try:
                    responseDict[regionName].append(countryName)
                except KeyError:
                    responseDict[regionName] = []
    except Exception as e:
        print(e)
    finally:
        pass
    return JsonResponse(responseDict)


@csrf_exempt
def getAggregatedCsv(request):
    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    response = requests.get(url)
    csvLines: list = []
    for line in response.iter_lines():
        csvLines.append(line.decode('utf-8').split(','))
    # 0 -Date
    # 1 - Country
    # 2 - Confirmed
    # 3 - Recovered
    # 4 - Deaths
    responseDict = defaultdict()
    for idx, item in enumerate(csvLines):
        if (len(item) == 6):
            item[1] = item[1] + item[2]
            del item[2]
        if(idx == 0):
            continue

        try:
            countryName = item[1]
            confirmedCases = int(item[2])
            recoveredCases = int(item[3])
            deaths = int(item[4])
        except IndexError:
            continue

        try:
            responseDict[countryName]["confirmed"] = confirmedCases
            responseDict[countryName]["recovered"] = recoveredCases
            responseDict[countryName]["deaths"] = deaths

        except KeyError:
            responseDict[countryName] = {}
            responseDict[countryName]["confirmed"] = 0
            responseDict[countryName]["recovered"] = 0
            responseDict[countryName]["deaths"] = 0

    return JsonResponse(responseDict)
