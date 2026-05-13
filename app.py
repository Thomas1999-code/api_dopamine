import os
from flask import Flask, make_response, jsonify
from helpers.extensions import db
from controllers.eventi_controller import eventi_bp
from controllers.utenti_controller import utenti_bp
from controllers.preferiti_controller import preferiti_bp
from controllers.recensioni_controller import recensioni_bp

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dopamine'
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(eventi_bp)
app.register_blueprint(utenti_bp)
app.register_blueprint(recensioni_bp)
app.register_blueprint(preferiti_bp)

@app.route("/")
def home():
    return {"message": "API_DOPAMINE online"}

@app.route("/health", methods=['GET'])
def connection():
    try:
        return jsonify({"message" : "Connected"}), 200
    except Exception:
        return jsonify({"error" : "Internal server error"}), 500
    
    
# @app.errorhandler(400)
# def handle_bad_request(error):
#     message = getattr(error, 'description', 'Bad request')
#     return make_response(jsonify({'error': message}), 400)

# @app.errorhandler(404)
# def handle_not_found(error):
#     message = getattr(error, 'description', 'Not found')
#     return make_response(jsonify({'error': message}), 404)

# @app.errorhandler(500)
# def handle_server_error(error):
#     message = getattr(error, 'description', 'Internal server error')
#     return make_response(jsonify({'error': message}), 500)

if __name__ == "__main__":
    app.run(debug=True)