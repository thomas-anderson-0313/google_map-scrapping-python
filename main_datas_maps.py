# -*- coding: utf-8 -*-


from exportDatas import ExportDataMaps
from maps_data_scraper import GoogleMapsDataScraper
from threading import Thread
import sys
import os


def split_list(a, n):
    k, m = divmod(len(a), n)
    return list((a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)))


def scrapearMaps(language, list, outputFolder, results, thread):
    scraper = GoogleMapsDataScraper(language, outputFolder)
    scraper.initDriver()
    listPlaces = []

    cont = 1
    for l in list:
        place = scraper.scraperDatas(l)

        if (place != None):
            print('Output nº '+str(thread)+' ' + str(cont) +
                  '/' + str(len(list)) + ' - OK - ' + l)
            listPlaces = place
        else:
            print('Output nº '+str(thread)+' ' + str(cont) +
                  '/' + str(len(list)) + ' - ERROR - ' + l)
        cont += 1

    results[thread] = listPlaces


def mainGoogleMaps(language, fileKw, outputFolder):
    file = open(fileKw, 'r', encoding='utf-8')
    listF = file.read().splitlines()
    file.close()

    threads = 5
    listThreads = [None] * threads
    listResults = [None] * threads
    divided = split_list(listF, threads)

    for i in range(len(listThreads)):
        listThreads[i] = Thread(target=scrapearMaps, args=(
            language, divided[i], outputFolder, listResults, i,))
        listThreads[i].start()

    for i in range(len(listThreads)):
        listThreads[i].join()

    listFinal = []

    for i in range(len(listResults)):
        listFinal = listFinal + listResults[i]

    export = ExportDataMaps(outputFolder+'00_output.xls', '', listFinal)
    export.exportExcel()


if __name__ == "__main__":
    language = "EN"
    kwPlace = "./keywords.txt"
    file = "./outputs/"

    mainGoogleMaps(language, kwPlace, file)
