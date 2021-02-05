Cosa contiene la cartella:
- main.py effettua il parsing del file json e popola l’ontologia
- parse_json.py definisce tutti i metodi di parsing del file json
- costs.py contiene tutte le definizioni delle costanti utilizzate in main.py
- OWL_to_json.py NON USARE è una prova nella conversione delle classi OWL in un file json.
			    creato perchè il metodo classes() fornito da owlready2 restituisce un vettore flat delle 			    classi
- ontology.json è l’ontologia convertita in json.

- data
	- Service.json è il file json di input
	-CSOntology.owl è l’ontologia base
	-CSOntologyExtended.owl è l’ontologia popolata

L’ontologia è stata modificata secondo le richieste e sono state inserite le classi Agnostic e Vendor specific, riempite con gli individui
Ogni individuo agnostic è equivalent a una lista di  individui vendor specific

modifica ObjectProperty isServiceEquivalent:
dominio = AgnosticCloudService
range = VendorSpecificCloudService
