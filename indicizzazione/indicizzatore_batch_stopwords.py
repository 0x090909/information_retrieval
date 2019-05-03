#--- importazione di interi moduli ---#
import sys
import getopt
import os.path

#--- importazione di parti di modulo ---#
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from xml.dom.minidom import parse, parseString
from whoosh.analysis import StandardAnalyzer, RegexAnalyzer, StopFilter, RegexTokenizer

import json
#--- estrazione dei dati di un tag ---#
def gettagdata(dom,tag):
	nodes = dom.getElementsByTagName(tag)
	if nodes is None or len(nodes)==0:
		return None
	node = nodes[0]
	if node is None:
		return None
	return node.firstChild.data.strip()
#prendi stop words dal file
json_stop_words = open("stopWords.json","r")
json_string = ""
for line in json_stop_words:
	json_string = json_string+line

datastore = json.loads(json_string)

analyzer = StandardAnalyzer(stoplist=frozenset(datastore))
#--- definizione dello schema ---#
schema = Schema(docid      		= ID(stored=True),
				title      		= TEXT(analyzer=analyzer,stored=True),
				identifier	   	= ID(stored=True),
				terms 			= NGRAM(stored=True),
				authors      	= NGRAM(stored=True),
				abstract 		= TEXT(analyzer=analyzer,stored=True),
				publication		= TEXT(stored=True),
				source 			= TEXT(stored=True))

#--- elementi XML possibili ---#
tags = ['I',
		'U',
		'S',
		'M',
		'T',
		'P',
		'W',
		'A']

#--- verifica dell'esistenza e creazione dell'indice ---#
if not os.path.exists(sys.argv[1]):
	os.mkdir(sys.argv[1])
	ix = create_in(sys.argv[1], schema)
else:
	ix = open_dir(sys.argv[1])

#--- allocazione del writer ---#
writer = ix.writer(limitmb=2048,procs=4,multisegment=True)

#--- scansione dei file dei documenti ---#
#leggi file xml

docs = open(sys.argv[2],"r") #we have a document per line
i = 1
for doc in docs:
		progress = (i/54711.0)*100
		print "\r Indexing progess: %f " % (progress) + "%",
	    #--- document object model ---#
		dom = parseString(doc)
		i = i+1
		#--- estrazione dei dati dal documento ---#
		this_I = gettagdata(dom,'I')
		this_U = gettagdata(dom,'U')
		this_S = gettagdata(dom,'S')
		this_M = gettagdata(dom,'M')
		this_T = gettagdata(dom,'T')
		this_P = gettagdata(dom,'P')
		this_W = gettagdata(dom,'W')
		this_A = gettagdata(dom,'A')

		#--- indicizzazione e archiviazione del documento ---#
		writer.add_document(docid	 	= this_I,
						   	title   	= this_T,
							identifier	= this_U,
							terms		= this_M,
							authors	    = this_A,
			                abstract    = this_W,
			                publication = this_P,
			                source      = this_S)
 #print listaDocumenti

print "\r Indexed everything!",
#--- chiusura sicura del writer ---#
print "committing index...",
writer.commit()
print "done"
