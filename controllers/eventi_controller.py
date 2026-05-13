from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models.Evento import Evento
from models.Recensioni import Recensione
from datetime import datetime
from helpers.extensions import db

eventi_bp = Blueprint("eventi", __name__)

#Ottengo tutti gli eventi del mio database
@eventi_bp.route("/api/events", methods=["GET"])
def get_events():
    try:
        events = Evento.query.all()

        if not events:
            return jsonify({"error": "Not found"}), 404

        return jsonify([e.serialize() for e in events])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500

#Ottengo l'evento corrispondente all'id
@eventi_bp.route("/api/events/<int:id_evento>", methods=['GET'])
def get_event_by_id(id_evento:int):
    try:
        event = Evento.query.get(id_evento)

        if not event:
            return ({"error":"Not found"}), 404
        
        return jsonify(event.serialize())
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500

#Ottengo tutti gli eventi corripondenti al nome
@eventi_bp.route("/api/events/name/<string:nome_evento>", methods=['GET'])
def get_event_by_name(nome_evento):
    try:
        if len(nome_evento) < 3:
            return jsonify({"error" : "Author lenght should be more longer"}), 400

        event = Evento.query.filter(Evento.nome_evento == nome_evento).all()

        if not event:
            return jsonify({"error": "Not found"}), 404

        return jsonify([d.serialize() for d in event])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    

#Ottengo tutti gli eventi corripondenti alla località
@eventi_bp.route("/api/events/location/<string:localita_evento>", methods=['GET'])
def get_event_by_location(localita_evento):
    try:
        if len(localita_evento) < 3:
            return jsonify({"error" : "Location event lenght should be more longer"}), 400

        event = Evento.query.filter(Evento.localita_evento == localita_evento).all()

        if not event:
            return jsonify({"error": "Not found"}), 404

        return jsonify([d.serialize() for d in event])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    
#Ottengo tutti  gli eventi in base ad un range di prezzo
@eventi_bp.route("/api/events/price", methods=['GET'])
def get_events_by_price():
    try:
        min_price = request.args.get('min', type=int)
        max_price = request.args.get('max', type=int)

        if min_price is not None and max_price is not None:
            events = Evento.query.filter(
                Evento.prezzo_evento.between(min_price,max_price)
            ).all()
        elif min_price is not None:
            events = Evento.query.filter(Evento.prezzo_evento >= min_price).all()
        elif max_price is not None:
            events = Evento.query.filter(Evento.prezzo_evento <= max_price).all()
        else:
            return jsonify({"error" : "No price filters provided"}), 400

        if not events:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([e.serialize() for e in events])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500


#Ottengo tutti gli eventi corripondenti a quella data o al mio range di date
@eventi_bp.route("/api/events/date", methods=['GET'])
def get_event_by_dateTime():
    try:
        min_date_str = request.args.get('min_date')
        max_date_str = request.args.get('max_date')

        if not min_date_str and not max_date_str:
            return jsonify({"error" : "Date is required"}), 400
        
        min_date_obj = datetime.strptime(min_date_str, "%Y-%m-%d").date()
        max_date_obj = datetime.strptime(max_date_str, "%Y-%m-%d").date()

        if min_date_obj is not None and max_date_obj is not None:
            events = Evento.query.filter(
                    Evento.data_evento.between(min_date_obj,max_date_obj)
                ).all()
        elif min_date_obj is not None:
            events = Evento.query.filter(Evento.data_evento >= min_date_obj).all()
        elif max_date_obj is not None:
            events = Evento.query.filter(Evento.data_evento <= max_date_obj).all()
        elif min_date_obj is not None and max_date_obj is not None and min_date_obj == max_date_obj:
            events = Evento.query.filter(Evento.data_evento == min_date_obj).all()
        else:
            return jsonify({"error" : "No Date filter provided"}), 400

        if not events:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([e.serialize() for e in events])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    
#Ottengo tutti gli evetnti in ordine per meglio votati
@eventi_bp.route("/api/events/rate", methods=['GET'])
def get_events_by_rate():
    try:
        events = Evento.query.join(Recensione)\
                    .group_by(Evento.id_evento)\
                        .order_by(func.avg(Recensione.valutazione).desc())\
                            .all()

        if not events:
            return jsonify({"error" : "Not fount"}), 404
        
        return jsonify([e.serialize() for e in events])
    
    except SQLAlchemyError as e:
        print("Error", e)
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error" : "Internal server error"}), 500
    
