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
    """
    Funzione che serve per trovare, data una lista di query identificate da un numero tra 1 e 63, 
    quante volte appaiono i termini delle query nei corrsipondenti documenti rilevanti,
    suddividendo i conteggi nei tre campi title, abstract e trems.
    Il risultato dovrebbe essere del tipo:
    
    #Query i
    #       word1  word2  ...
    #doc1   2;7;0  4;0;0   .          (word1 e' presente 2 volte in title, 7 volte in abstract e 0 volte in terms, word2 non e' presente in doc1)
    #doc2   0;*;0  0;*;0   .          (gli asterischi indicano che, in questo caso, a doc2 manca il campo abstract)
    #...      .      .    ...
    
    Per ogni i contenuto nella lista q.
    I campi sono in ordine title;abstract;trems
    
    Parameters
    ----------
    q : list of string
    Lista contenente gli identificatori delle query che interessano.
    
    reldocs : dict
    Dizionario, deve avere come chiavi gli identificatori contenuti in q e come valori gli identificatori dei documenti rilevanti corrispondenti,
    possibilmente ottenibili dal "file di rilevanza".
    
    title : list of string
    Lista delle query
    
    maxres : int
    Numero intero positivo deve indicare il numero massimo di documenti rilevanti.
    
    Returns
    -------
    None
    """
    
    for i in q:                                                                         # Per ogni query della lista q
        print "\nQuery numero",i
        query = qp(campo,ix.schema,group = qparser.OrGroup).parse(reldocs[i])           # Crea una query per cercare i documenti rilevanti
        results = ix.searcher().search(query,limit=maxres)                              # Dovrebbe trovare i documenti rilevanti usando gli identificatori
        query_terms = list(set(title[int(i)-1].split(" ")))                             # Crea lista con i termini della query
        first_row = " "*11  # Per compensare la lunghezza dell'identificatore dei documenti
        lterms = dict([(x,max([len(x),10])+3) for x in query_terms])                    # Crea lista che riporta qunto spazio dedicare a ciascuna colonna
        #print lterms
        for g in query_terms:                                                           # Crea la prima riga con i termini della query
            first_row += g.ljust(lterms[g]," ")
        print first_row
        for j in results:                                                               # Per ogni documento rilevante per la query i
            row = [""]
            c2 = 0  # Contatore per riga
            for g in query_terms:                                                       # Per ogni termine della query
                row.append("")
                for l in fields:                                                        # Per ogni campo ("title", "abstract" e "terms")
                    c1 = 0  # Contatore per parola e campo
                    try:
                        cleaned_term = j[l].replace(","," ").replace("/"," ").replace("."," ").replace("-"," ").replace("?","").replace("'"," ").lower().split(" ")
                        for k in cleaned_term:                                          # Per ogni parola del campo
                            if k==g :                                                   # Controllo se la parola e' uguale al termine corrente,
                                c1 += 1                                                 # se si' aggiungo 1 al conteggio
                                c2 += 1
                        row[-1] += (str(c1)+(";" if l!="terms" else "")).ljust(4," ")   # aggiunge elemento come "2;  " a row[-1]               
                    except KeyError:                                                    # Se un campo non e' presente nel documento aggiunge invece "*;  "
                        row[-1] += "*"
                        if l!="terms":
                            row[-1] += ";  "
                row[-1] = row[-1].ljust(lterms[g]," ")                                  # aggiusta la spaziatura per l'elemento ***;***;***     
            # Adesso si dovrebbe avere la riga completa sotto forma di lista di elementi delle colonne in row
            print j["identifier"].ljust(11," ") + "".join(row)+(" tot. "+str(c2) if c2 != 0 else "") 
            # Stampa la riga e aggiunge un'ultima colonna con i totali di riga(se non nulli)
    return None

# ---------------------------------------------------------------------------------------- #
def tnn(i, reldocs, title, maxres):
    """
    Funzione che riassume i risultati ottenibili con la funzione iq(), per la query i.
    Stampa i totali di colonna della "matrice" ottenibile da iq(), per la query i.
    Omette eventuali query per cui i documenti rilevanti non contengono nessuna parola della query.
    
    Il risultato dovrebbe essere del tipo:
                word1  word2  ...
    #Query i    3;0;0  0;0;0  ... (word1 e' presente 3 volte in totale tra i title dei documenti rilevani, word2 non e' presente in nessun documento rilevante)
    
    I campi sono in ordine title;abstract;trems
    
    Parameters
    ----------
    i : string
    Stringa che contiene l'identificatore della query che ci interessa.
    
    reldocs : dict
    Dizionario, deve avere come chiavi gli identificatori di alcune query, tra cui i, e come valori gli identificatori dei documenti rilevanti corrispondenti,
    possibilmente ottenibili dal "file di rilevanza".
    
    title : list of string
    Lista delle query
    
    maxres : int
    Numero intero positivo deve indicare il numero massimo di documenti rilevanti.
    
    Returns
    -------
    None
    """
    
    query = qp(campo,ix.schema,group = qparser.OrGroup).parse(reldocs[i])               # Crea una query per cercare i documenti rilevanti
    results = ix.searcher().search(query,limit=maxres)                                  # Dovrebbe trovare i documenti rilevanti usando gli identificatori
    query_terms = list(set(title[int(i)-1].split(" ")))                                 # Crea lista con i termini della query
    first_row = " "*11
    lterms = dict([(x,max([len(x),10])+3) for x in query_terms])                        # Crea lista che riporta qunto spazio dedicare a ciascuna colonna
    for g in query_terms:                                                               # Crea la prima riga con i termini della query
        first_row += g.ljust(lterms[g]," ")
    row = []
    tot = 0
    for g in query_terms:                                                               # Per ogni termine della query
        row.append("")
        for l in fields:                                                                # Per ogni campo ("title", "abstract" e "terms")
            c = 0
            for j in results:                                                           # Per ogni documento
                try:
                    cleaned_term = j[l].replace(","," ").replace("/"," ").replace("."," ").replace("-"," ").replace("?","").replace("'"," ").lower().split(" ")
                    for k in cleaned_term:                                              # Per ogni parola del campo
                        if k==g:                                                        # Controllo se la parola e' uguale al termine corrente,
                            c += 1                                                      # se si' aggiungo 1 al conteggio
                            tot += 1         
                except KeyError:                                                        # Se il campo non c'e' il conteggio rimane a 0 
                    pass
            row[-1] += (str(c)+(";" if l!="terms" else "")).ljust(4," ")                # aggiusta la spaziatura per l'elemento ***;***;***  
        row[-1] = row[-1].ljust(lterms[g]," ")
    # Adesso si dovrebbe avere la riga completa sotto forma di lista di elementi delle colonne in row
    if tot != 0:
        print "\n"+first_row
        print "query "+i.ljust(5," ")+ "".join(row)+"   tot. "+str(tot)+" parole su "+str(len(reldocs[i].split(" ")))+" documenti rilevanti"
    # Stampa la riga se il totale e' non nullo e aggiunge un'ultima colonna con il totale di riga
    return None
    
