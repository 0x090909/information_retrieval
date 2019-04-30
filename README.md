# Per iniziare

Il progetto e' organizzato nelle seguenti cartelle:
* indicizzazione -> contiene i programmi per l'indicizzazione di un singolo documento e l'indicizzazione di tutti i documenti
* ricerca -> contiene i programmi per la ricerca interattiva

# Indicizzazione

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

### NOTA: il numero di run dipende dal numero di variabili considerate e dal numero di valori che possono assumere, per esempio se proviamo due indici diversi e tre combinazioni di parametri diverse per il BM25 abbiamo 2x3 run

# Ricerca

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

### Output treceval BASELINE_UN_CAMPO.TRECEVAL
```c
  num_q          	all	63
	num_ret        	all	630
	num_rel        	all	2823
	num_rel_ret    	all	0
	map            	all	0.0000
	gm_ap          	all	0.0000
	R-prec         	all	0.0000
	bpref          	all	0.0000
	recip_rank     	all	0.0000
	ircl_prn.0.00  	all	0.0000
	ircl_prn.0.10  	all	0.0000
	ircl_prn.0.20  	all	0.0000
	ircl_prn.0.30  	all	0.0000
	ircl_prn.0.40  	all	0.0000
	ircl_prn.0.50  	all	0.0000
	ircl_prn.0.60  	all	0.0000
	ircl_prn.0.70  	all	0.0000
	ircl_prn.0.80  	all	0.0000
	ircl_prn.0.90  	all	0.0000
	ircl_prn.1.00  	all	0.0000
	P5             	all	0.0000
	P10            	all	0.0000
	P15            	all	0.0000
	P20            	all	0.0000
	P30            	all	0.0000
	P100           	all	0.0000
	P200           	all	0.0000
	P500           	all	0.0000
	P1000          	all	0.0000
```
#### Considerazioni:
La precisione media dei risultati del reperimento è zero quindi non è utilizzabile come baseline, in quanto poco utile.

### Output treceval, 1 campo, TFIDF:
```c
  num_q          	all	63
	num_ret        	all	630
	num_rel        	all	2823
	num_rel_ret    	all	0
	map            	all	0.0000
	gm_ap          	all	0.0000
	R-prec         	all	0.0000
	bpref          	all	0.0000
	recip_rank     	all	0.0000
	ircl_prn.0.00  	all	0.0000
	ircl_prn.0.10  	all	0.0000
	ircl_prn.0.20  	all	0.0000
	ircl_prn.0.30  	all	0.0000
	ircl_prn.0.40  	all	0.0000
	ircl_prn.0.50  	all	0.0000
	ircl_prn.0.60  	all	0.0000
	ircl_prn.0.70  	all	0.0000
	ircl_prn.0.80  	all	0.0000
	ircl_prn.0.90  	all	0.0000
	ircl_prn.1.00  	all	0.0000
	P5             	all	0.0000
	P10            	all	0.0000
	P15            	all	0.0000
	P20            	all	0.0000
	P30            	all	0.0000
	P100           	all	0.0000
	P200           	all	0.0000
	P500           	all	0.0000
	P1000          	all	0.0000
```
### Output treceval, 2 campi, TFIDF:
```c
  num_q          	all	63
	num_ret        	all	630
	num_rel        	all	2823
	num_rel_ret    	all	0
	map            	all	0.0000
	gm_ap          	all	0.0000
	R-prec         	all	0.0000
	bpref          	all	0.0000
	recip_rank     	all	0.0000
	ircl_prn.0.00  	all	0.0000
	ircl_prn.0.10  	all	0.0000
	ircl_prn.0.20  	all	0.0000
	ircl_prn.0.30  	all	0.0000
	ircl_prn.0.40  	all	0.0000
	ircl_prn.0.50  	all	0.0000
	ircl_prn.0.60  	all	0.0000
	ircl_prn.0.70  	all	0.0000
	ircl_prn.0.80  	all	0.0000
	ircl_prn.0.90  	all	0.0000
	ircl_prn.1.00  	all	0.0000
	P5             	all	0.0000
	P10            	all	0.0000
	P15            	all	0.0000
	P20            	all	0.0000
	P30            	all	0.0000
	P100           	all	0.0000
	P200           	all	0.0000
	P500           	all	0.0000
	P1000          	all	0.0000
```
### Output treceval, 3 campi, TFIDF:
```c
  num_q          	all	63
	num_ret        	all	630
	num_rel        	all	2823
	num_rel_ret    	all	0
	map            	all	0.0000
	gm_ap          	all	0.0000
	R-prec         	all	0.0000
	bpref          	all	0.0000
	recip_rank     	all	0.0000
	ircl_prn.0.00  	all	0.0000
	ircl_prn.0.10  	all	0.0000
	ircl_prn.0.20  	all	0.0000
	ircl_prn.0.30  	all	0.0000
	ircl_prn.0.40  	all	0.0000
	ircl_prn.0.50  	all	0.0000
	ircl_prn.0.60  	all	0.0000
	ircl_prn.0.70  	all	0.0000
	ircl_prn.0.80  	all	0.0000
	ircl_prn.0.90  	all	0.0000
	ircl_prn.1.00  	all	0.0000
	P5             	all	0.0000
	P10            	all	0.0000
	P15            	all	0.0000
	P20            	all	0.0000
	P30            	all	0.0000
	P100           	all	0.0000
	P200           	all	0.0000
	P500           	all	0.0000
	P1000          	all	0.0000
```

