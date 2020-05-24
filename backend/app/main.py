from fastapi import FastAPI
from app import routes


def init_application() -> FastAPI:
    application = FastAPI(debug=True)
    application.include_router(routes.router, prefix="")

    return application


app = init_application()
