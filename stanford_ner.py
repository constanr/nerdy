__author__ = 'croman'
# -*- coding: utf-8 -*-

import rdflib
from lxml import etree
from nltk.tag.stanford import NERTagger

def ner(datasetfile, format):

    tweets = ""
    tweetids = []
    st = NERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '/usr/share/stanford-ner/stanford-ner.jar', encoding='utf8')

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

    tweetlist = []
    for t in tweets.split('\n'):
        tweetlist.append(t.split())

    results = ''

    tagged = st.tag_sents(tweetlist)
    print len(tagged)
    for x in range(0, len(tagged)):
        inEntity = False
        for (word, entity) in tagged[x]:
            if entity != 'O' and inEntity:
                entity = 'I-'+entity
            elif entity != 'O' and inEntity == False:
                entity = 'B-'+entity
                inEntity = True
            else:
                inEntity = False
            results += word + '/' + entity + ' '
        results += "||"+tweetids[x]+"\n"

    return results
