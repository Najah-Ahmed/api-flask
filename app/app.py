from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = '889888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXTENSIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)


@app.before_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return{'is_admin': True}
    return{'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def exprired_token_callback():
    return jsonify({
        'description': 'the token has expried',
        'error': 'token_expried'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature Verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missig_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access Token',
        'error': 'Authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


api.add_resource(Item, '/api/item/<string:name>')
api.add_resource(Store, '/api/store/<string:name>')
api.add_resource(User, '/api/user/<int:user_id>')
api.add_resource(ItemList, '/api/items')
api.add_resource(StoreList, '/api/stores')
api.add_resource(UserRegister, '/api/register')
api.add_resource(UserLogin, '/api/login')
api.add_resource(TokenRefresh, '/api/refresh')
api.add_resource(UserLogout, '/api/logout')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
