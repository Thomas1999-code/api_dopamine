from helpers.extensions import db

class Preferito(db.Model):
    __tablename__ = "preferiti"

    id_utente = db.Column(db.Integer, db.ForeignKey("utenti.id_utente"), primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey("eventi.id_evento"), primary_key=True)

    utente = db.relationship("Utente", backref="preferiti")

    def serialize(self):
        return {
            "id_utente": self.id_utente,
            "id_evento": self.id_evento
        }
    