#RUN DI BASE

#--- importazione di interi moduli ---#
import string as str
import sys
import getopt
import os.path
import json

#--- importazione di parti di modulo ---#
from xml.dom.minidom import parse, parseString
from whoosh import scoring,qparser
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser as qp
from whoosh.qparser import MultifieldParser as mp
from whoosh.formats import Frequency
from whoosh.analysis import StandardAnalyzer, RegexAnalyzer, StopFilter, RegexTokenizer

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
        print query,'\t',"Q0",'\t',results[rank]['identifier'],'\t',rank,'\t',results[rank].score,'\t',tag
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
#prendi stop words dal file
json_stop_words = open("../indicizzazione/stopWords.json","r")
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

# search fields
un_campo = 'title'
due_campi = ["title", "abstract"]
tre_campi = ["title", "abstract", "terms"]

MAXDOCS = 1000												# max num doc reperiti
runtag = "BASELINE"

if not os.path.exists(sys.argv[1]):           				# controlla se l'indice non c'e'
    print sys.argv[1],"does not exist"        				# esci se non esiste
else:                                         				# altrimenti procedi
    st = FileStorage(sys.argv[1])             				# afferra la maniglia e
    ix = st.open_index()                      				# apri il file corrispondente
    #--- apertura del file delle query ---#
    infile = open(sys.argv[2],'r')
    #--- lettura del file
    text = infile.read()
    #--- dom delle query
    dom = parseString(text)
    #-- estrazione dei dati della query
    title = gettagdata(dom,'title')
    num = gettagdata(dom,'num')
    for qid in num:
        title[int(qid)-1].encode('utf-8')                                   # prepara il testo della query
        if sys.argv[3]=='1':                                                # se il secondo argomento e' 1
            query = qp( un_campo,                                            # cerca l'indice usando un solo campo
                        schema,                                              # usando lo schema dato
                        group = qparser.OrGroup).parse(title[int(qid)-1])    # e l'operatore OR
        elif sys.argv[3]=='2':                                              # altrimenti
            query = mp(due_campi,                                           # cerca l'indice usando due campi
                        schema,                                              # usando lo schema dato e
                        group = qparser.OrGroup).parse(title[int(qid)-1])    # l'operatore OR
        elif sys.argv[3]=='3':                                              # altrimenti
            query = mp(tre_campi,                                           # cerca l'indice usando tre campi
                        schema,                                              # usando lo schema dato e
                        group = qparser.OrGroup).parse(title[int(qid)-1])    # l'operatore OR
        results = ix.searcher(weighting=scoring.BM25F()).search(query,limit=MAXDOCS)
        #--- res(results,query,MAXDOCS,runtag)                          	#
        res(results,qid,MAXDOCS,runtag)

    infile.close()
    ix.searcher().close()
