#--- cacm_search_eval
#--- MM: 2018-03-28

# importazione di interi moduli
import string as str
import sys
import getopt
import os.path
import json
# importazione di parti di modulo
from xml.dom.minidom import parse, parseString
from whoosh import scoring,qparser
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StandardAnalyzer, RegexAnalyzer, StopFilter, RegexTokenizer

# estrazione dei dati di un tag
def gettagdata(dom,tag):
    nodes = dom.getElementsByTagName(tag)
    if nodes is None or len(nodes)==0:
        return None
    tagdata = []
    for node in nodes:
        tagdata.append(str.rstrip(str.lstrip(node.firstChild.data)))
    return tagdata

# stampa i risultati in forma trec_eval
def res(results, query = "1", n = 10, tag = "tag"):
    rank = 0
    if len(results) < n:
        n = len(results)
    for rank in xrange(0,n):
        print query,'\t',"Q0",'\t',results[rank]['docid'],'\t',\
          rank,'\t',results[rank].score,'\t',tag
        rank += 1

# elementi XML possibili
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
# definizione dello schema (deve essere quello usato
# dall'indicizzatore
#--- definizione dello schema ---#
schema = Schema(docid      		= ID(stored=True),
				title      		= TEXT(stored=True),
				identifier	   	= ID(stored=True),
				terms 			= NGRAM(stored=True),
				authors      	= NGRAM(stored=True),
				abstract 		= TEXT(stored=True),
				publication		= TEXT(stored=True),
				source 			= TEXT(stored=True))

# campi di ricerca
campi = ["title", "abstract"]
weight = "TFIDF"
runtag = "RUNTAG"
index = "../ohsumed_index_dir"
queryfile = "query.ohsu.1-63.xml"

opts, args = getopt.getopt(sys.argv[1:], "f:w:t:i:q:")
for opt,arg in opts:
    if opt == "-f":
        # estrae i campi separati da virgola
        campi = re.split(",",arg)
    elif opt == "-w":
        weight = arg
    elif opt == "-t":
        runtag = arg+"_"+weight
    elif opt == "-i":
        index = arg
    elif opt == "-q":
        queryfile = arg
    else:
        assert False, "uso: -f campi,di,ricerca -w pesatura -t runtag -i index directory"

# verifica dell'esistenza dell'indice e del query file
if not os.path.exists(index):
    # esci se non esiste
    print index,"does not exist"
elif not os.path.exists(queryfile):
    # esci se non esiste
    print queryfile,"does not exist"
else:
    # procedi se esiste
    st = FileStorage(index)
    ix = st.open_index()
    # apertura del file delle query
    infile = open(queryfile,'r')
    # lettura del file
    text = infile.read()
    # dom delle query
    dom = parseString(text)
    # estrazione dei dati della query
    title = gettagdata(dom,'title')
    num   = gettagdata(dom,'num')
    #    for i in xrange(0,64):
    #    print num[i],MultifieldParser(campi, None, group = qparser.OrGroup).parse(title[i])
    # scansione delle query e reperimento
    for id in num:
        title[int(id)-1].encode('utf-8')
        if len(campi)==1:
            query = QueryParser(campi[0], schema, group = qparser.OrGroup).parse(title[int(id)-1])
            #print query
        else:
            query = MultifieldParser(campi, schema, group = qparser.OrGroup).parse(title[int(id)-1])
            #print query
        if weight=="TFIDF":
            results = ix.searcher(weighting=scoring.TF_IDF()).search(query, limit=1000)
        elif weight=="BM25F":
            results = \
            ix.searcher(weighting=scoring.BM25F()).search(query,limit=1000)
        else:
            # default: TF
            results = ix.searcher(weighting = scoring.Frequency()).search(query, limit=1000)
        res(results,id,1000,runtag)
    ix.searcher().close()
