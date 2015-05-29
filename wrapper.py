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


def nif(niffile, ner='ritter'):

    if ner == 'ritter':
        results = ritter_ner.ner(niffile+'.ttl', "nif")
    elif ner == 'stanford':
        results = stanford_ner.ner(niffile+'.ttl', "nif")
        print results
    elif ner == 'polyglot':
        results = polyglot_ner.ner(niffile+'.ttl', 'nif')
    print "NER completado"

    nifresult = resultstonif.convert(results, niffile+'.xml')
    print "Conversión a NIF completada"

    return nifresult


def score(corpus, ner='ritter'):

    if ner == 'ritter':
        results = ritter_ner.ner(corpus+'.xml', "xml")
        print "NER completado"
    elif ner == 'stanford':
        results = stanford_ner.ner(corpus+'.ttl', "nif")
        print "NER completado"
    elif ner == 'polyglot':
        results = polyglot_ner.ner(corpus+'.ttl', 'nif')
        print "NER completado"


    nifresults = resultstonif.convert(results, corpus+'.xml')
    print "Conversión a NIF completada"
    print nifresults

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

print 'Brian: \n'+score('Brian Collection')
print '\nMena: \n'+score('Mena Collection')
print '\nMicroposts2014: \n'+score('Microposts2014_Collection_train')

#print 'Brian: \n'+nif('Mena Collection')
#print nif('Brian Collection', 'stanford')
#print adaboost('Brian Collection')
#print nif('Mena Collection', 'polyglot')