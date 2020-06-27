from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True, help="This field is required"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return{'Message': "Item not Found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item name {} already exist.'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {"message": "AN ERROR OCCURRED INSTERING THE ITEM"}, 500

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,  data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "AN ERROR OCCURRED INSTERING THE ITEM"}, 500

        else:
            try:
                updated_item.update()
            except:
                return {"message": "AN ERROR OCCURRED UPDATE THE ITEM"}, 500
        return updated_item.json(), 201


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return{'items': items}