# ---------------------------------------------------------------------------------------- #
def fqt(hit, num, title):
    """
    Funzione che permette di sapere in quali query e' presente la parola in hit o, se hit contiene piu' parole, le query dove quelle parole appaiono contemporaneamente.
    
    Il risultato dovrebbe essere del tipo:
    
    La parola 'hit' si trova nelle query: 1,2,3,...
    
    oppure
    
    Le parole 'hi1', 'hit2', ... si trovano contemporanamente nelle query: 1,2,3,... 
    
    Parameters
    ----------
    hit : string o lista di string
    Se in formato string dovrebbe contenere solo un termine, se e' una lista puo' contenere piu' termini.
    
    num : list
    Contiene gli identificatori delle query.
    
    title : list of string
    Lista delle query
    
    Returns
    -------
    ql : list
    Contiene gli identificatori delle query in cui e' presente la parola
    """
    
    ql = []
    if isinstance(hit, basestring):
        for i in num:                                                                   # Per ogni query in num
            query_terms = set(title[int(i)-1].split(" "))                               # Creo l'insieme delle parole della query
            if hit in query_terms:                                                      # Controllo se il termine hit e' in questo insieme
                ql.append(i)
        if ql:
            print "\nLa parola '"+hit+"' si trova nelle query: ",
            print str(ql)[1:-1].replace("'","").replace("u","")  # [1:-1] serve per togliere le parentesi quadre, replace("u","") nel caso la stringa fosse unicode
        else:
            print "\nLa parola '"+hit+"' non si trova in nessuna query."
    else:
        for i in num:                                                                   # Per ogni query in num
            query_terms = set(title[int(i)-1].split(" "))                               # Creo l'insieme delle parole della query
            if set(hit).issubset(query_terms):                                          # Controllo se i termini in hit formano un sottoinsieme delle parole nella query 
                ql.append(i)
        if ql:
            print "\nLe parole "+str(hit)[1:-1]+" si trovano contemporanamente nelle query: ",
            print str(ql)[1:-1].replace("'","").replace("u","")
        else:
            print "\nLe parole "+str(hit)[1:-1]+" non si trovano contemporanamente in nessuna query."
    return ql

# ---------------------------------------------------------------------------------------- #
import json
# rimuove gia' le stopword delle prove precedenti 
json_stop_words = open("../Indicizzazione/stopWords_clinico.json","r")
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
    
    if sys.argv[4] == "iq":                                                         # identificatore query
        # Prendo in input le query che mi interessano
        # Si prevede di avere una lista degli identificatori delle query
        hits = raw_input("Inserisci indici query separati da virgole (tra 1 e 63 compresi, premi invio per concludere): ")
        while hits != "":
            q=hits.split(",")
            iq(q, reldocs, title, maxres)
            hits = raw_input("\nInserisci indici query separati da virgole (tra 1 e 63 compresi, premi invio per concludere): ")
    
    
    elif sys.argv[4] == "tnn":                                                      # tot not null
        for i in num:  # Per ogni query della lista num
            tnn(i, reldocs, title, maxres)
    
    
    elif sys.argv[4] == "fqt":                                                      # find query term
        # Se si usa l'opzione -d allora si richiamano anche le funzioni iq() e tnn() per le query ottenute da fqt()
        hits = raw_input("Inerisci termini separati da virgole (premi invio per concludere): ")
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
                        print "\nNon ci sono dettagli disponibili."
                    print "#"*200
            
            if len(sys.argv) > 5 and sys.argv[5] == "-d" and len(hits)>1:
                ql = fqt(hits, num, title)
                if ql:
                    for i in ql:
                        iq([i], reldocs, title, maxres)
                        tnn(i, reldocs, title, maxres)
                        print "\n"
                else:
                    print "\nNon ci sono dettagli disponibili."
            
            hits = raw_input("\nInerisci termini separati da virgole (premi invio per concludere): ")    
    infile.close()
    ix.searcher().close()


# uso: python frq_terms_rel_docs.py cartella_indice file_query file_qrels modalita'(iq, tnn, fqt) 
# python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt iq
# python frq_terms_rel_docs.py ../indice_stop2/ query.ohsu.1-63.xml qrels.ohsu.batch.87.txt tnn





