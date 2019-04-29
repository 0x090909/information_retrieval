#--- importazione di interi moduli ---#
import string as str
import sys
import getopt
import os.path

#--- importazione di parti di modulo ---#
from xml.dom.minidom import parse, parseString
from whoosh import scoring,qparser
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

#--- estrazione dei dati di un tag ---#
def gettagdata(dom,tag):
    nodes = dom.getElementsByTagName(tag)
    if nodes is None or len(nodes)==0:
        return None
    tagdata = []
    for node in nodes:
        tagdata.append(str.rstrip(str.lstrip(node.firstChild.data)))
    return tagdata

#--- stampa i risultati in forma trec_eval
def res(results, query = "1", n = 10, tag = "tag"):
    rank = 0
    if len(results) < n:
        n = len(results)
    for rank in xrange(0,n):
        print query,"Q0",results[rank].docnum,\
          rank,results[rank].score,tag
        rank += 1

#--- elementi XML possibili ---#
tags = ['I',
		'U',
		'S',
		'M',
		'T',
		'P',
		'W',
		'A']

#--- definizione dello schema (deve essere quello usato
#--- dall'indicizzatore
schema = Schema(docid      	= ID(stored=True),
		title      	= TEXT(stored=True),
		identifier	= ID(stored=True),
		terms 		= NGRAM(stored=True),
		authors      	= NGRAM(stored=True),
		abstract 	= TEXT(stored=True),
		publication	= TEXT(stored=True),
		source 		= TEXT(stored=True))

# search fields
un_campo = 'title'
due_campi = ["title", "abstract"]
tre_campi = ["title", "abstract", "terms"]

# checking index
if not os.path.exists(sys.argv[1]):
    # quitting if not existing
    print sys.argv[1],"does not exist"
else:
    # if the index is existing
    # opening index
    st = FileStorage(sys.argv[1])
    ix = st.open_index()
    # reading a query
    querytext = getquery("Enter a query (hit enter to end): ")
    # while not empty
    while querytext <> "":
        # if the second argument is 1 search one field
        if sys.argv[2]=='1':
            query = QueryParser(un_campo,schema).parse(querytext)
        # if the second argument is 2 search two fields
        elif sys.argv[2]=='2':
            query = MultifieldParser(due_campi,ix.schema).parse(querytext)
        else:
            # search three fields
            query = MultifieldParser(tre_campi,ix.schema).parse(querytext)
        # get results using TF_IDF (BM25F may be used instead)
        results = ix.searcher(weighting=scoring.TF_IDF()).search(query)
        # printing results
        res(results)
        # reading new query
        querytext = getquery("Enter a query (hit enter to end): ")
    # closing index
    ix.searcher().close()
    
