
from datetime import timedelta
from bson import ObjectId
from pymongo import MongoClient
from flask_jwt_extended import create_access_token,create_refresh_token
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash
from datetime import datetime
import jwt
import random

database = MongoClient('mongodb://localhost:27017').Registration
users_records = database.users

feedbacks_records=database.products_with_description

class UserOperations:
    def insert_data_into_database(self, record):
        data =users_records.insert_one(record)
        record.pop('password')
        record.pop("_id")
        # payload={"data":data,"exp":datetime.utcnow()+timedelta(hours=1)}

        access_token=create_access_token(identity=record)
        refresh_token = create_refresh_token(identity=record)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Registered successfully"
        }

    def login_into_account(self,user):
        records = users_records.find({"email": user['email']})
        pass1 = [record.get("password") for record in records][0]
        hash_match = check_password_hash(pass1, user['password'])
        if hash_match:
            records = users_records.find({"email": user['email']})
            record = list(records)[0]
            record.pop("_id")
            record.pop("password")
            created_access_token = create_access_token(identity=record, fresh=True)
            refresh_token = create_refresh_token(identity=record)
            return {
                "access_token": created_access_token,
                "refresh_token": refresh_token,
                "message": "Loggined successfully"
            }
        else:
            raise BadRequest("Invalid password")

    def matching_token(self,id,email):
        data=list(users_records.find({"_id":ObjectId(id)}))
        if data[0]['email']==email:
            return "user verified"
        else:
            return "token is not belong to this user"


    def post_feedback(self,id,document):
        user=feedbacks_records.count_documents({"_id":ObjectId(id)})
        list=[]
        product_id=random.randint(1,11000)
        if product_id not in list:
            document['product_id']=str(product_id)

        if user==0:
            user=feedbacks_records.insert_one({"_id":ObjectId(id),"products_descriptions":document})
            
            return "Thanks for adding the product"
        
        else:
            user=feedbacks_records.update_one({"_id":ObjectId(id)},{"$push":{"products_descriptions":document}})
            
            return "Thanks for adding the product"
    
    def find_all_products(self):
        feedbacks=feedbacks_records.find({},{"_id":0,"products_descriptions":1})
        return list(feedbacks)
    
    def add_likes(self,user_id,id,product_id):
        data=feedbacks_records.aggregate([{"$unwind":{"path":"$products_descriptions"}},
                                          {"$match":{"_id":ObjectId(id),"products_descriptions.product_id":product_id}},
                                          {"$project":{"products_descriptions.liked_persons":1,"products_descriptions.dis_liked_persons":1}},
                                          {"$match":{"$or":[{"products_descriptions.dis_liked_persons":user_id},
                                                            {"products_descriptions.liked_persons":user_id}]}}])
        if list(data)==None:
            filter_condition = {"_id": ObjectId(id)}
            update_operation = {
                        "$inc": {"products_descriptions.$[elem].total_likes": 1},
                        "$push": {"products_descriptions.$[elem].liked_persons": user_id}
                    }
            array_filters = [{"elem.product_id":  str(product_id)}]

            product_check=feedbacks_records.find(filter_condition,{"products_descriptions.product_id":str(product_id)})
            if list(product_check)!=0:
                result=feedbacks_records.update_one(filter_condition, update_operation, array_filters=array_filters)
                return "thanks for giving the like"
            else:
                return "product_id not exists in the database records"
        else:
            return "User already mentioned his decision"     

    def add_dislikes(self,user_id,id,product_id):

        data=feedbacks_records.aggregate([{"$unwind":{"path":"$products_descriptions"}},
                                          {"$match":{"_id":ObjectId(id),"products_descriptions.product_id":product_id}},
                                          {"$project":{"products_descriptions.liked_persons":1,"products_descriptions.dis_liked_persons":1}},
                                          {"$match":{"$or":[{"products_descriptions.dis_liked_persons":user_id},
                                                            {"products_descriptions.liked_persons":user_id}]}}])
        if list(data)==None:
            filter_condition = {"_id": ObjectId(id)}
            update_operation = {
                        "$inc": {"products_descriptions.$[elem].total_dis_likes": 1},
                        "$push": {"products_descriptions.$[elem].dis_liked_persons": user_id}
                    }
            array_filters = [{"elem.product_id": str(product_id)}]

            product_check=feedbacks_records.find(filter_condition,{"products_descriptions.product_id":str(product_id)})

            if list(product_check)!=0:
                result=feedbacks_records.update_one(filter_condition,update_operation, array_filters=array_filters)
                return "sorry for your inconvience we will improve it"
            else:
                return "Product_id is not exists in the database records"
        else:
            return "User already mentioned his decision"
        
    def add_comments(self,user_id,id,product_id,comment):
        data=feedbacks_records.aggregate([{"$unwind":{"path":"$products_descriptions"}},
                                          {"$match":{"_id":ObjectId(id),"products_descriptions.product_id":product_id}},
                                          {"$project":{"products_descriptions.comments":1}},
                                          {"$match":{"products_descriptions.comments._id":user_id}}])
        
        if list(data)==None:
            filter_condition = {"_id": ObjectId(id)}
            update_operation = {"$push":{"products_descriptions.$[elem].comments":{"_id":user_id,"comment":comment}}}
            array_filters = [{"elem.product_id": str(product_id)}]
            product_check=feedbacks_records.find(filter_condition,{"products_descriptions.product_id":str(product_id)})

            if list(product_check)!=0:
                result=feedbacks_records.update_one(filter_condition,update_operation, array_filters=array_filters)
                return "thanks for your feedback"
            else:
                return "Product_id is not exists in the database records"
        else:
            return "User already mentioned his decision"
        
    def getting_id_from_token(self,email):
        user=users_records.find({"email":email})
        res=list(user)[0].get('_id')
        return res


