from dotenv import load_dotenv

load_dotenv(verbose=True)


from fastapi import FastAPI
from app import routes
from app.db import db as database


def init_application() -> FastAPI:
    application = FastAPI(debug=True)
    application.include_router(routes.router, prefix="")

    return application


app = init_application()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Gracefully disconnecting database")
    await database.disconnect()
