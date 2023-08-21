from flask import request
from marshmallow import validates,ValidationError
from Registration.user_repository import users_records

@validates(['first_name','last_name'])
def checking_spaces(value):
    if value.isspace():
        raise ValidationError("Don't enter only spaces")

@validates('email')
def email(value):
    email=users_records.count_documents({"email":value})
    if email!=0:
        raise ValidationError("email already exists in the database")
    if value[0].isalpha()==False:
        raise ValidationError("email takes uppercase at the starting character")


@validates('email')
def checking_email(value):
    email=users_records.count_documents({"email":value})
    if email==0:
        raise ValidationError("user not exists in the database records")

@validates("confirm_password")
def validate_match_password(value):
    if value!=request.json["password"]:
        raise ValidationError("password not matched")
