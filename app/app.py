from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required


from securty import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = '889888'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Item, '/api/item/<string:name>')
api.add_resource(ItemList, '/api/items')
api.add_resource(UserRegister, '/api/register')


if __name__ == "__main__":
    from database import db
    db.init_app(app)
    app.run(debug=True)
