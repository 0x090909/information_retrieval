#usando la modalita' iq
#dato insieme di query ottenere i documenti rilevanti per ciascuna
#contare il numero di volte in cui una parola della query appare nei documenti
#tipo:
#Query k
#       word1 word2 ...
#doc1   2;7;0 4;0;0 
#doc2   0;0;0 0;3;0
#...
#con numero di volte in titolo;abstract;tremini

#--- importazione di interi moduli
import string as st
import sys
import getopt
import os.path
#--- importazione di parti di modulo
from whoosh import qparser
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser as qp
from whoosh.qparser import MultifieldParser as mp
from whoosh.searching import Searcher
from xml.dom.minidom import parse, parseString

import re
# ---------------------------------------------------------------------------------------- #
# estrazione dei dati di un tag 
def gettagdata(dom,tag):
    nodes = dom.getElementsByTagName(tag)
    if nodes is None or len(nodes)==0:
        return None
    tagdata = []
    for node in nodes:
        tagdata.append(st.rstrip(st.lstrip(node.firstChild.data)))   
    return tagdata

# ---------------------------------------------------------------------------------------- #
def iq(q, reldocs, title, maxres):
    for i in q:#per ogni query della lista
        print "\nQuery numero",i
        query = qp(campo,ix.schema,group = qparser.OrGroup).parse(reldocs[i])  # creo una query per cercare i documenti rilevanti
        results = ix.searcher().search(query,limit=maxres)                  # dovrebbe trovare i documenti con gli identificatori
        query_terms = list(set(title[int(i)-1].split(" ")))                            # creo lista con i termini della query
        first_row = " "*11
        lterms = dict([(x,max([len(x),10])+3) for x in query_terms])
        #print lterms
        for g in query_terms:
            first_row += g.ljust(lterms[g]," ")
        print first_row
        for j in results:                                                   # per ogni documento
            row = [""]
            c2 = 0
            for g in query_terms:                                           # per ogni termine della query
                row.append("")
                for l in fields:                                            # per ogni campo ("title", "abstract" e "terms")
                    c1 = 0
                    try:
                        for k in j[l].replace(","," ").replace("/"," ").replace("."," ").replace("-"," ").replace("?","").replace("'"," ").lower().split(" "):                           # per ogni parola del campo
                            if k==g :                                        # controllo se la parola e' uguale al termine corrente
                                c1 += 1                                      # se si' aggiungo 1 al conteggio
                                c2 += 1
                        row[-1] += (str(c1)+(";" if l!="terms" else "")).ljust(4," ") # riga del tipo ***;***;*** ***;***;*** ...                  
                    except KeyError:
                        row[-1] += "*"
                        if l!="terms":
                            row[-1] += ";  "
                row[-1] = row[-1].ljust(lterms[g]," ")
            # adesso dovrei avere la linea completa 
            print j["identifier"].ljust(11," ") + "".join(row)+(" tot. "+str(c2) if c2 != 0 else "")
            # aggiungi ultima riga con i totali
    return

# ---------------------------------------------------------------------------------------- #
def tnn(i, reldocs, title, maxres):
    query = qp(campo,ix.schema,group = qparser.OrGroup).parse(reldocs[i])  # creo una query per cercare i documenti rilevanti
    results = ix.searcher().search(query,limit=maxres)                  # dovrebbe trovare i documenti con gli identificatori
    query_terms = list(set(title[int(i)-1].split(" ")))                           # creo lista con i termini della query
    first_row = " "*11
    lterms = dict([(x,max([len(x),10])+3) for x in query_terms])
    for g in query_terms:
        first_row += g.ljust(lterms[g]," ")
    row = []
    tot = 0
    for g in query_terms:                                           # per ogni termine della query
        row.append("")
        for l in fields:                                            # per ogni campo ("title", "abstract" e "terms")
            c = 0
            for j in results:                                       # per ogni documento
                try:
                    for k in j[l].replace(","," ").replace("/"," ").replace("."," ").replace("-"," ").lower().split(" "):      # per ogni parola del campo
                        if k==g:                                        # controllo se la parola e' uguale al termine corrente
                            c += 1                                      # se si' aggiungo 1 al conteggio
                            tot += 1         
                except KeyError:
                    pass
            row[-1] += (str(c)+(";" if l!="terms" else "")).ljust(4," ")                      # riga del tipo ***;***;*** ***;***;*** ...
        row[-1] = row[-1].ljust(lterms[g]," ")
    # adesso dovrei avere la linea completa 
    if tot != 0:
        print "\n"+first_row
        print "query "+i.ljust(5," ")+ "".join(row)+"   tot. "+str(tot)+" parole su "+str(len(reldocs[i].split(" ")))+" documenti rilevanti"
    # aggiungi ultima riga con i totali
    return
    
