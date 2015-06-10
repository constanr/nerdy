__author__ = 'croman'
# -*- coding: utf-8 -*-

import os
import subprocess
import codecs

from lxml import etree

import rdflib
import re


def ner(dataset, format):

    with codecs.open(dataset, 'rb', encoding='utf-8') as datasetfile:

        tweets = ""
        tweetids = []

        if format == "xml":

            dataset = etree.parse(datasetfile)
            for tweet in dataset.xpath('//Tweet'):
                tweetText = tweet.xpath('./TweetText/text()')[0]
                tweets += ' '.join(re.findall(r"[\w:/!#$%&*+,\-:;?@^_`{|}~.]+|[\"'().[\]<=>]", tweetText))+"\n"
                tweetids.append(tweet.xpath('./TweetId/text()')[0])

            tweets = tweets.encode('utf-8')
            #resultsfile.write(tweets)
        elif format == "nif":

            tweetdict = {}
            a = rdflib.Graph()
            a.parse(datasetfile, format='n3')

            for s, p, o in a:
                if s.endswith(',') and p.endswith('isString'):
                    id = s.split('#')[0].split('.xml/')[1]
                    tweetdict[id] = ' '.join(re.findall(r"[\w:/!#$%&*+,\-:;?@^_`{|}~.]+|[\"'().[\]<=>]", o))
                    #tweetids.append(id)

            for key in sorted(tweetdict):
                tweetids.append(key)
                tweets += tweetdict[key]+'\n'
            tweets = tweets.encode('utf-8')



        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ["TWITTER_NLP"] = "/home/croman/PycharmProjects/twitter_nlp-master/"
        ner = subprocess.Popen(['python', '/home/croman/PycharmProjects/twitter_nlp-master/python/ner/extractEntities2.py'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)


        results = ner.communicate(input=tweets)[0]

        results = results.decode('utf-8')

        lines = results.splitlines()
        idresults = ''

        for x in range(0, len(lines[:-1])):
            line = lines[x]+" ||"+tweetids[x]+"\n"
            idresults += line

    #print idresults
    return idresults

print ner('Mena Collection.ttl', 'nif')