from helpers.extensions import db 

class Cupon(db.Model):
    __tablename__ = "cupon"

    id_cupon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utente = db.Column(db.Integer, db.ForeignKey("utenti.id_utente"), primary_key=True)
    valore_cupon = db.Column(db.Integer)

    utente = db.relationship("Utente", backref="cupon")
    
    def serialize(self):
        return {
            "cupon": self.id_cupon,
            "id_utente": self.id_utente,
            "id_player":self.id_player,
            "valore":self.valore_cupon
        }