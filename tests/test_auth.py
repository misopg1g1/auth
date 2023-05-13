from sqlalchemy.orm import declarative_base

import schemas
import api
import models
import helpers

import bcrypt
import json

from config.db_client import db_client
from fastapi.testclient import TestClient


class TestClassLogin:
    def test_success(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()
        user_instance = models.User(user='user1',
                                    password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                    role='ADMIN')
        login_instance_schema = schemas.LoginUserSchema(**user_instance.__dict__)
        models.User.push_object(user_instance)
        dict_login_instance_schema: dict = dict(sorted(login_instance_schema.dict().items(), key=lambda kv: kv[0]))
        dict_login_instance_schema['password'] = 'password1'
        raw_hash = helpers.get_hash(dict_login_instance_schema)
        dict_login_instance_schema['hash'] = helpers.encrypt_hash(raw_hash)

        resp = client.post("/session/login", json=dict_login_instance_schema)
        assert resp.status_code == 200
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()

    def test_unauthorized(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()
        user_instance = models.User(user='user1',
                                    password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                    role='ADMIN')
        login_instance_schema = schemas.LoginUserSchema(**user_instance.__dict__)
        models.User.push_object(user_instance)
        dict_login_instance_schema: dict = dict(sorted(login_instance_schema.dict().items(), key=lambda kv: kv[0]))
        dict_login_instance_schema['password'] = 'password2'
        raw_hash = helpers.get_hash(dict_login_instance_schema)
        dict_login_instance_schema['hash'] = helpers.encrypt_hash(raw_hash)
        resp = client.post("/session/login", json=dict_login_instance_schema)
        assert resp.status_code == 401
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()



    def test_forbidden(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()
        user_instance = models.User(user='user1',
                                    password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                    role='ADMIN')
        login_instance_schema = schemas.LoginUserSchema(**user_instance.__dict__)
        models.User.push_object(user_instance)
        dict_login_instance_schema: dict = dict(sorted(login_instance_schema.dict().items(), key=lambda kv: kv[0]))
        dict_login_instance_schema['password'] = 'password1'
        raw_hash = helpers.get_hash(dict_login_instance_schema)
        dict_login_instance_schema['hash'] = helpers.encrypt_hash(raw_hash)
        dict_login_instance_schema['user'] = 'user2'
        resp = client.post("/session/login", json=dict_login_instance_schema)
        assert resp.status_code == 403
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()



#

class TestClassCreateUser:
    def test_success(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance = models.User(user='user1',
                                             password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                             role='ADMIN')
        models.User.push_object(existing_user_instance)
        existing_user_instance = models.User.query_by_kwargs(True, user="user1")
        token = helpers.generate_token(json.loads(existing_user_instance.json(exclude={'password'})))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        user_to_add = {"user": 'user2', "password": 'password2', "role": 'SELLER', "verify_password": "password2"}
        raw_hash = helpers.get_hash(user_to_add)
        user_to_add['hash'] = helpers.encrypt_hash(raw_hash)
        resp = client.post("/session/create_user", json=user_to_add, headers=headers)
        assert resp.status_code == 200
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()


    def test_conflict(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance1 = models.User(user='user1',
                                              password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                              role='ADMIN')

        models.User.push_object(existing_user_instance1)
        existing_user_instance2 = models.User(user='user2',
                                              password=bcrypt.hashpw('password2'.encode(), bcrypt.gensalt(10)).decode(),
                                              role='SELLER')
        models.User.push_object(existing_user_instance2)
        existing_user_instance = models.User.query_by_kwargs(True, user="user1")
        token = helpers.generate_token(json.loads(existing_user_instance.json(exclude={'password'})))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        user_to_add = {"user": 'user2', "password": 'password2', "role": 'SELLER', "verify_password": "password2"}
        raw_hash = helpers.get_hash(user_to_add)
        user_to_add['hash'] = helpers.encrypt_hash(raw_hash)
        resp = client.post("/session/create_user", json=user_to_add, headers=headers)
        assert resp.status_code == 409
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()


    def test_unauthorized(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance1 = models.User(user='user1',
                                              password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                              role='ADMIN')

        models.User.push_object(existing_user_instance1)
        existing_user_instance2 = models.User(user='user2',
                                              password=bcrypt.hashpw('password2'.encode(), bcrypt.gensalt(10)).decode(),
                                              role='SELLER')
        models.User.push_object(existing_user_instance2)
        existing_user_instance = models.User.query_by_kwargs(True, user="user2")
        token = helpers.generate_token(json.loads(existing_user_instance.json(exclude={'password'})))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        user_to_add = {"user": 'user2', "password": 'password2', "role": 'SELLER', "verify_password": "password2"}
        raw_hash = helpers.get_hash(user_to_add)
        user_to_add['hash'] = helpers.encrypt_hash(raw_hash)
        resp = client.post("/session/create_user", json=user_to_add, headers=headers)
        assert resp.status_code == 401
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()



class TestClassRefreshToken:
    def test_success(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance = models.User(user='user1',
                                             password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                             role='ADMIN')
        models.User.push_object(existing_user_instance)
        existing_user_instance = models.User.query_by_kwargs(True, user="user1")
        token = helpers.generate_token(json.loads(existing_user_instance.json(exclude={'password'})))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        resp = client.get("/session/refresh_token", headers=headers)
        resp_msg = resp.json().get("access_token", None)
        assert resp.status_code == 200
        assert resp_msg == token
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()



class TestClassVerifyRoles:
    def test_success(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance = models.User(user='user1',
                                             password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                             role='ADMIN')
        models.User.push_object(existing_user_instance)
        existing_user_instance = models.User.query_by_kwargs(True, user="user1")
        token = helpers.generate_token(json.loads(existing_user_instance.json(exclude={'password'})))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        payload = {"roles": ["ADMIN"]}
        payload["hash"] = helpers.encrypt_hash(helpers.get_hash(payload))
        resp = client.post("/session/verify_roles", json=payload, headers=headers)
        assert resp.status_code == 204
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()


    def test_forbidden(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance = models.User(user='user1',
                                             password=bcrypt.hashpw('password1'.encode(),
                                                                    bcrypt.gensalt(10)).decode(),
                                             role='ADMIN')
        models.User.push_object(existing_user_instance)
        existing_user_instance = models.User.query_by_kwargs(True, user="user1")
        token = helpers.generate_token(json.loads(existing_user_instance.json(exclude={'password'})))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        payload = {"roles": ["SELLER"]}
        payload["hash"] = helpers.encrypt_hash(helpers.get_hash(payload))
        resp = client.post("/session/verify_roles", json=payload, headers=headers)
        assert resp.status_code == 403
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()



class TestClassVerifyToken:
    def test_success(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance = models.User(user='user1',
                                             password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                             role='ADMIN')
        models.User.push_object(existing_user_instance)
        existing_user_instance = models.User.query_by_kwargs(True, user="user1")
        token = helpers.generate_token(json.loads(existing_user_instance.json(exclude={'password'})))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        resp = client.get("/session/verify_token", headers=headers)
        assert resp.status_code == 200
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()


    def test_unauthorized(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        db_client.session.commit()

        existing_user_instance = models.User(user='user1',
                                             password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                             role='ADMIN')
        models.User.push_object(existing_user_instance)
        existing_user_instance = models.User.query_by_kwargs(True, user="user1")
        dict_existing_user_instance = json.loads(existing_user_instance.json(exclude={'password'}))
        dict_existing_user_instance["role"] = "SELLER"
        token = helpers.generate_token(dict_existing_user_instance)
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        resp = client.get("/session/verify_token", headers=headers)
        assert resp.status_code == 401
        declarative_base().metadata.drop_all(bind=db_client.engine)
        db_client.session.commit()

