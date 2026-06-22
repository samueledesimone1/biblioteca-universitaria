# Biblioteca Universitaria

Sistema informativo per la gestione di una biblioteca universitaria, realizzato con Django, SQLite e Bootstrap.

## Funzionalità implementate

- Visualizzazione del catalogo libri con scheda dettagliata
- Registrazione e autenticazione utenti differenziati per ruolo (studente/docente)
- Ricerca nel catalogo per titolo, autore o categoria
- Gestione dei prestiti (assegnazione e restituzione)
- Inserimento e consultazione recensioni
- Visualizzazione e iscrizione agli eventi culturali

## Requisiti

- Python 3.10+
- Django 6.x
- Git

## Installazione e avvio

1. Clona il repository e spostati nella cartella
2. Crea e attiva il virtual environment: python3 -m venv venv && source venv/bin/activate
3. Installa le dipendenze: pip install django
4. Applica le migrazioni: python3 manage.py migrate
5. Carica i dati di esempio: python3 manage.py loaddata fixtures/initial_data.json
6. Avvia il server: python3 manage.py runserver
7. Apri il browser su http://127.0.0.1:8000

## Credenziali di esempio

- Studente: username mario.rossi, password Biblioteca2024!
- Docente: username prof.bianchi, password Biblioteca2024!

## Struttura del progetto

- biblioteca/ — configurazione Django
- catalogo/ — app principale con modelli, viste e template
- fixtures/ — dati di esempio