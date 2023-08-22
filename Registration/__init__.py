from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from Registration.user_controllers import registion_namespace,feedbacks_namespace
from flask_cors import CORS

def create_app():
    app=Flask(__name__)
    authorizations = {
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            },
        }
    
    api=Api(app,doc='/swagger',security="Bearer Auth",authorizations=authorizations)

    app.config["JWT_SECRET_KEY"]="this is secret"
    jwt = JWTManager(app)
    api.add_namespace(registion_namespace)
    api.add_namespace(feedbacks_namespace)
    CORS(app)
    return app