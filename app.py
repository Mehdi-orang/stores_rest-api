from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import Store, StoreList
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'  # configure Authentication URL (must be before init jwt)
app.secret_key = 'Mohammad'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'  # configure Authentication Key Name
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)  # configure Token Expiration Time

# customize JWT auth response, include user_id in response body
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#     return jsonify({
#                         'access_token': access_token.decode('utf-8'),
#                         'user_id': identity.id
#                    })


# customize JWT auth response, include user_id in response body
# @jwt.jwt_error_handler
# def customized_error_handler(error):
#     return jsonify({
#                        'message': error.description,
#                        'code': error.status_code
#                    }), error.status_code

# more for flask-jwt at https://pythonhosted.org/Flask-JWT/

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__:
    db.init_app(app )
    app.run(port=5000, debug=True)
