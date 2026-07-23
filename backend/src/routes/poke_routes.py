from fastapi import APIRouter, HTTPException

from src.services.poke_service import (
    search_pokemon,
    list_pokemon,
    filter_pokemon as filter_pokemon_service
)


router = APIRouter()


@router.get("/pokemon")
def list(
    limit: int = 50,
    offset: int = 0
):
    return list_pokemon(limit, offset)


@router.get("/pokemon/filter")
def filter_pokemon(
    nome: str | None = None,
    tipo: str | None = None,
    geracao: str | None = None,
    page: int = 1,
    limit: int = 50
):

    return filter_pokemon_service(
        nome,
        tipo,
        geracao,
        page,
        limit
    )


@router.get("/pokemon/{nome}")
def pokemon(nome: str):

    resultado = search_pokemon(nome)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Pokémon não encontrado"
        )

    return resultado