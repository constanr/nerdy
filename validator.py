#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'croman'

import sys
import os
import codecs
import rdflib


def validate(goldenset, results):

    with codecs.open(goldenset, 'rb', encoding='utf-8') as goldensetfile, codecs.open(results, 'rb', encoding='utf-8') as resultsfile:
        a = rdflib.Graph()
        a.parse(goldensetfile, format='n3')
        r = rdflib.Graph()
        r.parse(resultsfile, format='n3')

        tweets = {}
        offsets = {}
        multiword = {}

        #Se extraen los tweets
        for s, p, o in a:

            if s.endswith(',') and p.endswith('isString'):
                id = s.split('#')[0]
                tweets[id] = o

        #Se extraen las entidades multipalabra
        for s, p, o in a:
            if p.endswith('anchorOf'):
                id = s.split('#')[0]
                offsets[s] = o
                for offset in offsets.keys():
                    startoffset1 = int(s.split('#char=')[1].split(',')[0])
                    endoffset1 = int(s.split('#char=')[1].split(',')[1])
                    startoffset2 = int(offset.split('#char=')[1].split(',')[0])
                    endoffset2 = int(offset.split('#char=')[1].split(',')[1])

                    if id == offset.split('#')[0] and startoffset1 != startoffset2 and abs(endoffset1-startoffset2)<5:
                        if tweets[id][min(endoffset1,startoffset2):max(endoffset1,startoffset2)] == ' of ':
                            if not multiword.has_key(id):
                                multiword[id] = []
                            #print tweets[id][min(startoffset1,startoffset2):max(endoffset1,endoffset2)]
                            multiword[id].append(tweets[id][min(startoffset1,startoffset2):max(endoffset1,endoffset2)])
                        elif tweets[id][min(endoffset1,startoffset2):max(endoffset1,startoffset2)] == '/':
                            if not multiword.has_key(id):
                                multiword[id] = []
                            #print tweets[id][min(startoffset1,startoffset2):max(endoffset1,endoffset2)]
                            multiword[id].append(tweets[id][min(startoffset1,startoffset2):max(endoffset1,endoffset2)])

        """for m in multiword:
                print m, multiword[m]"""

        #Calcula la precisión del sistema
        def precision():

            fullmentions = 0
            totalmentions = 0
            partialmentions = 0
            annotatedmentions = {}



            #Extrae las menciones anotadas en el golden set.
            for s, p, o in a:
                if p.endswith('anchorOf'):
                    id = s.split('#')[0]
                    if not annotatedmentions.has_key(id):
                        annotatedmentions[id] = []
                    annotatedmentions[id].append(o)

            #Compara las menciones que obtiene el sistema con las anotadas en el golden set
            for s, p, o in r:

                if p.endswith('anchorOf'):
                    id = s.split('#')[0]

                    if id in annotatedmentions.keys():
                        #Comprueba las menciones que coinciden completamente
                        if o in annotatedmentions[id]:
                            fullmentions += 1
                        else:
                            scored = False
                            for m in annotatedmentions[id]:
                                #Comprueba las menciones que coinciden parcialmente.
                                if o in m:
                                    partialmentions += 1
                                    scored = True
                                    break
                            #Comprueba las menciones formadas por varias entidades del golden set.
                            if scored==False and multiword.has_key(id):
                                #print multiword[id]
                                for multientity in multiword[id]:
                                    #print multientity, o
                                    if multientity in o:
                                        partialmentions += 1
                                        #print id,",",multientity,",", o

                    totalmentions += 1
            score = float(fullmentions)/float(totalmentions)
            partialscore = float(fullmentions+partialmentions)/float(totalmentions)
            #print "Full Mentions Precision: ",fullmentions, totalmentions, score
            #print "Full+Partial Mentions Precision: ",fullmentions+partialmentions, totalmentions, partialscore
            return score, partialscore


        def recall():
            totalmentions = 0
            fullmentions = 0
            partialmentions = 0
            resultmentions = {}

            #Extrae las menciones obtenidas por el sistema.
            for s, p, o in r:

                if p.endswith('anchorOf'):
                    id = s.split('#')[0]
                    if not resultmentions.has_key(id):
                        resultmentions[id] = []
                    resultmentions[id].append(o)

            #Compara las menciones que obtiene el sistema con las anotadas en el golden set
            for s, p, o in a:

                if p.endswith('anchorOf'):
                    id = s.split('#')[0]
                    #Comprueba las menciones que coinciden completamente
                    if id in resultmentions.keys() and o in resultmentions[id]:
                        fullmentions += 1
                    elif id in resultmentions.keys():
                        scored = False
                        for m in resultmentions[id]:
                        #Comprueba las menciones que coinciden parcialmente
                            if m in o:
                               partialmentions += 1
                               scored = True
                               break
                        #Comprueba las menciones formadas por varias entidades del golden set.
                        if scored==False and multiword.has_key(id):
                            #print multiword[id]
                            for multientity in multiword[id]:
                                #print multientity, o
                                if multientity in o:
                                    partialmentions += 1
                                    #print id,",",multientity,",", o


                    totalmentions += 1
            score = float(fullmentions)/float(totalmentions)
            partialscore = float(fullmentions+partialmentions)/float(totalmentions)
            #print "Full Mentions Recall: ",fullmentions, totalmentions, score
            #print "Full+Partial Mentions Recall: ",fullmentions+partialmentions, totalmentions, partialscore
            return score,partialscore



        def f1():
            fullprec, partialprec = precision()
            fullrec, partialrec = recall()
            results = "Full Mentions Precision: "+str(fullprec)+"\nFull+Partial Mentions Precision: "+str(partialprec)
            results += "\nFull Mentions Recall: "+str(fullrec)+"\nFull+Partial Mentions Recall: "+str(partialrec)
            finalresults = "\nFull Mentions F1: "+str(2*fullprec*fullrec/(fullprec+fullrec))+"\nFull+Partial Mentions F1: "+str(2*partialprec*partialrec/(partialprec+partialrec))
            return results+finalresults

    return f1()