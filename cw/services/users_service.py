from flask import current_app

from cw.dao import UserDAO, user
from cw.exceptions import ItemNotFound
from cw.schemas.user import UserSchema
from cw.services.base import BaseService
from cw.tools.security import generate_password_digest, compare_passwords


class UsersService(BaseService):
    def get_one_by_id(self, pk):
        movie = UserDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return UserSchema().dump(movie)

    def get_one_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_limit_users(self, page):
        limit = current_app.config["ITEMS_PER_PAGE"]
        offset = (page - 1) * limit
        users = UserDAO(self._db_session).get_limit(limit=limit, offset=offset)
        return UserSchema(many=True).dump(users)

    def create(self, data_in):
        user_pass = data_in.get("password")
        if user_pass:
            data_in["password"] = generate_password_digest(user_pass)
        user = UserDAO(self._db_session).create(data_in)
        return UserSchema().dump(user)

    def update(self, data_in):
        user = UserDAO(self._db_session).update(data_in)
        return UserSchema().dump(user)

    def update_pass(self, data_in):
        user_pass_1 = data_in.get("password_1")
        user_pass_2 = data_in.get("password_2")
        if not compare_passwords(password_hash=user_pass_1, other_password=user_pass_2):
            raise ItemNotFound
        user.password = generate_password_digest(user_pass_2)

