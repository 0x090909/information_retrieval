#--- importazione di interi moduli
import sys
import getopt
import os.path
#--- importazione di parti di modulo
from whoosh import scoring
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

# def res(results,query):
#     print "Trovati",len(results),"risultati in risposta a",query
#     for r in results:
#         #--- togli il commento per stampare il titolo
#         print r['docid']#, print r['title']

def res(results, query = "1", n = 10, tag = "tag"):
    rank = 0
    if len(results) < n:
        n = len(results)
    for rank in xrange(0,n):
        print str(rank) + " " +(results[rank]["title"])
        rank += 1

def getquery(prompt):
    return raw_input(prompt)



#--- definizione dello schema (deve essere quello usato
#--- dall'indicizzatore
schema = Schema(docid      	= ID(stored=True),
        		title      	= TEXT(stored=True),
        		identifier	= ID(stored=True),
        		terms 		= NGRAM(stored=True),
        		authors     = NGRAM(stored=True),
        		abstract 	= TEXT(stored=True),
        		publication	= TEXT(stored=True),
        		source 		= TEXT(stored=True))

#--- campi di ricerca
# M - sono le keyword
# T - e' il titolo

un_campo = 'title'
due_campi = ["title", "abstract"]


#--- verifica dell'esistenza dell'indice
if not os.path.exists(sys.argv[1]):
    #--- esci se non esiste
    print sys.argv[1],"does not exist"
else:
    #--- procedi se esiste
    st = FileStorage(sys.argv[1])
    ix = st.open_index()
    print ix
    querytext = getquery("Enter a query (hit enter to end): ")
    while querytext <> "":
        #--- togli il commento per cercare su piu' campi
        #--- query = MultifieldParser(due_campi,ix.schema).parse(querytext)
        #--- e commenta la riga seguente
        query = QueryParser(un_campo,schema).parse(querytext)
        results = ix.searcher(weighting=scoring.TF_IDF()).search(query)
        #--- res(results,query)
        res(results)
        querytext = getquery("Enter a query (hit enter to end): ")
    ix.searcher().close()
