#--- importazione di interi moduli
import string as str
import sys
import getopt
import os.path
import numpy as np
#--- importazione di parti di modulo
from whoosh import scoring,qparser,highlight as hl
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser as qp
from whoosh.qparser import MultifieldParser as mp
from whoosh.searching import Searcher
from xml.dom.minidom import parse, parseString
from random import randint
from random import sample
# ---------------------------------------------------------------------------------------- #
# estrazione dei dati di un tag 
def gettagdata(dom,tag):
    nodes = dom.getElementsByTagName(tag)
    if nodes is None or len(nodes)==0:
        return None
    tagdata = []
    for node in nodes:
        tagdata.append(str.rstrip(str.lstrip(node.firstChild.data)))   
    return tagdata

# ---------------------------------------------------------------------------------------- #
class intgen:
    def __init__(self):                       				# inizializza un generatore di interi
        self.index = {}                       				# mappa chiave->intero 
        self.nextint = 0                      				# prossimo intero
    def id2int(self,myid):                      				# dai l'intero della chiave
        if myid not in self.index:              				# se la chiave non e' stata ancora vista
           self.index[myid] = self.nextint      				# inseriscila e dalle l'intero
           self.nextint += 1                  				# prepara il prossimo intero
        return self.index[id]                 				# ritorna l'intero della chiave
    def int2id(self,integer):                 				# dai la chiave dell'intero
        for key,i in self.index.iteritems():  				# scandisci la mappa
            if i==integer:                    				# fino a quando trovi la chiave
                return key                    				# da ritornare
        return None                           				# altrimenti ritorna None
    def write(self):                          				# scrivi il dizionari
        for k,i in self.index.iteritems():    				# scandisci tutte le coppie chiave-valore
            print k,i                         				# e stampa ciascuna coppia
           
# ---------------------------------------------------------------------------------------- #
def res(results, query = "1", n = 10, tag = "tag"):#risultati in formato trec eval
    rank = 0
    if len(results) < n:
        n = len(results)
    for rank in xrange(0,n):
        print query,'\t',"Q0",'\t',results[rank]['identifier'],'\t',rank,'\t',results[rank].score,'\t',tag
        rank += 1
        
# ---------------------------------------------------------------------------------------- #
def getquery(prompt):                         				# 
    return raw_input(prompt)                  				# 
                                              				# 
schema = Schema(docid      	= ID(stored=True),
            title      	= TEXT(stored=True),
            identifier	= ID(stored=True),
            terms 		= NGRAM(stored=True),
            authors     = NGRAM(stored=True),
            abstract 	= TEXT(stored=True),
            publication	= TEXT(stored=True),
            source = TEXT(stored=True))

un_campo = "title"                            				# 
due_campi = ["title", "abstract"]             				# 
tre_campi = ["title", "abstract", "terms"]
runtag = ""                             				# 
                                                            #
