__author__ = 'croman'
# -*- coding: utf-8 -*-
import wrapper
from senpy.plugins import SenpyPlugin
from senpy.models import Entry, Response
class nerdyPlugin(SenpyPlugin):
    def analyse(self, **params):
        classifier = params.get("classifier", "polyglot-es")
        p = params.get("prefix", None)
        response = Response(prefix=p)
        (entities, types, startIndexes, endIndexes) = wrapper.service(params.get("input"), classifier)
        print (entities, types, startIndexes, endIndexes)
        #(entities, types, startIndexes, endIndexes) = (["CR7", "Real Madrid"],["PER", "ORG"],[0,30],[2,40])
        for x in range(0, len(entities)):
            entry = Entry(id="Entry"+str(x),
                          prefix=p,
                          anchorOf=entities[x],
                          taClassRef="dbo:"+types[x],
                          startIndex=startIndexes[x],
                          endIndex=endIndexes[x])
            response.entries.append(entry)
            print entry
        return response
#n = nerdyPlugin({"name":"nerdy", "version":"0.1"})
#n.analyse(classifier='stanford-es', input="Cristiano Ronaldo is a player")
