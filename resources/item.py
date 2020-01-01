from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be empty!")
    parser.add_argument('store_id', type=int, required=True, help="Each item needs a store!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'error': 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'error': "An item with the name '{}' is already exist".format(name)}, 400

        request_data = self.parser.parse_args()
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {'error': 'something went wrong from our side while trying to insert the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {'success': 'item deleted'}, 200
        return {'error': 'item not found'}, 404

    def put(self, name):
        request_data = self.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        if item:
            item.price = request_data['price']
            item.store_id = request_data['store_id']
        else:
            item = ItemModel(name, **request_data)
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
