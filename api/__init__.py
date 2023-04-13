import api.routers as api_routers
from common import add_custom_errors, handle_cors, decryptor_middleware
from config.db_client import db_client
from models import SQLBaseModel

from fastapi import FastAPI


def create_app():
    SQLBaseModel.metadata.create_all(db_client.engine)
    app = FastAPI()
    add_custom_errors(app)
    app.include_router(api_routers.health_router)
    app.include_router(api_routers.session_router)
    handle_cors(app)
    decryptor_middleware(app)
    return app
