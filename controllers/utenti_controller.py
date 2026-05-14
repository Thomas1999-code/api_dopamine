from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.Utenti import Utente
from datetime import datetime, timedelta
from helpers.extensions import db
from flask_jwt_extended import ( #Librerie per la gestione dei token
    create_access_token,
    jwt_required,
    get_jwt_identity
)

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
    

#Ottegno l'utente in base al suo nome       
@utenti_bp.route("/api/users/<string:nome_utente>", methods=['GET'])
def get_user_by_name(nome_utente:str):
    try:
        users = Utente.query.filter(nome_utente).all()

        if not users:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([u.serialize() for u in users]) 
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    

#Login del Utente   
@utenti_bp.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing fields"}), 400

        user = Utente.query.filter_by(email_utente=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        #Utilizzo di un token per memorizzare login
        token = create_access_token(identity=user.id, #Utilizzo login dell'user per la creazione del token
                                    expires_delta=timedelta(hours=2) #Imposto una durata del token di due ore
                                    ) 

        return jsonify({
            "token": token,
            "user": user.serialize()
        }), 200
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500

    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": "Internal server error"}), 500
    

#root sicura
@utenti_bp.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = Utente.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.serialize()), 200


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
        
        try:
            data_obj = datetime.strptime(data["data"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        new_user = Utente(
            nome_utente = data.get("nome"),
            cognome_utente = data.get("cognome"),
            username_player = data.get("username"),
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
        user.username_player = data.get("username", user.username_player)
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
            "username" : "username_player",
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

        return jsonify({"message" : "Update complted"}), 201
    
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