from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from app.routes.chat import chat
    app.register_blueprint(chat)
    
    return app