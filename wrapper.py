__author__ = 'croman'
# -*- coding: utf-8 -*-


import subprocess
import rdflib
import codecs

import ritter_ner
import stanford_ner
import validator
import resultstonif

def nif(niffile, ner='ritter'):

    if ner == 'ritter':
        results = ritter_ner.ner(niffile+'.ttl', "nif")
    elif ner == 'stanford':
        results = stanford_ner.ner(niffile+'.ttl', "nif")
        print results
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

#print 'Brian: \n'+score('Brian Collection')
#print '\nMena: \n'+score('Mena Collection')
#print '\nMicroposts2014: \n'+score('Microposts2014_Collection_train')

#print 'Brian: \n'+nif('Mena Collection')
print nif('Brian Collection', 'stanford')