#Ottengo tutti gli eventi in base al più recente
@eventi_bp.route("/api/events/recent", methods=['GET'])
def get_event_by_date():
    try:
        events = Evento.query\
                    .order_by(Evento.data_evento.asc())\
                        .all()
        
        if not events:
            return jsonify({"error" : "Not found"}), 404
        
        return jsonify([e.serialize() for e in events])
    
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error" : "Databse error"}), 500
    
    except Exception as e:
        print(e)
        return jsonify({"error" : "Internal server error"}), 500

#Creazione di un nuovo evento
@eventi_bp.route("/api/events", methods=['POST'])
def create_event():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        required_fields = [
            "nome", "descrizione", "prezzo",
            "localita", "data", "immagine", "servizi"
        ]

        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        try:
            data_obj = datetime.strptime(data["data"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        new_event = Evento(
            nome_evento=data["nome"],
            descrizione_evento=data["descrizione"],
            prezzo_evento=data["prezzo"],
            localita_evento=data["localita"],
            data_evento=data_obj,
            immagine_evento=data["immagine"],
            indirizzo_evento=data["indirizzo"],
            servizi_evento=data["servizi"]
        )

        db.session.add(new_event)
        db.session.commit()

        return jsonify(new_event.serialize()), 201

    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    
#Update completo di un evento in base all'id
@eventi_bp.route("/api/events/<int:id_evento>", methods=['PUT'])
def update_event_put(id_evento):
    try:
        event = Evento.query.get(id_evento)

        if not event:
            return jsonify({"error" : "Not found"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400

        event.nome_evento = data.get("nome", event.nome_evento)
        event.descrizione_evento = data.get("descrizione", event.descrizione_evento)
        event.localita_evento = data.get("localita", event.localita_evento)
        event.immagine_evento = data.get("immagine", event.immagine_evento)
        event.indirizzo_evento = data.get("indirizzo", event.indirizzo_evento)
        event.prezzo_evento = data.get("prezzo", event.prezzo_evento)
        event.servizi_evento = data.get("servizi", event.servizi_evento)
        
        if data.get("data"):
            event.data_evento = datetime.strptime(
                    data["data"], "%Y-%m-%d"
                ).date()

        db.session.commit()

        return jsonify(event.seralize()), 201
    
    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500
    
#Update parziale di un solo campo in base al suo id
@eventi_bp.route("/api/events/<int:id_evento>", methods=['PATCH'])
def update_event_patch(id_evento):
    try:
        event = Evento.query.get(id_evento)

        if not event:
            return jsonify({"error" : "Not found"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"error" : "Missing JSON body"}), 400

        required_fields = {
            "nome":"nome_evento", 
            "descrizione":"descrizione_evento", 
            "prezzo":"prezzo_evento",
            "localita":"localita_evento", 
            "data":"data_evento",
            "indirizzo":"indirizzo_evento",
            "immagine":"immagine_evento",
            "servizi":"servizi_evento"
        }

        for key_filed, value_filed in required_fields.items():
            if key_filed in data:
                if key_filed == "data":
                    setattr(
                        event,
                        value_filed,
                        datetime.strptime(data[key_filed], "%Y-%m-%d").date()
                    )
                else:
                    setattr(event,value_filed,data[key_filed])

        db.session.commit()

        return jsonify({"message" : "Uptede completed successfully"}), 201

    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internal server error"}), 500


#Elimino l'evento in base al suo id
@eventi_bp.route("/api/events/<int:id_evento>", methods=['DELETE'])
def delete_event(id_evento):
    try:
        event = Evento.query.get(id_evento)

        if not event:
            return jsonify({"error" : "Not found"}), 404
        
        db.session.delete(event)
        db.session.commit()

        return jsonify({"message" : "Event deleted successfully"}), 201

    except SQLAlchemyError as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Database error"}), 500
    
    except Exception as e:
        print("Error", e)
        db.session.rollback()
        return jsonify({"error" : "Internel server error"}), 500