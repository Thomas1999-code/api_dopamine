from helpers.extensions import db

class Recensione(db.Model):
    __tablename__ = "recensioni"

    id_utente = db.Column(db.Integer, db.ForeignKey("utenti.id_utente"), primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey("eventi.id_evento"), primary_key=True)
    valutazione = db.Column(db.Integer)
    commento = db.Column(db.Text)

    utente = db.relationship("Utente", backref="recensioni")
    evento = db.relationship("Evento", backref="recensioni")

    def serialize(self):
        return {
            "id_utente": self.id_utente,
            "id_evento": self.id_evento,
            "valutazione": self.valutazione,
            "commento": self.commento
        }