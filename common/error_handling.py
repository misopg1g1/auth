from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppErrorBaseClass(Exception):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass


class Conflict(AppErrorBaseClass):
    pass


class NotAllowed(AppErrorBaseClass):
    pass


class Forbidden(AppErrorBaseClass):
    pass


class BadRequest(AppErrorBaseClass):
    pass


class NotReady(AppErrorBaseClass):
    pass


def add_custom_errors(app: FastAPI):
    @app.exception_handler(AppErrorBaseClass)
    async def handle_exception_error(request: Request, exc: AppErrorBaseClass):
        return JSONResponse(status_code=500, content={"error": exc.args[0]})

    @app.exception_handler(ObjectNotFound)
    async def handle_404_error(request: Request, exc: ObjectNotFound):
        return JSONResponse(status_code=404, content={"error": exc.args[0]})

    @app.exception_handler(BadRequest)
    async def handle_400_error(request: Request, exc: BadRequest):
        return JSONResponse(status_code=400, content={"error": exc.args[0]})

    @app.exception_handler(NotAllowed)
    async def handle_401_error(request: Request, exc: NotAllowed):
        return JSONResponse(status_code=401, content={"error": exc.args[0]})

    @app.exception_handler(Forbidden)
    async def handle_403_error(request: Request, exc: Forbidden):
        return JSONResponse(status_code=403, content={"error": exc.args[0]})

    @app.exception_handler(Conflict)
    async def handle_409_error(request: Request, exc: Conflict):
        return JSONResponse(status_code=409, content={"error": exc.args[0]})
