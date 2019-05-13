#--- importazione di interi moduli ---#
import string
import sys
import getopt
import os.path
import multiprocessing as mp

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
        tagdata.append(string.rstrip(string.lstrip(node.firstChild.data)))
    return tagdata

#--- stampa i risultati in forma trec_eval
def res(results, query, n, tag, outf):
    rank = 0
    if len(results) < n:
        n = len(results)
    for rank in xrange(0,n):
        s = query + " " + "Q0" + " " + str(results[rank].docnum) + " " + str(rank) + " " + str(results[rank].score) + " " + tag + "\n"
        outf.write(s)
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

analyzer = StandardAnalyzer(stoplist=frozenset(datastore))
#--- definizione dello schema ---#
schema = Schema(docid      		= ID(stored=True),
				title      		= TEXT(stored=True),
				identifier	   	= ID(stored=True),
				terms 			= NGRAM(stored=True),
				authors      	= NGRAM(stored=True),
				abstract 		= TEXT(stored=True),
				publication		= TEXT(stored=True),
				source 			= TEXT(stored=True))
#--- campi di ricerca
un_campo = 'title'
due_campi = ["title", "abstract"]
tre_campi = ["title", "abstract", "terms"]
#--- procedi se esiste
st = FileStorage(sys.argv[1])
ix = st.open_index()

def cerca_max(b_min, b_max, proc):
    print("B min: "+str(b_min))
    print("B max: "+str(b_max))
    #--- apertura del file delle query ---#
    infile = open(sys.argv[2],'r')
    #--- lettura del file
    text = infile.read()
    #--- dom delle query
    dom = parseString(text)
    #--- estrazione dei dati della query
    title = gettagdata(dom,'title')
    num   = gettagdata(dom,'num')
    b = b_min+0.01
    while b_min < b <= b_max:
        k1 = 0.0
        while k1 <= 10.0:
            outfile = open(str(proc)+"/ohsumed-b"+str(b)+"-k"+str(k1)+".txt","w")
            #--- scansione delle query e reperimento
            for id in num:
                title[int(id)-1].encode('utf-8')
                # print int(id),title[int(id)-1]
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
                results = ix.searcher(weighting=scoring.BM25F(B=b,K1=k1)).search(query,limit=1000)
                res(results,id,1000,str(proc)+"/cacm-b"+str(b)+"-k"+str(k1),outfile)
            k1 += 0.5
        b += 0.05
    ix.searcher().close()
    print("Worker "+ str(proc) + " done")

if __name__ == "__main__":
	#--- verifica dell'esistenza dell'indice
	if not os.path.exists(sys.argv[1]):
	    #--- esci se non esiste
	    print sys.argv[1],"does not exist"
	else:
	    processes = [mp.Process(target=cerca_max, args=(0,0.25,1)), mp.Process(target=cerca_max, args=(0.25,0.50,2)), mp.Process(target=cerca_max, args=(0.50,0.75,3)), mp.Process(target=cerca_max, args=(0.75,1,4))]
	# Run processes
	# Run processes
	for p in processes:
	    p.start()
