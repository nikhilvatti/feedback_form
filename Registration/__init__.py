from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from Registration.user_controllers import registion_namespace,feedbacks_namespace


def create_app():
    app=Flask(__name__)

    api=Api(app,doc='/swagger')
    app.config["JWT_SECRET_KEY"]="this is secret"
    jwt = JWTManager(app)
    api.add_namespace(registion_namespace)
    api.add_namespace(feedbacks_namespace)

    return app