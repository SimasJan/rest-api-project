from typing import Dict
from venv import create
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users.")

@blp.route('/register')
class UserRegister(MethodView):
    
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # if there is at least 1 row, abort the request.
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(409, message="A user with that username already exists.")
        
        user = UserModel(
            username=user_data['username'],
            password=pbkdf2_sha256.hash(user_data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully.'}


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data) -> Dict:
        """Authenticate an user with the details from the `user_data` and return an `access_token`, otherwise 401 exception."""
        user = UserModel.query.filter(UserModel.username == user_data['username']).first()
        # verify the password for the user.
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            acces_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': acces_token, 'refresh_token': refresh_token}

        abort(401, message="Invalid credentials provided.")


@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'acces_token': new_token}

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        """Logout the user from the session."""
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'Successfully logged out.'}


@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    # @blp.response(200, UserSchema)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted.'}