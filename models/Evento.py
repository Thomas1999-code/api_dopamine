from helpers.extensions import db 

class Evento(db.Model):
    __tablename__ = "eventi"

    id_evento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_evento = db.Column(db.String(255))
    indirizzo_evento = db.Column(db.String(255))
    descrizione_evento = db.Column(db.Text)
    prezzo_evento = db.Column(db.Integer)
    data_evento = db.Column(db.String(50))
    localita_evento = db.Column(db.String(255))
    immagine_evento = db.Column(db.String(255))
    servizi_evento = db.Column(db.Text)

    def serialize(self):
        return {
            "id": self.id_evento,
            "nome": self.nome_evento,
            "indirizzo_evento":self.indirizzo_evento,
            "descrizione": self.descrizione_evento,
            "prezzo": self.prezzo_evento,
            "data": self.data_evento,
            "localita": self.localita_evento,
            "immagine": self.immagine_evento,
            "servizi": self.servizi_evento
        }