__author__ = 'croman'
# -*- coding: utf-8 -*-

import rdflib
from lxml import etree
from nltk.tag.stanford import NERTagger
import ner

def ner(datasetfile, format, language):

    tweets = ""
    tweetids = []
    if language == 'english':
        st = NERTagger('classifiers/english.all.3class.distsim.crf.ser.gz', 'classifiers/stanford-ner.jar', encoding='utf8')
    elif language == 'spanish':
        st = NERTagger('classifiers/spanish.ancora.distsim.s512.crf.ser.gz', 'classifiers/stanford-ner.jar', encoding='utf8')

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
        print tweets

    tweetlist = []
    for t in tweets.splitlines():
        newtweet = []
        for word in t.split():
            newword = u''
            if word.endswith(",") or word.endswith("."):
                newtweet.append(word[:-1])
                newtweet.append(word[-1])
            else:
                newtweet.append(word)
        print newtweet
        tweetlist.append(newtweet)


    results = ''
    tagged = []

    for tweet in tweetlist:
        tagged.append(st.tag(tweet))
        print tagged[-1]
    print len(tagged)
    for x in range(0, len(tagged)):
        inEntity = False
        for line in tagged[x]:
            for (word, entity) in line:
                if entity != 'O' and inEntity:
                    entity = 'I-'+entity
                elif entity != 'O' and inEntity == False:
                    entity = 'B-'+entity
                    inEntity = True
                else:
                    inEntity = False
                results += word + '/' + entity + ' '
        results += "||"+tweetids[x]+"\n"

    print results
    return results
