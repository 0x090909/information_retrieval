#--- importazione di interi moduli ---#
import sys
import getopt
import os.path
import json
#--- importazione di parti di modulo ---#
from xml.dom.minidom import parse, parseString

#--- estrazione dei dati di un tag ---#
def gettagdata(dom,tag):
	nodes = dom.getElementsByTagName(tag)
	if nodes is None or len(nodes)==0:
		return None
	node = nodes[0]
	if node is None:
		return None
	return node.firstChild.data.strip()


if __name__ == "__main__":
    docs = open(sys.argv[1],"r") #we have a document per line
    i = 1
    stopWords = []
    #definisco stop word come parola che ha meno di 3 lettere
    for doc in docs:
        progress = (i/54710.0)*100
        #print "\r Parsing progess: %f " % (progress) + "%",
        #--- document object model ---#
        dom = parseString(doc)
        i = i+1
        #--- estrazione dei dati dal documento ---#
        terms = gettagdata(dom,'M')
        title = gettagdata(dom,'T')
        abstract = gettagdata(dom,'W')
        if abstract is not None:
            listTerms = terms.split(" ")
        else:
            listTerms = []

        if title is not None:
            listTitle = title.split(" ")
        else:
            listTitle = []

        if abstract is not None:
            listAbstract = abstract.split(" ")
        else:
            listAbstract = []
        listOfAll = set(listTerms+listTitle+listAbstract)-set("not")
        stop =[stop for stop in listOfAll if len(stop)<=4]
        stopWords += stop
    uniqueStop = set(stopWords)
    print json.dumps(list(uniqueStop))
