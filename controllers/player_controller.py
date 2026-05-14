from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models.Players import Player
from models.Recensioni import Recensione
from helpers.extensions import db

player_bp = Blueprint("player", __name__)

#Ottengo tutti i player
@player_bp.route("/api/players", methods=['GET'])
def get_all_players():
    try:
        players = Player.query.all()

        if not players:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([p.serialize() for p in players])
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error" : "Internal server error"}), 500
    
#Ottengo il player in base al suo id
@player_bp.route("/api/players/<int:id_player>", methods=['GET'])
def get_player_by_id(id_player:int):
    try:
        player = Player.query.get(id_player)

        if not player:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify({player.serialize()})
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify("Internal server error"), 500
    
#Creazione di un player
@player_bp.route("/api/players", methods=["POST"])
def create_player():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error" : "missing required fileds"}), 400
        
        player = Player(
            nome_player = data.get("name")
        )

        db.session.add(player)
        db.session.commit()

        return jsonify({"message" : "player created successfully!"}), 200
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500