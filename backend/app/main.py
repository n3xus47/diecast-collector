"""Aplikacja API dla Diecast Collector."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import create_db_and_tables
from app.routers import cars, collection

create_db_and_tables()

app = FastAPI(title="Diecast Collector API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cars.router)
app.include_router(collection.router)


@app.get("/")
async def root():
    return {"message": "Diecast Collector API"}
