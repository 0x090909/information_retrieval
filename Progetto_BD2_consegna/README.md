# Sistema IR per reperimento dalla collezione sperimentale OHSUMED

Questo progetto tratta la realizzazione attraverso il pacchetto Whoosh, di un motore di ricerca volto al reperimento di documenti della collezione sperimentale OHSUMED indicizzata opportunamente. 
Il progetto è anche corredato di un webserver che permette all’utente di interrogare il motore di ricerca in forma interattiva attraverso un browser a scelta.


## Installazione

Usare [git](https://git-scm.com/downloads) per clonare il progetto, nella cartella scelta.

```bash
    git clone https://github.com/mastershef/information_retrieval.git
```

## Prerequisiti
Programmi contenuti nelle sottocartelle sono scritti principalmente in python, in particolare, è stata utilizzata la versione 2.7.
Inoltre, sono stati utilizzati vari moduli: Whoosh (2.7.4), paginate-whoosh (0.3), web.py (0.39), scipy (1.2.2).

Per installare questi moduli basta utilizzare il coando:
```bash
    pip install whoosh paginate-whoosh web.py scipy
```

## Utilizzo
Il progetto è suddiviso in cinque sotto-cartelle, per ognuna di esse si ha un file README che descrive le funzionalità e il modo di utilizzare i rispettivi programmi.
Le cinque cartelle sono descritte brevemente di seguito:
* Indicizzazione: contiene i programmi dedicati alla creazione degli indici e la collezione sperimentale utilizzata.
* Ricerca: contiene i programmi per effettuare il reperimento e le  query sperimentali.
* Benchmarking: contiene il pacchetto di trec_eval compresso, le cartelle in cui vengono salvati i risultati, i programmi per la valutazione delle run e  il file dei documenti rilevanti.
* Analisi_frequenze: contiene i programmi utilizzati per cercare le stopword utilizzate nella terza prova degli esperimenti.
* Web: contiene i programmi per far funzionare il server web con le pagine relative al motore di ricerca.

Per far funzionare i comandi riportati nei README delle sottocartelle  è necessario essere nella cartella principale della repository(il percorso dipende da dove è stata clonata):
```bash
    cd .../Progetto_BD2_consegna/
```

## Supporto
Per eventuali dubbi sul codice inviare una mail ad uno tra i seguenti indirizzi:
* alessandro.stefani.6@studenti.unipd.it
* caterina.buranelli@studenti.unipd.it
* gheorghecristi.gutu@studenti.unipd.it

## Autori
Alessandro Stefani , Caterina Buranelli e Cristi Gutu

