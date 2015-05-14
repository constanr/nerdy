__author__ = 'croman'
# -*- coding: utf-8 -*-

import polyglot
from polyglot.text import Text, Word
import rdflib
from lxml import etree

def ner(datasetfile, format):

    tweets = ""
    tweetids = []

    if format == 'xml':
        dataset = etree.parse(datasetfile)
        for tweet in dataset.xpath('//Tweet'):
            tweetText = tweet.xpath('./TweetText/text()')[0]
            tweets += tweetText+"\n"
            tweetids.append(tweet.xpath('./TweetId/text()')[0])
        tweets = tweets.encode('utf-8')

    elif format == "nif":

        tweetdict = {}
        a = rdflib.Graph()
        a.parse(datasetfile, format='n3')

        for s, p, o in a:
            if s.endswith(',') and p.endswith('isString'):
                tweetid = s.split('#')[0].split('.xml/')[1]
                tweetdict[tweetid] = o

        for key in sorted(tweetdict):
            tweetids.append(key)
            tweets += tweetdict[key]+'\n'
        tweets = tweets.encode('utf-8')


    for t in tweets.split('\n'):
        text = Text(t)
        print text.string.encode('utf-8')
        print text.entities
        print


ner("Microposts2014_Collection_train.ttl", "nif")
