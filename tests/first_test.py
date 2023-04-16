import schemas
import api
import config
import models

from config.db_client import db_client

import hashlib
import bcrypt
import json

from fastapi.testclient import TestClient
from cryptography.fernet import Fernet

path_login = "/session/login"

class TestClassFirstTest:
    def test_succes(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        user_instance = models.User(user='user1',
                                    password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                    role='ADMIN')
        login_instance_schema = schemas.LoginUserSchema(**user_instance.__dict__)
        models.User.push_object(user_instance)
        dict_login_instance_schema: dict = dict(sorted(login_instance_schema.dict().items(), key=lambda kv: kv[0]))
        dict_login_instance_schema['password'] = 'password1'
        raw_hash = hashlib.md5(json.dumps(dict_login_instance_schema).encode()).hexdigest()
        dict_login_instance_schema['hash'] = Fernet(config.AppConfigValues.ENCRYPTION_KEY_SECRET).encrypt(
            raw_hash.encode()).decode()

        resp = client.post(path_login, json=dict_login_instance_schema)
        assert resp.status_code == 200

    def test_unauthorized(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        user_instance = models.User(user='user1',
                                    password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                    role='ADMIN')
        login_instance_schema = schemas.LoginUserSchema(**user_instance.__dict__)
        models.User.push_object(user_instance)
        dict_login_instance_schema: dict = dict(sorted(login_instance_schema.dict().items(), key=lambda kv: kv[0]))
        dict_login_instance_schema['password'] = 'password2'
        raw_hash = hashlib.md5(json.dumps(dict_login_instance_schema).encode()).hexdigest()
        dict_login_instance_schema['hash'] = Fernet(config.AppConfigValues.ENCRYPTION_KEY_SECRET).encrypt(
            raw_hash.encode()).decode()

        resp = client.post(path_login, json=dict_login_instance_schema)
        assert resp.status_code == 401

    def test_forbidden(self):
        client = TestClient(api.create_app())
        db_client.session.query(models.User).delete()
        user_instance = models.User(user='user2',
                                    password=bcrypt.hashpw('password1'.encode(), bcrypt.gensalt(10)).decode(),
                                    role='ADMIN')
        login_instance_schema = schemas.LoginUserSchema(**user_instance.__dict__)
        models.User.push_object(user_instance)
        dict_login_instance_schema: dict = dict(sorted(login_instance_schema.dict().items(), key=lambda kv: kv[0]))
        dict_login_instance_schema['password'] = 'password2'
        raw_hash = hashlib.md5(json.dumps(dict_login_instance_schema).encode()).hexdigest()
        dict_login_instance_schema['hash'] = Fernet(config.AppConfigValues.ENCRYPTION_KEY_SECRET).encrypt(
            raw_hash.encode()).decode()
        
        dict_login_instance_schema['user'] = 'user1'
        resp = client.post(path_login, json=dict_login_instance_schema)
        assert resp.status_code == 403      