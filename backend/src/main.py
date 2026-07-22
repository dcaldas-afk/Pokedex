from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.poke_routes import router


app = FastAPI(
    title="Pokédex API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pokedex-5oph.onrender.com/pokemon"
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)