# Per iniziare

Il progetto e' organizzato nelle seguenti cartelle:
* indicizzazione -> contiene i programmi per l'indicizzazione di un singolo documento e l'indicizzazione di tutti i documenti
* ricerca -> contiene i programmi per la ricerca interattiva

# Indicizzazione

Nella repository attuale e' caricata un indice che e' stato fatto secondo questo schema:

```python
schema = Schema(I 	= ID(stored=True),
		U      	= NUMERIC(stored=True),
		S      	= TEXT(stored=True),
		M      	= TEXT,
		T      	= TEXT,
		P      	= TEXT,
                W      	= TEXT,
                A      	= TEXT)

```

Nel caso in cui questo schema non vada bene, semplicemente bisogna andare nel
file ```/indicizzatore/indicizzatore_batch.py``` modificarlo e lanciarlo.

Attenzione: Il file indicizzatore_batch si aspetta un file oshumed.87.xml, che
bisogna estrarre dallo zip contenuto nella cartella indicizzatore

I tempi di indicizzazione su un processore Dual Core sono stati di circa 10 minuti.


