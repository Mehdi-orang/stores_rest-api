from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('username', type=str, required=True, help="This field cannot be empty!")
    request_parser.add_argument('password', type=str, required=True, help="This field cannot be empty!")

    def post(self):
        data = self.request_parser.parse_args()

        if UserModel.find_user_by_username(data['username']):
            return {'error': 'A user with that username is already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"success": "user created successfully!"}, 201
