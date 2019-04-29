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

### NOTA: il numero di run dipende dal numero di variabili considerate e dal numero di valori che possono assumere, per esempio se proviamo due indici diversi e tre combinazini di parametri diverse per il BM25 abbiamo 2x3 run 
 
# Ricerca 

In questo paragrafo metteremo i risultati temporanei ottenuti con le varie RUN che poi dovranno essere formattate per bene e inserite nel documento finale.

####Baseline RUN
A un campo: 
``` python ricerca_batch.py ../ohsumed_index_dir/ query.ohsu.1-63.xml 1 > BASELINE_UN_CAMPO.RUN ```

A due campi: 
``` python ricerca_batch.py ../ohsumed_index_dir/ query.ohsu.1-63.xml 2 > BASELINE_DUE_CAMPI.RUN ```
