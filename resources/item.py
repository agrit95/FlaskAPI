from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
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

    @jwt_required(fresh=True)
    def post(self, name):
        item = ItemModel.find_item(name)
        if item:
            return {'message': f'item {name} already exists'}, 400
        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['isAdmin']:
            return {'message': 'Admin privilege required for this action'}, 401
        item = ItemModel.find_item(name)
        if item:
            item.delete_from_db()
            return {'message': f'item {name} deleted successfully'}, 200
        return {'message': 'Item not found'}, 404

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_item(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data will be available if you login'
        }, 200
