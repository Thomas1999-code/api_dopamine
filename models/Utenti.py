from helpers.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash #Libreria che mi consente di hashare la psw dell'utente

class Utente(db.Model):
    __tablename__ = "utenti"

    id_utente = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome_utente = db.Column(db.String(255))
    cognome_utente = db.Column(db.String(255))
    username_player = db.Column(db.String(255))
    n_telefono_utente = db.Column(db.Integer)
    indirizzo_utente = db.Column(db.String(255))
    descrizione_utente = db.Column(db.Text)
    data_nascita_utente = db.Column(db.String(50))
    foto_profilo_utente = db.Column(db.String(255))
    password_utente = db.Column(db.String(255), nullable=False)
    email_utente = db.Column(db.String(255), unique=True, nullable=False)

    def set_password(self, password): #Funzione che utiliza il metodo della libreria per criptare la password
        self.password_utente = generate_password_hash(password) 

    def check_password(self, password): #Controllo che la password che ricevo in ingresso sia uguale a quella hashata
        return check_password_hash(self.password_utente, password)

    def serialize(self):
        return {
            "id": self.id_utente,
            "nome": self.nome_utente,
            "cognome": self.cognome_utente,
            "username": self.username_player,
            "telefono": self.n_telefono_utente,
            "indirizzo": self.indirizzo_utente,
            "descrizione": self.descrizione_utente,
            "data": self.data_nascita_utente,
            "fotoProfio": self.foto_profilo_utente,
            "email":self.email_utente,
            "password":self.password_utente
        }