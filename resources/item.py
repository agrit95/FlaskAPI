from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="can't be empty")
    parser.add_argument('store_id', type=int, required=True,
                        help="please associate the item with a store")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        item = ItemModel.find_item(name)
        if item:
            return {'message': f'item {name} already exists'}, 400
        data = self.parser.parse_args()
        price = data['price']
        store_id = data['store_id']
        item = ItemModel(name, price, store_id)
        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item(name)
        if item:
            item.delete_from_db()
            return {'message': f'item {name} deleted successfully'}, 200
        return {'message': 'Item not found'}, 404

    def put(self, name):
        data = self.parser.parse_args()
        price = data['price']
        # store_id = data['store_id']
        item = ItemModel.find_item(name)
        if item:
            item.price = price
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):

    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
