from src.database.connection import get_connection
from src.database.query import (
    SEARCH_POKEMON,
    SEARCH_POKEMON_TYPES,
    SEARCH_ABILITY,
    LIST_POKEMON,
    SEARCH_POKEMON_BY_TYPE,
    SEARCH_POKEMON_NAME
)


def search_pokemon(nome):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            SEARCH_POKEMON,
            (f"%{nome}%",)
        )

        pokemon = cursor.fetchone()

        if pokemon is None:
            return None

        pokemon_id = pokemon[0]

        cursor.execute(
            SEARCH_POKEMON_TYPES,
            (pokemon_id,)
        )

        tipos = [
            tipo[0]
            for tipo in cursor.fetchall()
        ]


        cursor.execute(
            SEARCH_ABILITY,
            (pokemon_id,)
        )

        habilidades = [
            {
                "nome": habilidade[0],
                "is_hidden": habilidade[1]
            }
            for habilidade in cursor.fetchall()
        ]


        return {
            "id": pokemon[0],
            "pokeapi_id": pokemon[1],
            "nome": pokemon[2],
            "altura": pokemon[3],
            "peso": pokemon[4],
            "sprite": pokemon[5],
            "tipos": tipos,
            "habilidades": habilidades
        }


    finally:

        cursor.close()
        conn.close()



def list_pokemon(limit: int, offset: int):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            LIST_POKEMON,
            (limit, offset)
        )

        pokemons = cursor.fetchall()


        return [
            {
                "pokeapi_id": pokemon[0],
                "nome": pokemon[1],
                "altura": pokemon[2],
                "peso": pokemon[3],
                "sprite": pokemon[4]
            }
            for pokemon in pokemons
        ]


    finally:

        cursor.close()
        conn.close()



def search_type(nome):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            SEARCH_POKEMON_BY_TYPE,
            (nome,)
        )

        pokemons = cursor.fetchall()


        return [
            {
                "pokeapi_id": pokemon[0],
                "nome": pokemon[1],
                "sprite": pokemon[2]
            }
            for pokemon in pokemons
        ]


    finally:

        cursor.close()
        conn.close()



def search_pokemons(nome):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            SEARCH_POKEMON_NAME,
            (f"%{nome}%",)
        )

        pokemons = cursor.fetchall()


        return [
            {
                "pokeapi_id": pokemon[0],
                "nome": pokemon[1],
                "sprite": pokemon[2]
            }
            for pokemon in pokemons
        ]


    finally:

        cursor.close()
        conn.close()