#--- importazione di interi moduli ---#
import string as str
import sys
import getopt
import os.path

#--- importazione di parti di modulo ---#
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from xml.dom.minidom import parse, parseString

#--- estrazione dei dati di un tag ---#
def gettagdata(dom,tag):
	nodes = dom.getElementsByTagName(tag)
	if nodes is None or len(nodes)==0:
		return None
	node = nodes[0]
	if node is None:
		return None
	return str.rstrip(str.lstrip(node.firstChild.data))

#--- definizione dello schema ---#
schema = Schema(I      = ID(stored=True),
				U      = NUMERIC(stored=True),
				S      = TEXT(stored=True),
				M      = TEXT,
				T      = TEXT,
				P      = TEXT,
                W      = TEXT,
                A      = TEXT)

#--- elementi XML possibili ---#
tags = ['I',
		'U',
		'S',
		'M',
		'T',
		'P',
		'W',
		'A']

#--- verifica dell'esistenza e creazione dell'indice ---#
if not os.path.exists("ohsumed_index_dir"):
	os.mkdir("ohsumed_index_dir")
	ix = create_in("ohsumed_index_dir", schema)
else:
	ix = open_dir("ohsumed_index_dir")

#--- allocazione del writer ---#
writer = ix.writer()

#--- apertura del file del documento ---#
infile = open(sys.argv[1],'r')

#--- lettura del documento ---#
text = infile.read()

#--- document object model ---#
dom = parseString(text)

#--- estrazione dei dati dal documento ---#
this_I	 	= gettagdata(dom,'I')
this_U      = gettagdata(dom,'U')
this_S		= gettagdata(dom,'S')
this_M		= gettagdata(dom,'M')
this_T	    = gettagdata(dom,'T')
this_P	    = gettagdata(dom,'P')
this_W	    = gettagdata(dom,'W')
this_A	    = gettagdata(dom,'A')

#--- indicizzazione e archiviazione del documento ---#
writer.add_document(I	 	= this_I,
				   	U   	= this_U,
				   	S		= this_S,
				   	M		= this_M,
				   	T	    = this_T,
                    P       = this_P,
                    W       = this_W,
                    A       = this_A)

#--- chiusura sicura del writer ---#
writer.commit()
