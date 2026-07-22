from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.poke_routes import router


app = FastAPI(
    title="Pokédex API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pokedex-cfpnhd4zl-dcaldas-afk1.vercel.app/",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)