from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.Recensioni import Recensione
from models.Utenti import Utente
from datetime import datetime
from helpers.extensions import db


recensioni_bp = Blueprint("recensioni",__name__)


@recensioni_bp.route("/api/reviews", methods=['GET'])
def get_all_reviews():
    try:
        reviews = Recensione.query.all()

        if not reviews:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([r.serialize() for r in reviews])
    
    except SQLAlchemyError:
        return jsonify({"error" : "Database error"}), 500
    
    except Exception:
        return jsonify({"error" : "Internal server error"}), 500
    
@recensioni_bp.route("/api/reviews/<int:id_recensione>", methods=['GET'])
def get_reviews_by_id(id_recensione:int):
    try:
        review = Recensione.query.get(id_recensione)

        if not review:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify({review.serialize()})
    
    except SQLAlchemyError:
        return jsonify({"error" : "Database error"}), 500
    
    except Exception:
        return jsonify({"error" : "Internal server error"}), 500
    
@recensioni_bp.route("/api/reviews/<string:nome_utente>", methods=['GET'])
def get_reviews_by_user_name(nome_utente:str):
    try:
        results = Recensione.query.join(Recensione.utente)\
                    .filter(Utente.nome_utente == nome_utente)\
                    .all()

        if not results:
            return jsonify({"error" : "Not in data"}), 404
        
        return jsonify([r.serialize() for r in results])
    
    except SQLAlchemyError:
        return jsonify({"error" : "Database error"}), 500
    
    except Exception:
        return jsonify({"error" : "Internal server error"}), 500
    
    
@recensioni_bp.route("/api/reviews", methods=['POST'])
def create_review():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400
        
        required_fileds = [
            "id_utente", "id_evento","valutazione", "descrizione"
            ]
        
        misssing = [f for f in required_fileds if f not in data]
        if misssing:
            return jsonify({"error" : f"Missing fields: {misssing}"}), 400
        
        new_review = Recensione(
            id_utente = data.get("id_utente"),
            id_evento = data.get("id_evento"),
            valutazione = data.get("valutazione"),
            commento = data.get("descrizione")
        )

        db.session.add(new_review)
        db.session.commit()

        return jsonify({"message" : "Review added succesfully"}), 201

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception:
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500
    
@recensioni_bp.route("/api/reviews/<int:id_recensione>", methods=['PATCH'])
def update_review_patch(id_recensione):
    try:
        review = Recensione.query.get(id_recensione)

        if not review:
            return jsonify({"error" : "Not found"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400

        required_fields = {
            "id_utente":"id_utente_recensione", 
            "id_evento":"id_evento_recensione", 
            "valutazione":"valutazione_recensione",
            "commento":"descrizione_recensione", 
        }

        for key_filed, value_filed in required_fields.item():
            if key_filed in data:
                setattr(review,value_filed,data[key_filed])

        db.session.commit()

        return jsonify({"message" : "Uptede completed successfully"}), 201

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception:
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500
    
@recensioni_bp.route("/api/reviews/<int:id_recensione>", methods=['DELETE'])
def delete_reviews(id_recensione):
    try:
        review = Recensione.query.get(id_recensione)

        if not review:
            return jsonify({"error" : "Not found"}), 404
        
        db.session.delete(review)
        db.session.commit()

        return jsonify({"message" : "Review deleted successfully"}), 201

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception:
        db.session.rollback()
        return jsonify({"error" : "Internel server error"}), 500