# ---------------------------------------------------------------------------------------- #
def fqt(hit, num, title):
    ql = []
    if isinstance(hit, basestring):
        for i in num:
            query_terms = set(title[int(i)-1].split(" "))
            if hit in query_terms:
                ql.append(i)
        if ql:
            print "\nLa parola '"+hit+"' si trova nelle query: ",
            print str(ql)[1:-1].replace("'","").replace("u","")
        else:
            print "\nLa parola '"+hit+"' non si trova in nessuna query."
    else:
        for i in num:
            query_terms = set(title[int(i)-1].split(" "))
            if set(hit).issubset(query_terms):
                ql.append(i)
        if ql:
            print "\nLe parole "+str(hit)[1:-1]+" si trovano contemporanamente nelle query: ",
            print str(ql)[1:-1].replace("'","").replace("u","")
        else:
            print "\nLe parole "+str(hit)[1:-1]+" non si trovano contemporanamente in nessuna query."
    return ql

# ---------------------------------------------------------------------------------------- #
import json

json_stop_words = open("./stopWords_clinico.json","r")
json_string = ""
for line in json_stop_words:
	json_string = json_string+line

datastore = json.loads(json_string)
#print datastore

campo = "identifier"
fields = ["title", "abstract", "terms"]

if not os.path.exists(sys.argv[1]):                     # controlla se l'indice non c'e'
    print sys.argv[1],"does not exist"                  # esci se non esiste
else:                                                   # altrimenti procedi
    fst = FileStorage(sys.argv[1])                      # afferra la maniglia e
    ix = fst.open_index()                               # apri il file corrispondente
    #--- apertura del file delle query ---#
    infile = open(sys.argv[2],'r')
    #--- lettura del file
    text = infile.read()
    #--- dom delle query
    dom = parseString(text)
    #--- estrazione dei dati della query
    #title = gettagdata(dom,'title')
    num   = gettagdata(dom,'num')
    #desc  = gettagdata(dom,'desc')
    #for x in range(len(title)-1):    
    #    title[x]+=" "+desc[x]
    title = gettagdata(dom,'desc')
    title = [x.replace(",","").replace("/"," ").replace(".","").replace("-"," ").replace("?","").replace("'"," ").lower() for x in title]
    title = [re.sub(r"\d+ ",""," ".join([y for y in x.split(" ") if y not in datastore])) for x in title]
    #print title
    relfile = open(sys.argv[3],'r') # apro il file di rilevanza dei documenti per query
    reldocs = {}
    maxres = 1
    count = 0
    for r in relfile.readlines():
        a=r.split(" ")[::2]                  # prendo il primo e il terzo elemento di ogni riga (numero query, identificativo documento rilevante)
        if a[0] in reldocs:                  # se e' il primo documento rilevante della query a[0]
           reldocs[a[0]]+=" "+a[1]           # aggiungo all'insieme relativo alla query a[0] il documento
           count += 1
        else:                                # altrimenti  
            reldocs[a[0]] = a[1]             # aggiungo numero query come chiave nel dizionario ed il relativo documento
            if count > maxres:
                maxres = count
                if int(a[0])<64:
                    mydoc = a[0]
            count = 0
    relfile.close()
    # fino ad ora ho i documenti rilevanti per query
    
    if sys.argv[4] == "iq":                          #indice query
        # prendo in input le query che mi interessano
        # immagino di avere una lista di numeri di query
        hits = raw_input("Comma-separated query (tra 1 e 63 compresi, press enter to end): ")
        while hits != "":
            q=hits.split(",")
            iq(q, reldocs, title, maxres)
            hits = raw_input("\nComma-separated query (tra 1 e 63 compresi, press enter to end): ")
    
    
    elif sys.argv[4] == "tnn":                                                    #tot not null
        for i in num:#per ogni query della lista
            tnn(i, reldocs, title, maxres)
    
    
    elif sys.argv[4] == "fqt":                                                      #find query term
        hits = raw_input("Comma-separated terms (press enter to end): ")
        while hits != "":
            hits = hits.split(",")
            for hit in hits:
                ql = fqt(hit, num, title)
                if len(sys.argv) > 5 and sys.argv[5] == "-d":
                    if ql:
                        for i in ql:
                            iq([i], reldocs, title, maxres)
                            tnn(i, reldocs, title, maxres)
                            print "\n"
                    else:
                        print "\nNo details avaiable."
                    print "#"*200
            
            if len(sys.argv) > 5 and sys.argv[5] == "-d" and len(hits)>1:
                ql = fqt(hits, num, title)
                if ql:
                    for i in ql:
                        iq([i], reldocs, title, maxres)
                        tnn(i, reldocs, title, maxres)
                        print "\n"
                else:
                    print "\nNo details avaiable."
            
            hits = raw_input("\nComma-separated terms (press enter to end): ")    
    infile.close()
    ix.searcher().close()


#uso: python get_....py cartella_indice file_query file_qrels modalita'(iq, tnn, fqt) 
# python frq_terms_rel_docs.py ./indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt iq
# python frq_terms_rel_docs.py ./indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt tnn





