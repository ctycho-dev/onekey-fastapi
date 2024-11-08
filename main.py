""" FastAPI """

import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app import models
from app.database import engine
from app.routes import cdek, email

# creates database by pydantic, but we use alembic instead now
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://leeblock.ru",
    "https://wwww.leeblock.ru",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root"""
    return {"message": "Hello World"}


app.include_router(cdek.router)
app.include_router(email.router)


def main():
    """Main function."""
    rc = 0

    try:
        uvicorn.run(app, port=5000)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f'Error: {exc}')
        rc = -1

    return rc


if __name__ == '__main__':
    sys.exit(main())
