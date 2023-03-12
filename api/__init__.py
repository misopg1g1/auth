import api.routers as api_routers
from fastapi import FastAPI
from common import add_custom_errors, handle_cors, decryptor_middleware


def create_app():
    app = FastAPI()
    add_custom_errors(app)
    app.include_router(api_routers.health_router)
    handle_cors(app)
    decryptor_middleware(app)
    return app
