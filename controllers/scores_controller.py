from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models.Utenti import Utente
from models.Scores import Score
from helpers.extensions import db

score_bp = Blueprint("score", __name__)

#Ottengo tutti gli score
@score_bp.route("/api/score", methods=['GET'])
def get_all_scores():
    try:
        scores = Score.query.all()

        if not scores:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([s.serialize() for s in scores])
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error" : "Internal server error"}), 500
    

#Ottengo il punteggio in base al suo id
@score_bp.route("/api/scores/<int:id_score>", methods=['GET'])
def get_score_by_id(id_score:int):
    try:
        score = Score.query.get(id_score)

        if not score:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify(score.serialize())
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify("error", "Internal server error"), 500
    

#Ottengo tutti i punteggi e gli username annessi
@score_bp.route("/api/scores/username", methods=['GET'])
def get_all_scores_usernames():
    try:
        results = db.session.query(
                    Utente.username_player,
                    Score.punteggio
                        ).join(
                            Score,
                            Utente.id_utente == Score.id_utente
                            ).all()

        response = []

        for row in results:
            response.append({
                "username": row.username,
                "punteggio": row.punteggio
            })

        return jsonify(response), 200

    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error" : "Internal server error"}), 500
    
    
#Unisco le tabelle player e la tabella score
@score_bp.route("/api/score/player", methods=['GET'])
def get_score_plyer():
    try:
        score_players = Score.query.join(
                            Score, Utente.id_utente == Score.id_utente
                            ).all()
        
        if not score_players:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify({
            "id_utente" : Utente.id_utente,
            "username" : Utente.username_player,
            "id_score" : Score.id_score,
            "score " : Score.score
        })
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error" : "Database error"}), 500
     
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error" : "Internal server error"}), 500
    
    
#metto in ordine crescente tutti i punteggi con username annesso
@score_bp.route("/api/scores", methods=['GET'])
def asc_scores():
    try:
        scores = Score.query(
                    Utente.username_player,
                    Score.Score
                    ).join(
                        Utente,
                        Utente.id_utente == Score.id_utente
                        ).filter(Score.score.asc()).all()

        if not scores:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify({
            "username" : Utente.username_player,
            "score" : Score.score
        })
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        return jsonify({"error", "Database error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error" : "Internal server error"}), 500
    

#Creazione di un nuovo punteggio
@score_bp.route("/api/scores", methods=['POST'])
def cerate_score():
    try:
        data = request.get_json()

        required_fileds = {"id_utente, score"}
        miss = [f for f in required_fileds if f not in data]
        if miss:
            return jsonify({"error" : f"{miss} is required!"}), 400
        
        new_score = Score(
            id_player = data.get("id_player"),
            score = data.get("score")
        )

        db.session.add(new_score)
        db.session.commit()

        return jsonify({
            "message" : "Score created successfully",
            "score" : new_score.serialize()
        })
    
    except SQLAlchemyError as e:
        print("Error: ", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500
    
    except Exception as e:
        print("Error: ", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500