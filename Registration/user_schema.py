
from marshmallow import fields, Schema,validate
from Registration.validator import checking_spaces,email,validate_match_password, checking_email

class Userdetails(Schema):
    first_name=fields.String(validate=[checking_spaces,validate.Length(min=3,max=50),
                                       validate.Regexp(r'[A-Za-z0-9]',error=("the string will take only alphabetics and digits"))],required=True)
    last_name=fields.String(validate=[checking_spaces,validate.Length(min=3,max=50),
                                       validate.Regexp(r'[A-Za-z0-9]',error=("the string will take only alphabetics and digits"))],required=True)
    email=fields.Email(validate=email,required=True)
    
    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=50),
            validate.Regexp(r'^(?=.*[A-Z])(?=.*[@#$%^&+=])(?=.*[0-9]).*$')
        ],
        load_only=True
    )
    confirm_password=fields.String(validate=validate_match_password,required=True,load_only=True)

class AfterRegistration(Schema):
    access_token=fields.String()
    refresh_token=fields.String()
    message=fields.String()

class userLogin(Schema):
    email = fields.Email(validate=checking_email, required=True)
    password = fields.String(
        required=True,
        validate= [
            validate.Length(min=8, max=50),
            validate.Regexp(r'^(?=.*[A-Z])(?=.*[@#$%^&+=])(?=.*[0-9]).*$')
        ],
        load_only=True
    )

class AfterLogin(Schema):
    access_token = fields.String()
    refresh_token = fields.String()
    message = fields.String()

class Feedback_form(Schema):
    description=fields.String(required=True)
    id=fields.String(required=True)