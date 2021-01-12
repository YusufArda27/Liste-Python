from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import shelve
import json
app = Flask(__name__)
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open('list.db')
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/')
def home_page():
    return 'Hello, World!'



class List(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        articles = list()
        for key in keys:
            articles.append(shelf[key])
        return {'data':articles}
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id',required=True)
        parser.add_argument('Author',required=True)
        parser.add_argument('Context',required=True)

        args = parser.parse_args()

        shelf=get_db()
        shelf[args['id']] = args 

        return {'message':'Added', 'data':args}, 201


class Item(Resource):
    def get(self,identifier):
        shelf = get_db()
        if identifier not in shelf.keys():
            return {'message':'not found'}
        return {"data":shelf[identifier]}

    def delete(self,identifier):
        shelf = get_db()
        if identifier not in shelf.keys():
            return {'message':'not found'}
        del shelf[identifier]
        return 204
api.add_resource(List, '/lists')
api.add_resource(Item, '/list/<string:identifier>')