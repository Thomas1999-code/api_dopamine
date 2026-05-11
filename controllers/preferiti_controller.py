from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.Preferiti import Preferito
from models.Utenti import Utente
from datetime import datetime
from helpers.extensions import db


preferiti_bp = Blueprint("preferiti",__name__)


@preferiti_bp.route("/api/favorites", methods=['GET'])
def get_all_favorites():
    try:
        favorites = Preferito.query.all()

        if not favorites:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([r.serialize() for r in favorites])
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error" : "Internal server error"}), 500
    
@preferiti_bp.route("/api/favorites/<int:id_preferito>", methods=['GET'])
def get_favorites_by_id(id_preferito:int):
    try:
        favorite = Preferito.query.get(id_preferito)

        if not favorite:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify({favorite.serialize()})
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    
@preferiti_bp.route("/api/favorites/<string:nome_utente>", methods=['GET'])
def get_favorites_by_user_name(nome_utente:str):
    try:
        results = Preferito.query.join(Preferito.utente)\
                    .filter(Utente.nome_utente == nome_utente)\
                    .all()

        if not results:
            return jsonify({"error" : "Not in data"}), 404
        
        return jsonify([r.serialize() for r in results])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    
    
@preferiti_bp.route("/api/favotites", methods=['POST'])
def create_favorite():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400
        
        required_fileds = [
            "id_utente", "id_evento"
            ]
        
        misssing = [f for f in required_fileds if f not in data]
        if misssing:
            return jsonify({"error" : f"Missing fields: {misssing}"}), 400
        
        new_favorite = Preferito(
            id_utente = data.get("id_utente"),
            id_evento = data.get("id_evento")
        )

        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"message" : "Favorite added succesfully"}), 201

    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500
    
# @preferiti_bp.route("/api/reviews/<int:id_preferito>", methods=['PATCH'])
# def update_favorite_patch(id_preferito):
#     try:
#         favorite = Preferito.query.get(id_preferito)

#         if not favorite:
#             return jsonify({"error" : "Not found"}), 404
        
#         data = request.get_json()

#         if not data:
#             return jsonify({"error" : "Missing JSON body"}), 400

#         required_fields = {
#             "id_utente":"id_utente_recensione", 
#             "id_evento":"id_evento_recensione", 
#         }

#         for key_filed, value_filed in required_fields.item():
#             if key_filed in data:
#                 setattr(favorite,value_filed,data[key_filed])

#         db.session.commit()

#         return jsonify({"message" : "Uptede completed successfully"}), 201

#     except SQLAlchemyError as e:
#         print("Error", e)
#         db.session.rollback()
#         return jsonify({"error" : "Database error"}), 500
    
#     except Exception as e:
#         print("Error", e)
#         db.session.rollback()
#         return jsonify({"error" : "Internal server error"}), 500
    
@preferiti_bp.route("/api/favorites/<int:id_preferito>", methods=['DELETE'])
def delete_favorite(id_preferito):
    try:
        favorite = Preferito.query.get(id_preferito)

        if not favorite:
            return jsonify({"error" : "Not found"}), 404
        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message" : "Favorite deleted successfully"}), 201

    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internel server error"}), 500