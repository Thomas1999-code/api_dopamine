from helpers.extensions import db


class Admin(db.model):
    __tablename__ = "admin"

    ID_admin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_admin = db.Column(db.String(255))
    cognome_admin = db.Column(db.String(255))
    email_admin = db.Column(db.String(255))
    password_admin = db.Column(db.String(255))

    def serialize(self):
        return {
            "id": self.ID_admin,
            "nome": self.nome_admin,
            "cognome": self.cognome_admin,
            "email": self.email_admin,
            "password": self.password_admin,
        } 