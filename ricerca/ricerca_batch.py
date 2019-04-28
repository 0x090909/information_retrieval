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
schema = Schema(I      = ID(stored=True),
				U      = NUMERIC(stored=True),
				S      = TEXT(stored=True),
				M      = TEXT,
				T      = TEXT,
				P      = TEXT,
                W      = TEXT,
                A      = TEXT)

#--- campi di ricerca
# M - sono le keyword
# T - e' il titolo
un_campo = 'M'
due_campi = ["M", "T"]

#--- verifica dell'esistenza dell'indice
if not os.path.exists(sys.argv[1]):
    #--- esci se non esiste
    print sys.argv[1],"does not exist"
else:
    #--- procedi se esiste
    st = FileStorage(sys.argv[1])
    ix = st.open_index()
    #--- apertura del file delle query ---#
    infile = open(sys.argv[2],'r')
    #--- lettura del file
    text = infile.read()
    #--- dom delle query
    dom = parseString(text)
    #--- estrazione dei dati della query
    title = gettagdata(dom,'T')
    num   = gettagdata(dom,'I')
    #--- scansione delle query e reperimento
    for id in num:
        title[int(id)-1].encode('utf-8')
        # print int(id),title[int(id)-1]
        query = QueryParser(un_campo,None,\
                            group = qparser.OrGroup).parse(title[int(id)-1])
        results = ix.searcher(weighting=scoring.TF_IDF()).search(query,\
							  limit=1000)
        res(results,id,1000,"tag")
    ix.searcher().close()
