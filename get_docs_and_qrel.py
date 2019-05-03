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
import string as S
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

import re
# ---------------------------------------------------------------------------------------- #
# estrazione dei dati di un tag 
def gettagdata(dom,tag):
    nodes = dom.getElementsByTagName(tag)
    if nodes is None or len(nodes)==0:
        return None
    tagdata = []
    for node in nodes:
        tagdata.append(S.rstrip(S.lstrip(node.firstChild.data)))   
    return tagdata
  
schema = Schema(docid      	    = ID(stored=True),
                title      	    = TEXT(stored=True),
                identifier      = ID(stored=True),
                terms 	        = NGRAM(stored=True),
                authors         = NGRAM(stored=True),
                abstract        = TEXT(stored=True),
                publication	    = TEXT(stored=True),
                source          = TEXT(stored=True))

campo = "identifier"
fields = ["title", "abstract", "terms"]

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
    #tolte un po' di parole "inutili"
    title = [re.sub(r"\d+ ","",x.replace(",","").replace(".","").replace("and ","").replace("with ","").replace("of ","").replace("on","").replace("y","").replace("o","").replace("yo","").replace("the","")) for x in title]
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
    
    if sys.argv[4] == "iq":
        # prendo in input le query che mi interessano
        # immagino di avere una lista di numeri di query
        hits = raw_input("Comma-separated query (hit enter to end): ")
        while hits <> "":
            q=hits.split(",")
            for i in q:#per ogni query della lista
                print "\nQuery numero",i
                query = qp(campo,schema,group = qparser.OrGroup).parse(reldocs[i])  # creo una query per cercare i documenti rilevanti
                results = ix.searcher().search(query,limit=maxres)                  # dovrebbe trovare i documenti con gli identificatori
                query_terms = title[int(i)-1].split(" ")                            # creo lista con i termini della query
                first_row = " "*11
                for g in query_terms:
                    first_row += g.rjust(max([len(g)+1,12])," ")
                print first_row
                for j in results:                                                   # per ogni documento
                    row = []
                    c2 = 0
                    for h in query_terms:                                           # per ogni termine della query
                        row.append("")
                        for l in fields:                                            # per ogni campo ("title", "abstract" e "terms")
                            c1 = 0
                            try:
                                for k in j[l].split(" "):                           # per ogni parola del campo
                                    if k==h:                                        # controllo se la parola e' uguale al termine corrente
                                        c1 += 1                                      # se si' aggiungo 1 al conteggio
                                        c2 += 1
                                row[-1] += str(c1).rjust(3," ")                      # riga del tipo ***;***;*** ***;***;*** ...
                                if l!="terms":
                                    row[-1] += ";"
                            except KeyError:
                                row[-1] += "  0"
                                if l!="terms":
                                    row[-1] += ";"
                    # adesso dovrei avere la linea completa 
                    print j["identifier"].ljust(12," ") + " ".join(row)+(" tot. "+str(c2) if c2 != 0 else "")
                    # aggiungi ultima riga con i totali
            hits = raw_input("Comma-separated query (hit enter to end): ")
    
    elif sys.argv[4] == "tnn":                                                    #tot not null
        for i in num:#per ogni query della lista
            query = qp(campo,schema,group = qparser.OrGroup).parse(reldocs[i])  # creo una query per cercare i documenti rilevanti
            results = ix.searcher().search(query,limit=maxres)                  # dovrebbe trovare i documenti con gli identificatori
            query_terms = title[int(i)-1].split(" ")                            # creo lista con i termini della query
            first_row = " "*6
            for g in query_terms:
                first_row += g.rjust(max([len(g)+1,13])," ")
            row = []
            tot = 0
            for h in query_terms:                                           # per ogni termine della query
                row.append("")
                for l in fields:                                            # per ogni campo ("title", "abstract" e "terms")
                    c = 0
                    for j in results:                                       # per ogni documento
                        try:
                            for k in j[l].split(" "):                           # per ogni parola del campo
                                if k==h:                                        # controllo se la parola e' uguale al termine corrente
                                    c += 1                                      # se si' aggiungo 1 al conteggio
                                    tot += 1         
                        except KeyError:
                            pass
                    row[-1] += str(c).rjust(3," ")                      # riga del tipo ***;***;*** ***;***;*** ...
                    if l!="terms":
                        row[-1] += ";"
            # adesso dovrei avere la linea completa 
            if tot != 0:
                print "\n"+first_row
                print "query "+i.ljust(2," ")+ "  ".join(row)+"   tot. "+str(tot)+" parole su "+str(len(reldocs[i].split(" ")))+" documenti rilevanti"
            # aggiungi ultima riga con i totali
    infile.close()
    ix.searcher().close()


#uso: python qrel_....py cartella_indice file_query file_qrels modalita'(iq, tnn) 

