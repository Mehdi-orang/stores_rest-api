from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.json(), 200
        return {'error': 'store not found'}, 404

    def post(self, name):
        if StoreModel.find_store_by_name(name):
            return {'error': "A store with the name '{}' is already exists".format(name)}, 400
        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 201

    def delete(self, name):
        if StoreModel.find_store_by_name(name):
            store = StoreModel(name)
            store.delete_from_db()
            return {'success': 'store deleted successfully'}
        return {'error': 'store not found'}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
