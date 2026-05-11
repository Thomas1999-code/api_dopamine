# API DOPAMINE

REST API sviluppata in Python con Flask e SQLAlchemy per la gestione di eventi.
Il database è PostgreSQL hostato su Supabase.

Questa API è pensata per essere consumata da applicazioni client (es. app Android).

---

## 🚀 Tecnologie utilizzate

- Python 3
- Flask
- Flask-SQLAlchemy
- PostgreSQL (Supabase)
- psycopg2
- Gunicorn (deploy su Render)

---

## 🏗️ Struttura del progetto

API_DOPAMINE/
│
├── controllers/ # Endpoint REST API
├── models/ # Modelli SQLAlchemy (tabelle DB)
├── helpers/ # Configurazioni e extensions (db setup)
├── app.py # Entry point dell'app Flask
├── requirements.txt # Dipendenze Python
├── .gitignore # File ignorati da Git

---

## 🔌 Database

Il database utilizzato è PostgreSQL su Supabase.

Connessione gestita tramite SQLAlchemy.

Esempio URI:

postgresql+psycopg2://user:password@host:5432/postgres

---

## Endpoint principali

🔹 Health check

GET /health

---

## Verifica connessione API + database.

🔹 Eventi
GET    /api/events
GET    /api/events/<id>
POST   /api/events
PUT    /api/events/<id>
PATCH  /api/events/<id>
DELETE /api/events/<id>

🔹 Filtri eventi
GET /api/events/name/<nome>
GET /api/events/location/<localita>
GET /api/events/price?min=&max=
GET /api/events/date?min_date=&max_date=

---

## 🧪 Esecuzione in locale

Creare ambiente virtuale:

python -m venv my_venv

Attivare ambiente:
my_venv\Scripts\activate   # Windows

Installare dipendenze:
pip install -r requirements.txt

Avviare server:
python app.py

---

## 🌐 Deploy

L’API è pensata per essere deployata su piattaforme come:

Render
Railway
Fly.io

---

## 📱 Utilizzo

Questa API può essere consumata da:

applicazioni Android
frontend web
sistemi esterni

Base URL esempio:

https://your-api.onrender.com

---

## 🔐 Note di sicurezza
Le credenziali del database NON sono hardcoded
Utilizzo di variabili d'ambiente per produzione
Connessione sicura tramite SSL (Supabase)