# Per iniziare

Il progetto e' organizzato nelle seguenti cartelle:
* indicizzazione -> contiene i programmi per l'indicizzazione di un singolo documento e l'indicizzazione di tutti i documenti
* ricerca -> contiene i programmi per la ricerca interattiva

#Indicizzazione

Nella repository attuale e' caricata una indicizzazione che e' stata fatta secondo questo schema:

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
