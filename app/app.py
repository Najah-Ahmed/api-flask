from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required

from securty import authenticate, identity

from user import UserRegister

from item import Item, ItemList
app = Flask(__name__)
app.secret_key = '889888'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Item, '/api/item/<string:name>')
api.add_resource(ItemList, '/api/items')
api.add_resource(UserRegister, '/api/register')


if __name__ == "__main__":
    app.run(debug=True)
