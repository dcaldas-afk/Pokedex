from fastapi import APIRouter, HTTPException
from src.services.poke_service import (
    search_pokemon,
    list_pokemon,
    search_type,
    search_pokemons
)


router = APIRouter()


@router.get("/pokemon/{nome}")
def pokemon(nome: str):

    resultado = search_pokemon(nome)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Pokémon não encontrado"
        )

    return resultado

@router.get("/pokemon")
def list(
    limit: int = 50,
    offset: int = 0
):
    return list_pokemon(limit, offset)

@router.get("/tipo/{nome}")
def tipo(nome: str):

    return search_type(nome)

@router.get("/pokemon/search/{nome}")
def search(nome: str):

    return search_pokemons(nome)