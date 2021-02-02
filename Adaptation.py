# -*- coding: utf-8 -*-

import pandas  as pd
from es_pandas import es_pandas
from elasticsearch import Elasticsearch
from operator import itemgetter
from itertools import groupby
from time import sleep
import  re,csv,json


## Get All Marques
marques = []
with open('g8data.csv','r') as readfile :
    rd = csv.reader(readfile,delimiter =',')
    next(rd, None)  # skip the headers
    for row in rd:
        marque = (row[8])
        # Verify if marque already in marques liste && marque is not null
        if marque is not None and marque not in marques:
            marques.append(marque)

es = Elasticsearch()
# Gathers all results matching list :
dataList = []
def eplore_data():
    with open('prductsNamesMarques.csv', 'r') as readfile:
        rd = csv.reader(readfile, delimiter=',')
        for lrow in rd:
            for row in lrow:
                try:
                    print("Searching Row in Website File > " + row)
                    #row = row[1]
                    words = re.split('[\' .,()_-]', row)
                    print("Before Transofrmation > " + str(words))
                    words = [x.upper() for x in words]
                    #del words[0]
                    for word in words:
                        if word == "" or word == "CASQUE":
                            print(word)
                            del words[words.index(word)]
                    word = ('* OR *'.join(words))
                    word = "*" + word + "*"
                    print("After Transofrmation > " + str(words))

                    # res = es.search(index="dafy", body={"size":"10000","query": {"match_all": {}}})
                    print(word)
                    res = es.search(index="dafy", body={"size": "10000",
                                                        "query": {"query_string": {"default_field": "Désignation", "query": word}}})

                    print("Got %d Hits:" % res['hits']['total']['value'])
                    listItems = []
                    for hit in res['hits']['hits']:
                        result = hit["_source"]["Désignation"]
                        #print("result" + result)
                        count = 0
                        ## Test
                        flagWeb = False
                        flagElasticsearch = False
                        for marque in marques:
                            if marque in words:
                                #print("Marque Web " + marque)
                                marqueWeb = marque
                                flagWeb = True
                                break
                        marqueG8 = (hit["_source"]["Marque"])

                        """
                        for marque in marques:
                            if marque in result:
                                print("Marque G8 " + marque)
                                flagElasticsearch = True
                                marqueElastic = marque
                                break
                        """
                        #if marqueWeb == marqueG8:
                        #    print("Marque Web : " + marqueWeb)
                        #    print("Marque G8  : " + marqueG8)
    #                    if flagElasticsearch and  flagWeb and marqueElastic != marqueWeb:
                        #if flagWeb and marqueWeb != marqueG8:
                        #        x =1
                        if flagWeb and marqueWeb == marqueG8:
                            for w in words:
                                if w in result:
                                    count += 1
                                listItems.append([result, word, count])
                    # (listItems.sort(key=lambda x: x[2], reverse=True))
                    #print(json.dumps(listItems))
    #                if int(res['hits']['total']['value']) > 0:
                    print("List Items Length : " + str(len(listItems)))
                    if int(len(listItems)) > 0:
                        listItems.sort(key=itemgetter(2), reverse=True)
                        groups = groupby(listItems, itemgetter(2))
                        glo = [[item[0] for item in data] for (key, data) in groups]
                        print("FNAL DATA : ")
                        print(glo[0])

                        matching = {"web-product": row, "matchin-results": glo[0]}
                        dataList.append([matching])
                except Exception as e:
                    print("Exception : > " + str(e))
                #input("")
                print(dataList)
def indexation():
    #df = pd.DataFrame({'items':listElastics})
    df = pd.read_excel("g8data.xlsx", engine='openpyxl')
    es_host= 'http://localhost:9200'
    index = 'dafy'
    ## init template if you want
    doc_type = 'dafy'
    ep = es_pandas(es_host)
    ep.init_es_tmpl(df, doc_type)
    ep.to_es(df, index, doc_type=doc_type, use_index=True, thread_count=2, chunk_size=10000)

eplore_data()
#print(marques)
print(dataList)
with open('finalData.json', 'w') as f:
    json.dump(dataList, f)