### Output treceval, 2 campi, BM25 default:
```
	num_q          	all	63
	num_ret        	all	630
	num_rel        	all	2823
	num_rel_ret    	all	1
	map            	all	0.0000
	gm_ap          	all	0.0000
	R-prec         	all	0.0003
	bpref          	all	0.0003
	recip_rank     	all	0.0018
	ircl_prn.0.00  	all	0.0018
	ircl_prn.0.10  	all	0.0000
	ircl_prn.0.20  	all	0.0000
	ircl_prn.0.30  	all	0.0000
	ircl_prn.0.40  	all	0.0000
	ircl_prn.0.50  	all	0.0000
	ircl_prn.0.60  	all	0.0000
	ircl_prn.0.70  	all	0.0000
	ircl_prn.0.80  	all	0.0000
	ircl_prn.0.90  	all	0.0000
	ircl_prn.1.00  	all	0.0000
	P5             	all	0.0000
	P10            	all	0.0016
	P15            	all	0.0011
	P20            	all	0.0008
	P30            	all	0.0005
	P100           	all	0.0002
	P200           	all	0.0001
	P500           	all	0.0000
	P1000          	all	0.0000
```
### Output treceval, 2 campi, BM25 default:
```c
  num_q          	all	63
	num_ret        	all	630
	num_rel        	all	2823
	num_rel_ret    	all	0
	map            	all	0.0000
	gm_ap          	all	0.0000
	R-prec         	all	0.0000
	bpref          	all	0.0000
	recip_rank     	all	0.0000
	ircl_prn.0.00  	all	0.0000
	ircl_prn.0.10  	all	0.0000
	ircl_prn.0.20  	all	0.0000
	ircl_prn.0.30  	all	0.0000
	ircl_prn.0.40  	all	0.0000
	ircl_prn.0.50  	all	0.0000
	ircl_prn.0.60  	all	0.0000
	ircl_prn.0.70  	all	0.0000
	ircl_prn.0.80  	all	0.0000
	ircl_prn.0.90  	all	0.0000
	ircl_prn.1.00  	all	0.0000
	P5             	all	0.0000
	P10            	all	0.0000
	P15            	all	0.0000
	P20            	all	0.0000
	P30            	all	0.0000
	P100           	all	0.0000
	P200           	all	0.0000
	P500           	all	0.0000
	P1000          	all	0.0000
```
