<<<<<<< HEAD
Ogni sottocartella ha un file README che contiene le
indicazioni su come fare funzionare i programmi per la
ricerca, benchmarking e indicizzazione.
=======
# Sistema IR per reperimento dalla collezione sperimentale OHSUMED

Questo progetto tratta la realizzazione at-
traverso il pacchetto Whoosh, di un motore di ricerca volto al reperimen-
to di documenti della collezione sperimentale OHSUMED indicizzata
opportunamente. Il progetto anche corredato di un webserver che per-
mette all’utente di interrogare il motore di ricerca in forma interattiva
attraverso un browser a scelta.


## Installazione

Usare [git](https://git-scm.com/downloads) per clonare il progetto, nella cartella scelta.

```bash
git clone https://github.com/mastershef/information_retrieval.git
```

## Prerequisiti

```bash
 pip install whoosh paginate-whoosh web.py scipy
```

## Utilizzo
Il progetto è suddiviso in quattro sotto-cartelle, per ognuna di esse si ha un file README che descrive le funzionalità e il modo di utilizzare i rispettivi programmi.
Le quattro cartelle sono descritte brevemente inseguito
* Indicizzazione: contiene i programmi dedicati alla creazione degli indici e la collezione sperimentale utilizzata.
* Ricerca: contiene i programmi per effettuare il reperimento e le  query sperimentali.
* Benchmarking: contiene il pacchetto di trec_eval compresso, le cartelle in cui vengono salvati i risultati, i programmi per la valutazione delle run e  il file dei documenti rilevanti.
* Analisi_frequenze: contiiene i programmi utilizzati per cercare le stopword utilizzate nella terza prova degli esperimenti.

Per far funzionare i comandi riportati nei README delle sottocartelle  è necessario essere nellacartella principale della repository:
```bash
cd .../..
```

## Supporto
Per eventuali dubbi sul codice inviare una mail ad uno tra i seguenti indirizzi:



## Autori

>>>>>>> 488e033224840a100b1902c9139a26fc76eaa999
