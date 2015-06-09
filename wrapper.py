__author__ = 'croman'
# -*- coding: utf-8 -*-


import codecs

import ritter_ner
import stanford_ner
import validator
import resultstonif
import polyglot_ner

from sklearn.cross_validation import cross_val_score
from sklearn.datasets import load_iris
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


def nif(niffile, ner='polyglot'):

    if ner == 'ritter':
        results = ritter_ner.ner(niffile+'.ttl', "nif")
    elif ner == 'stanford-en':
        results = stanford_ner.ner(niffile+'.ttl', "nif", 'english')
        print results
    elif ner == 'stanford-es':
        results = stanford_ner.ner(niffile+'.ttl', "nif", 'spanish')
        print results
    elif ner == 'polyglot':
        results = polyglot_ner.ner(niffile+'.ttl', 'nif')
    print "NER completado"

    nifresult = resultstonif.convert(results, niffile+'.xml')
    print "Conversión a NIF completada"

    return nifresult


def score(corpus, ner='stanford-en'):

    if ner == 'ritter':
        results = ritter_ner.ner(corpus+'.xml', "xml")
        print "NER completado"
    elif ner == 'stanford-en':
        results = stanford_ner.ner(corpus+'.ttl', "nif", 'english')
        print "NER completado"
    elif ner == 'stanford-es':
        results = stanford_ner.ner(corpus+'.ttl', "nif", 'spanish')
        print "NER completado"
    elif ner == 'polyglot':
        results = polyglot_ner.ner(corpus+'.ttl', 'nif')
        print "NER completado"
    elif ner == 'voting':
        results = voting(corpus)
        print "NER completado"

    nifresults = resultstonif.convert(results, corpus+'.xml')
    print "Conversión a NIF completada"
    #print nifresults

    resultspath = corpus+'-results.ttl'
    with codecs.open(resultspath, 'wb', encoding='utf-8') as resultsfile:
        resultsfile.write(nifresults)
    print "NIF guardado"

    scores = validator.validate(corpus+'.ttl', resultspath)
    print "Validación completada"

    return scores

def adaboost(corpus):
    vectorizer = TfidfVectorizer()
    #vectors = vectorizer.fit_transform()
    iris = load_iris()
    print iris.data
    clf = AdaBoostClassifier(n_estimators=100)
    scores = cross_val_score(clf, iris.data, iris.target)
    print scores.mean()

def voting(corpus):
    ner_results = []
    ner_results.append(ritter_ner.ner(corpus+'.xml', 'xml'))
    ner_results.append(stanford_ner.ner(corpus+'.ttl', 'nif', 'english'))
    ner_results.append(polyglot_ner.ner(corpus+'.ttl', 'nif', 'en'))
    #Ordenar por ids?

    for ner in ner_results:
        #print ner.splitlines()
        print len(ner.splitlines())

    voting_results = ''
    for x in range(0, len(ner_results[0].splitlines())):
        inEntity = False
        print x, len(ner_results[0].splitlines())
        print ner_results[0].splitlines()[x].split('||')[0]
        for y in range(0, len(ner_results[0].splitlines()[x].split('||')[0].split())):
            vote = 0
            print y, len(ner_results[0].splitlines()[x].split('||')[0].split())
            for z in range(0, len(ner_results)):
                print ner_results[0].splitlines()[x].split('||')[0].split()[y]
                entities = ner_results[z].splitlines()[x].split('||')[0].split()[y]
                if not entities.endswith('/O'):
                    vote += 1
            if vote > 1:
                if not inEntity:
                    vote = 'B-ENTITY'
                    inEntity = True
                else:
                    vote = 'I-ENTITY'
            else:
                vote = 'O'
                inEntity = False
            voting_results += ner_results[0].splitlines()[x].split()[y].rsplit('/', 1)[0]+'/'+vote+' '
        voting_results += '||'+ner_results[0].splitlines()[x].split('||')[1]+'\n'

    print voting_results
    return voting_results

#print 'Brian: \n'+score('Brian Collection')
#print '\nMena: \n'+score('Mena Collection')
#print '\nMicroposts2014: \n'+score('Microposts2014_Collection_train')
#print 'Test: \n'+score('testingcorpus')
#print voting('testingcorpus')
print score('testingcorpus', 'voting')

#print 'Brian: \n'+nif('Mena Collection')
#print nif('Brian Collection', 'stanford')
#print adaboost('Brian Collection')
#print nif('Mena Collection', 'polyglot')