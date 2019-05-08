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

https://www.ranks.nl/stopwords

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

##### BM25F default, nessuna manipolazione del testo, numero risultati restituiti per ogni query = 1000:

|              1 Campo             |              2 Campi             |              3 Campi             |
|----------------------------------|----------------------------------|----------------------------------|
| num_q              all    63     | num_q              all    63     | num_q              all    63     |
| num_ret            all    37454  | num_ret            all    57356  | num_ret            all    58456  |
| num_rel            all    670    | num_rel            all    670    | num_rel            all    670    |
| num_rel_ret        all    307    | num_rel_ret        all    387    | num_rel_ret        all    383    |
| map                all    0.1073 | map                all    0.1289 | map                all    0.1227 |


##### TF_IDF, nessuna manipolazione del testo, numero risultati restituiti per ogni query = 1000:

|              1 Campo             |              2 Campi             |              3 Campi             |
|----------------------------------|----------------------------------|----------------------------------|
| num_q              all    63     | num_q              all    63     | num_q              all    63     |
| num_ret            all    37454  | num_ret            all    57356  | num_ret            all    58456  |
| num_rel            all    670    | num_rel            all    670    | num_rel            all    670    |
| num_rel_ret        all    305    | num_rel_ret        all    380    | num_rel_ret        all    382    |
| map                all    0.0833 | map                all    0.0591 | map                all    0.0829 |

##### Considerazioni:
Il numero di documenti reperiti per tipo di schema di pesatura non differisce significativamente a seconda del numero di campi considerato, tuttavia quello che cambia evidentemente e' la precisione media che e' migliore con la combinazione BM25F a 2 campi

Alla luce dei dati osservati consideriamo come parametri BASELINE: 
* Documenti rilevanti reperiti: **387**
* Mean Average Precision: **0.1289**
