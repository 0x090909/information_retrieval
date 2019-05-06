Per iniziare
============

Il progetto e' organizzato nelle seguenti cartelle:
* indicizzazione -> contiene i programmi per l'indicizzazione di un singolo documento e l'indicizzazione di tutti i documenti
* ricerca -> contiene i programmi per la ricerca interattiva

Indicizzazione
==============

Nella repository attuale e' caricata un indice che e' stato fatto secondo questo schema:

```python
schema = Schema(docid      	= ID(stored=True),
		title      	= TEXT(stored=True),
		identifier	= ID(stored=True),
		terms 		= NGRAM(stored=True),
		authors      	= NGRAM(stored=True),
		abstract 	= TEXT(stored=True),
		publication	= TEXT(stored=True),
		source 		= TEXT(stored=True))

```

Nel caso in cui questo schema non vada bene, semplicemente bisogna andare nel
file ```/indicizzatore/indicizzatore_batch.py``` modificarlo e lanciarlo.

Attenzione: Il file indicizzatore_batch si aspetta un file oshumed.87.xml, che
bisogna estrarre dallo zip contenuto nella cartella indicizzatore

I tempi di indicizzazione su un processore Dual Core sono stati di circa 10 minuti.

Siamo riusciti a velocizzare l'indicizzazione (con tutti i campi in stored=True) seguendo lo spunto dato dalla documentazione whoosh:
> https://whoosh.readthedocs.io/en/latest/batch.html

Abbiamo osservato che togliendo le stop word, aumenta il numero di documenti rilevanti reperiti.
Dunque, attraverso un programma apposito (cerca_stop_words.py) abbiamo creato un elenco di tutte le stop word trovate all'interno della collezione di documenti. Il criterio che abbiamo usato e' stato la lunghezza che, se inferiore o uguale a una certa soglia S, determinava l'appartenenza alla lista di stop word.
Per determinare la soglia abbiamo effettuato alcuni tentativi:
* S=4, la lista includeva troppe parole appartenenti al lessico strettamente medico (HIVs)
* S=2, la lista includeva sigle di indicatori di interesse medico (RR,CP)
* S=1, la lista includeva le lettere alfabetiche, le cifre da 0 a 9 e qualche carattere speciale ("%","$"..)
Abbiamo deciso di porre la soglia S=1, perche' parole di lunghezza maggiore sarebbero potute essere di interesse per l'utente.
All'elenco di stop word trovate come descritto sopra, abbiamo aggiunto le stop word generali per la lingua inglese (congiunizoni, articoli, avverbi) provenienti da nltk, il Natural Language Toolkit, uno degli strumenti piu' usati per fare l'analisi dei testi, scritto interamente in python.



### NOTA: il numero di run dipende dal numero di variabili considerate e dal numero di valori che possono assumere, per esempio se proviamo due indici diversi e tre combinazioni di parametri diverse per il BM25 abbiamo 2x3 run

Ricerca
=======

In questo paragrafo metteremo i risultati temporanei ottenuti con le varie RUN che poi dovranno essere formattate per bene e inserite nel documento finale.

### NOTA: come leggere il nome di file di output
* run (baseline, TFIDF..)
* numero di campi (1 o più)
* treceval
* out

#### Baseline RUN
A un campo:
```bash
python ricerca_batch.py ../ohsumed_index_dir/ query.ohsu.1-63.xml 1 > BASELINE_UN_CAMPO.RUN
```

A due campi:
```bash
python ricerca_batch.py ../ohsumed_index_dir/ query.ohsu.1-63.xml 2 > BASELINE_DUE_CAMPI.RUN
```

Output treceval
===============

##### Output treceval, 1 campo, BM25 default, nessuna manipolazione del testo, numero risultati restituiti per ogni query = 1000:
```
num_q          	all	63
num_ret        	all	37454
num_rel        	all	670
num_rel_ret    	all	307
map            	all	0.1073
gm_ap          	all	0.0055
R-prec         	all	0.1187
bpref          	all	0.4538
recip_rank     	all	0.2998
ircl_prn.0.00  	all	0.3191
ircl_prn.0.10  	all	0.2841
ircl_prn.0.20  	all	0.2028
ircl_prn.0.30  	all	0.1406
ircl_prn.0.40  	all	0.1271
ircl_prn.0.50  	all	0.1070
ircl_prn.0.60  	all	0.0637
ircl_prn.0.70  	all	0.0376
ircl_prn.0.80  	all	0.0206
ircl_prn.0.90  	all	0.0081
ircl_prn.1.00  	all	0.0069
P5             	all	0.1524
P10            	all	0.1048
P15            	all	0.1026
P20            	all	0.0905
P30            	all	0.0804
P100           	all	0.0352
P200           	all	0.0202
P500           	all	0.0092
P1000          	all	0.0049

```
#### Considerazioni:
La precisione media dei risultati del reperimento è zero quindi non è utilizzabile come baseline, in quanto poco utile.


### Output treceval BASELINE_UN_CAMPO.TRECEVAL
### Output treceval, 1 campo, TFIDF:
### Output treceval, 2 campi, TFIDF:
### Output treceval, 3 campi, TFIDF:
### Output treceval, 2 campi, BM25 default:
