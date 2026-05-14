import os
from flask import Flask, jsonify
from helpers.extensions import db
from controllers.eventi_controller import eventi_bp
from controllers.utenti_controller import utenti_bp
from controllers.preferiti_controller import preferiti_bp
from controllers.recensioni_controller import recensioni_bp
from controllers.cupon_controller import cupon_bp
from controllers.scores_controller import score_bp

#dotenv serve per il funzionemnto di subabase ma solo in locale
#from dotenv import load_dotenv

#load_dotenv()

app = Flask(__name__)

#Connessione al database locale
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dopamine'

#Connessione al database online supabase attraverso l'indirizo salvato nella variebile d'ambiente nascosata su render
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") + "?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret-change-this"

db.init_app(app)

app.register_blueprint(eventi_bp)
app.register_blueprint(utenti_bp)
app.register_blueprint(recensioni_bp)
app.register_blueprint(preferiti_bp)
app.register_blueprint(score_bp)
app.register_blueprint(cupon_bp)

@app.route("/health", methods=['GET'])
def connection():
    try:
        return jsonify({"message" : "Welcome to api-dopamine"}), 200
    except Exception:
        return jsonify({"error" : "Internal server error"}), 500
 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)