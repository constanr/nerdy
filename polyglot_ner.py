__author__ = 'croman'
# -*- coding: utf-8 -*-

from polyglot.detect import Detector
from polyglot.text import Text, Word
import rdflib
from lxml import etree
import subprocess
import tweetstotxt
import codecs

def ner(datasetfile, format):

    tweetids = []
    tweets = ''
    tweetdict = {}

    if format == 'xml-collection':
        dataset = etree.parse(datasetfile)
        for tweet in dataset.xpath('//Tweet'):
            tweetText = tweet.xpath('./TweetText/text()')[0]
            tweets += tweetText+"\n"
            tweetids.append(tweet.xpath('./TweetId/text()')[0])
        tweets = tweets.encode('utf-8')
        with codecs.open(datasetfile.split('.xml')[0]+'.txt', 'wb', encoding='utf-8') as txt:
            tweets = tweets.decode('utf-8')
            txt.write(tweets)


    elif format == 'xml-socialtv':
        dataset = etree.parse(datasetfile)
        for tweet in dataset.xpath('//tweet'):
            tweetText = tweet.xpath('./text()')[0]
            tweets += tweetText+'\n'
            tweetids.append(tweet.get('id'))
        tweets = tweets.encode('utf-8')
        with codecs.open(datasetfile.split('.xml')[0]+'.txt', 'wb', encoding='utf-8') as txt:
            tweets = tweets.decode('utf-8')
            txt.write(tweets)


    elif format == "nif":

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

        with codecs.open(datasetfile.split('.ttl')[0]+'.txt', 'wb', encoding='utf-8') as txt:
            tweets = tweets.decode('utf-8')
            txt.write(tweets)



    """for t in tweets.split('\n'):
        text = Text(t)
        detector = Detector(t.decode('utf-8'))
        print text.string.encode('utf-8')
        print (detector.language)"""
    p = subprocess.Popen(['polyglot', '--lang', 'es', 'ner', '--input', datasetfile.split('.ttl')[0]+'.txt'], stdout=subprocess.PIPE)
    output,err = p.communicate()
    results = ''
    tweetoutput = output.split('\n\n')
    tweetoutput.pop()
    for x in range(0, len(tweetoutput)):
        inEntity = False
        for line in tweetoutput[x].splitlines():
            if len(line.split()) < 2:
                word = line.split('O')[0].decode('utf-8')
                entity = u'O'
            else:
                word = line.split()[0].decode('utf-8')
                entity = line.split()[1].decode('utf-8')
            if entity != 'O' and inEntity:
                entity = 'I-'+entity.split('I-')[1]
            elif entity != 'O' and inEntity == False:
                entity = 'B-'+entity.split('I-')[1]
                inEntity = True
            else:
                inEntity = False
            results += word + u'/' + entity + u' '
        results += u"||"+tweetids[x]+u"\n"
    return results
