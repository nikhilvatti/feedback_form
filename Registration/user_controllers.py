
from flask import request, jsonify
from flask_restx import Resource,Namespace
from flask_accepts import accepts,responds
from Registration.user_schema import Userdetails,AfterRegistration,userLogin,AfterLogin,Feedback_form
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from Registration.user_repository import UserOperations
from flask_jwt_extended import jwt_required,get_jwt_identity

import base64

registion_namespace=Namespace("registration",description="namsepace for registration")
feedbacks_namespace=Namespace('feedbacks',description='namespace for feedbacks')

@registion_namespace.route("/register")
class UserRegistration(Resource):
    @accepts(schema=Userdetails,api=registion_namespace)
    @responds(schema=AfterRegistration,api=registion_namespace)
    def post(self):
        user=request.json
        user['password']=generate_password_hash(user['password'])
        user.pop('confirm_password')
        user["Created_At"]=datetime.now()
        print(user)
        result = UserOperations.insert_data_into_database(self, user)
        return result

@registion_namespace.route("/login")
class UserLogin(Resource):
    @accepts(schema=userLogin,api=registion_namespace)
    @responds(schema=AfterLogin,api=registion_namespace)
    def get(self):
        user=request.json
        result=UserOperations.login_into_account(self, user)
        return result

@registion_namespace.route("/login/upload")
class post_feedback(Resource):
    @jwt_required()
    def post(self):
        description=request.form.get('description')
        image=request.files.get('image')
        id=request.form.get("id")
        image_file=image.read()
        image_encode=base64.b64encode(image_file).decode('utf-8')
        token_user=get_jwt_identity()
        result=UserOperations.matching_token(self,id,token_user.get('email'))

        if result=="user verified":
            document={"image":image_encode,"description":description,"total_dis_likes":0,"total_likes":0}
            post=UserOperations.post_feedback(self,id,document)
            return post

@registion_namespace.route("/login/all_products")
class AllProducts(Resource):
    def get(self):
        products=UserOperations.find_all_products(self)
        return products

@registion_namespace.route("/login/product/like")
class AddLike(Resource):
    @jwt_required()
    def get(self):
        data=request.json
        token_user=get_jwt_identity()
        user_id=UserOperations.getting_id_from_token(self,token_user["email"])
        result=UserOperations.add_likes(self,str(user_id),data['id'],str(data['product_id']))
        return result
    
@registion_namespace.route("/login/product/dislike")
class AddDisLike(Resource):
    @jwt_required()
    def get(self):
        data=request.json
        token_user=get_jwt_identity()
        user_id=UserOperations.getting_id_from_token(self,token_user["email"])
        result=UserOperations.add_dislikes(self,str(user_id),data['id'],str(data['product_id']))
        return result


@registion_namespace.route("/login/product/comment")
class AddComments(Resource):
    @jwt_required()
    def post(self):
        data=request.json
        token_user=get_jwt_identity()
        user_id=UserOperations.getting_id_from_token(self,token_user["email"])
        result=UserOperations.add_comments(self,str(user_id),data['id'],str(data['product_id']),data['comment'])
        return result

@registion_namespace.route("/login/product/like_dislike")
class ChangeResponse(Resource):
    @jwt_required()
    def put(self):
        data=request.json
        token_user=get_jwt_identity()
        user_id=UserOperations.getting_id_from_token(self,token_user["email"])
        result=UserOperations.change_from_like_to_dislike(self,str(user_id),data['id'],str(data["product_id"]))
        return result

@registion_namespace.route('/login/product/dislike_like')
class ChangeResponse1(Resource):
    @jwt_required()
    def put(self):
        data=request.json
        token_user=get_jwt_identity()
        user_id=UserOperations.getting_id_from_token(self,token_user["email"])
        result=UserOperations.change_from_dislike_to_like(self,str(user_id),data['id'],str(data["product_id"]))
        return result

@registion_namespace.route("/login/product/delete_comment")
class DeleteComment(Resource):
    @jwt_required()
    def put(self):
        data=request.json
        token_user=get_jwt_identity()
        user_id=UserOperations.getting_id_from_token(self,token_user["email"])
        result=UserOperations.delete_comment(self,user_id,data["id"],str(data['product_id']))
        return result

