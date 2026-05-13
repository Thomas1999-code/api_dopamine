from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.Utenti import Utente
from datetime import datetime
from helpers.extensions import db

utenti_bp = Blueprint("utenti", __name__)

#Ottengo tutti gli utenti memorizzati nel mio database
@utenti_bp.route("/api/users", methods=['GET'])
def get_all_users():
    try:
        users = Utente.query.all()

        if not users:
            return jsonify({"error" : "Not found"}), 404

        return jsonify([u.serialize() for u in users])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500

#Ottengo l'utente in base al suo id       
@utenti_bp.route("/api/users/<int:id_utente>", methods=['GET'])
def get_user_by_id(id_utente:int):
    try:
        user = Utente.query.get(id_utente)

        if not user:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify(user.serialize()) 
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    
#Creazione di un nuovo utente
@utenti_bp.route("/api/users", methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400

        required_fileds = [
            "nome","cognome","telefono",
            "descrizione", "data", "immagine"
            ]
        
        missing = [r for r in required_fileds if r not in data]
        if missing:
            return jsonify({"error": f"Missing fileds {missing}"}), 400

        new_user = Utente(
            nome_utente = data.get("nome"),
            cognome_utente = data.get("cognome"),
            n_telefono_utente = data.get("telefono"),
            descrizione_utente = data.get("descrizione"),
            indirizzo_utente = data.get("indirizzo"),
            data_nascita_utente = data.get("data"),
            foto_profilo_utente = data.get("immagine"),
            email_utente = data.get("email"),
            password_utente = data.get("password")
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.serialize()), 201
    
    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500

#Update completo di un utente 
@utenti_bp.route("/api/users/<int:id_utente>", methods=['PUT'])
def uptade_user_put(id_utente:int):
    try:
        user = Utente.query.get(id_utente)

        if not user:
            return jsonify({"error" : "Not found"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400

        user.nome_utente = data.get("nome", user.nome_utente)
        user.cognome_utente = data.get("cognome", user.cognome_utente)
        user.descrizione_utente = data.get("descrizione", user.descrizione_utente)
        user.n_telefono_utente = data.get("telefono", user.telefono_utente)
        user.foto_profilo_utente = data.get("immagine", user.immagine_utente)
        user.email_utente = data.get("email", user.email_utente)
        user.password_utente = data.get("password", user.password_utente)
        user.indirizzo_utente = data.get("indirizzo", user.indirizzo_utente)

        if data.get("data"):
            user.data_nascita_utente = datetime.strptime(
                    data["data"], "%Y-%m-%d"
                ).date()

        db.session.commit()

        return jsonify(user.seralize()), 201
    
    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500

    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500

#Update parziale di un singolo campo in base all' id  
@utenti_bp.route("/api/users/<int:id_utente>", methods=['PATCH'])
def update_user_patch(id_utente:int):
    try:
        user = Utente.query.get(id_utente)

        if not user:
            return jsonify({"error" : "Not found"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400

        required_fileds = {
            "nome" : "nome_utente", 
            "cognome" : "cognome_utente",
            "indirizzo" : "indirizzo_utente",
            "telefono" : "n_telefono_utente",
            "data" : "data_nascita_utente",
            "immagine" : "immagine_utente",
            "descrizone" : "descrizione_utente",
            "email" : "email_utente",
            "password" : "password_utente"
        }

        for key_filed, value_filed in required_fileds.items():
            if key_filed in data:
                if key_filed == 'data':
                    setattr(
                        user,
                        value_filed,
                        datetime.strptime(data['data'], "%Y-%m-%d").data()
                    )
                else:
                    setattr(user, value_filed, data[key_filed])

        db.session.commit()

        return jsonify({"message" : "Uptede complted"}), 201
    
    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500

    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500

#Eliminazione di un utenti in base all'id   
@utenti_bp.route("/api/users/<int:id_utente>", methods=['DELETE'])
def delete_user(id_utente:int):
    try:
        user = Utente.query.get(id_utente)

        if not user:
            return jsonify({"error" : "Not found"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message" : "Delete completed successfully"}), 201
    
    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500

    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500