MAXDOCS = 10                                  				# max num doc reperiti
MAXLSATERMS = 100                             				# max num righe matrice LSA
MAXRFTERMS = 100                              				# max num termini retroazione
                                              
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
    #--- estrazione dei dati della query
    title = gettagdata(dom,'title')
    num   = gettagdata(dom,'num')
    if sys.argv[4]=='e':                         # se il quarto argomento e' e, per leggere il file di rilevanza
        relfile = open("qrels-treceval.txt",'r') # apro il file di rilevanza dei documenti per query
        #questa parte e' un po' campata per aria usando un dizionario, sono ben accetti suggerimenti per migliorarla
        reldocs = {}
        for r in relfile.readlines():
            a=r.split(" ")[::2]                  # prendo il primo e il terzo elemento di ogni riga (numero query, identificativo documento rilevante)
            if a[0] in reldocs:                  # se e' il primo documento rilevante della query a[0]
                reldocs[a[0]].add(a[1])          # aggiungo all'insieme relativo alla query a[0] il documento
            else:                                # altrimenti  
                reldocs[a[0]] = set(a[1])        # aggiungo numero query come chiave nel dizionario ed il relativo documento
        relfile.close()
    #--- scansione delle query e reperimento
    for qid in num:
        title[int(qid)-1].encode('utf-8')                                   # prepara il testo della query
        if sys.argv[3]=='1':                                                # se il secondo argomento e' 1
            query = qp(un_campo,                                            # cerca l'indice usando un solo campo
                       schema,                                              # usando lo schema dato
                       group = qparser.OrGroup).parse(title[int(qid)-1])    # e l'operatore OR
        elif sys.argv[3]=='2':                                              # altrimenti 
            query = mp(due_campi,                                           # cerca l'indice usando due campi
                       schema,                                              # usando lo schema dato e
                       group = qparser.OrGroup).parse(title[int(qid)-1])    # l'operatore OR
        else:                                                               # altrimenti 
            query = mp(tre_campi,                                           # cerca l'indice usando tre campi
                       schema,                                              # usando lo schema dato e
                       group = qparser.OrGroup).parse(title[int(qid)-1])    # l'operatore OR
        #NOTA:stiamo usando TF_IDF 
        results = ix.searcher(weighting=scoring.TF_IDF()).search(query,limit=MAXDOCS)
        if len(sys.argv) < 5:                                               # caso base
            runtag+="BASETFIDF"
            #--- res(results,query,MAXDOCS,runtag)                          #
            res(results,qid,MAXDOCS,runtag)						            #
        #--- query expansion                                                #
        runtag+="FEEDBK"
        elif sys.argv[4]=='m':                                              # se il quarto arg e' m
            hit = randint(0,min([10,len(results)])-1)                       # cerca i documeni simili
            more_results = results[hit].more_like_this("title")             #
            res(more_results,qid,MAXDOCS,runtag)                            # stampa i nuovi risultati
            results = more_results
        elif sys.argv[4]=='e':                                              # se il quarto arg e' e
            runtag+="EXP"
            #creo un insieme contenente gli identificatori dei documenti trovati piu' rilevanti
            resdocs = set([results[h]['identifier'] for h in range(min([10,len(results)]))]) 
            with ix.searcher() as s:# prepara un alias
                if qid in reldocs:
                    reldocids = resdocs & reldocs[qid] # insieme intersezione dei documenti rilevanti e di quelli trovati
                    reldocnums = [int(s.document_number(identifier=i)) for i in reldocids]  # e una lista di documenti rilevanti
            #nota 'identifier' e' il numero (id) che caratterizza il documento nella collezione cacm
            #mentre il document_number (docnum) e' un numero assegnato al documento nell'indice 
                with ix.searcher() as s:				
                    expansion_terms = s.key_terms(reldocnums,"title",MAXRFTERMS)
                    #usa TFIDF per trovare termini utili(TFIDF medio alto) nei documenti detti rilevanti
                expanded_query_text = ""
                for term,score in expansion_terms:#query costruita usando i termini trovati da key_term()
                    expanded_query_text = term + ' ' + expanded_query_text
                if sys.argv[3]=='1':
                    runtag+="1C"
                    expanded_query = qp(un_campo,schema,group = qparser.OrGroup).parse(expanded_query_text)
                elif sys.argv[3]=='2':
                    runtag+="2C"
                    expanded_query = mp(due_campi,schema,group = qparser.OrGroup).parse(expanded_query_text)
                else:
                    runtag+="3C"
                    expanded_query = mp(tre_campi,schema,group = qparser.OrGroup).parse(expanded_query_text)
                more_results = ix.searcher(weighting=scoring.TF_IDF()).search(expanded_query,limit=MAXDOCS)
                res(more_results,qid,MAXDOCS,runtag)
                results = more_results
        
        # ANCORA DA PROVARE QUESTA PARTE
        elif sys.argv[4]=='i':                                              # se il quarto arg e' i
            runtag+="IMP"
            with ix.searcher() as s:                                        # prepara un alias
                reldocids = [int(s.document_number(docid=results[i]['identifier'])) for i in xrange(min([3,len(results)]))] # e una lista di documenti rilevanti		
                expansion_terms = s.key_terms(reldocids,"title",MAXRFTERMS)
                #usa TFIDF per trovare termini utili(TFIDF medio alto) nei documenti detti rilevanti
            expanded_query_text = ""
            for term,score in expansion_terms:#query costruita usando i termini trovati da key_term()
                expanded_query_text = term + ' ' + expanded_query_text
            if sys.argv[3]=='1':
                runtag+="1C"
                expanded_query = qp(un_campo,schema,group = qparser.OrGroup).parse(expanded_query_text)
            elif sys.argv[3]=='2':
                runtag+="2C"
                expanded_query = mp(due_campi,schema,group = qparser.OrGroup).parse(expanded_query_text)
            else:
                runtag+="3C"
                expanded_query = mp(tre_campi,schema,group = qparser.OrGroup).parse(expanded_query_text)
            more_results = ix.searcher(weighting=scoring.TF_IDF()).search(expanded_query,limit=MAXDOCS)
            res(more_results,qid,MAXDOCS,runtag)
            results = more_results
    infile.close()
    ix.searcher().close()
    
#query_expansion_feedback_batch.py, cartella indice, file query, numero di campi (1, 2 o 3), metodo di espansione delle query ("m", "e" o "i")
