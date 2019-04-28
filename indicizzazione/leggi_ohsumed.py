#leggi file xml
try:
    docs = open("ohsumed.87.xml","r") #we have a document per line

    listaDocumenti = []
    doc = ""
    i = 1
    for doc in docs:
        print "\r "+ str(i),
        listaDocumenti.append(doc)
        i = i+1
    #print listaDocumenti
except IOError as e:
    print("Couldn't open or write to file (%s)." % e)
