from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models.Utenti import Utente
from models.Cupons import Cupon 
from helpers.extensions import db

cupon_bp = Blueprint("cupon", __name__)

#Ottengo tutti i cupon
@cupon_bp.route("/api/cupons", methods=['GET'])
def get_all_cupons():
    try:
        cupons = Cupon.query.all()

        if not cupons:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([c.serialize() for c in cupons])
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"erorr" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ")
        return jsonify({"error" : "Internal server error"}), 500
    

#Ottengo il cupon in base all'id
@cupon_bp.route("/api/cupons/<int:id_cupon>", methods=['GET'])
def get_cupon_by_id(id_cupon:int):
    try:
        cupon = Cupon.query.get(id_cupon)
        
        if not cupon:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify(cupon.serialize())
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({"Internal server error"}), 500
    

#Creazione di un nuovo cupon
@cupon_bp.route("/api/cupons", methods=['POST'])
def create_cupon():
    try:
        data = request.get_json()

        required_fileds = {"id_utente", "valore_cupon"}
        miss = [f for f in required_fileds if f not in data]
        if miss:
            return jsonify({"error" : f"{miss} is required!"}), 400
            
        new_cupon = Cupon(
            id_utente = data.get("id_utente"),
            valore_cupon = data.get("valore_cupon")
        )

        db.session.add(new_cupon)
        db.session.commit()

        return jsonify({
            "message" : "cupon created successfully!",
            "cupon" : new_cupon.serialize()
        }), 201
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500