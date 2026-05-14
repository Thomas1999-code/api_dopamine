from helpers.extensions import db 

class Score(db.Model):
    __tablename__ = "score"

    id_score = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utente = db.Column(db.Integer, db.ForeignKey("utente.id_utente"), primary_key=True)
    score = db.Column(db.Integer)

    player = db.relationship("Utente", backref="score")
    
    def serialize(self):
        return {
            "id_score": self.id_score,
            "id_player":self.id_player,
            "valore":self.score
        }