from helpers.extensions import db 

class Utente(db.Model):
    __tablename__ = "utenti"

    id_utente = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome_utente = db.Column(db.String(255))
    cognome_utente = db.Column(db.String(255))
    n_telefono_utente = db.Column(db.Integer)
    indirizzo_utente = db.Column(db.String(255))
    descrizione_utente = db.Column(db.Text)
    data_nascita_utente = db.Column(db.String(50))
    foto_profilo_utente = db.Column(db.String(255))
    password_utente = db.Column(db.String(255))
    email_utente = db.Column(db.String(255))

    def serialize(self):
        return {
            "id": self.id_utente,
            "nome": self.nome_utente,
            "cognome": self.cognome_utente,
            "telefono": self.n_telefono_utente,
            "indirizzo": self.indirizzo_utente,
            "descrizione": self.descrizione_utente,
            "data": self.data_nascita_utente,
            "fotoProfio": self.foto_profilo_utente,
            "password":self.password_utente,
            "email":self.email_utente
        }