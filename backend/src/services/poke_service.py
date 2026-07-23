from src.database.connection import get_connection
from src.database.query import (
    SEARCH_POKEMON,
    SEARCH_POKEMON_TYPES,
    SEARCH_ABILITY,
    LIST_POKEMON
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

        # total de pokemons
        cursor.execute(
            "SELECT COUNT(*) FROM pokemon"
        )

        total = cursor.fetchone()[0]


        # pokemons da página
        cursor.execute(
            LIST_POKEMON,
            (limit, offset)
        )

        pokemons = cursor.fetchall()


        return {

            "pokemons": [
                {
                    "pokeapi_id": pokemon[0],
                    "nome": pokemon[1],
                    "altura": pokemon[2],
                    "peso": pokemon[3],
                    "sprite": pokemon[4]
                }
                for pokemon in pokemons
            ],

            "total": total
        }


    finally:

        cursor.close()
        conn.close()

def filter_pokemon(nome, tipo, geracao, page, limit):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        base_query = """
        FROM pokemon p
        """

        parametros = []
        where = []


        if tipo:

            base_query += """
            JOIN pokemon_tipo pt
                ON p.id = pt.pokemon_id
            JOIN tipo t
                ON pt.tipo_id = t.id
            """

            where.append("t.nome = %s")
            parametros.append(tipo.capitalize())


        if nome:

            where.append("p.nome ILIKE %s")
            parametros.append(f"%{nome}%")


        if geracao:

            where.append("p.geracao = %s")
            parametros.append(geracao)

        # Conta total de resultados

        count_query = """
        SELECT COUNT(DISTINCT p.id)
        """ + base_query


        if where:

            count_query += " WHERE " + " AND ".join(where)


        cursor.execute(
            count_query,
            parametros
        )

        total = cursor.fetchone()[0]

        # Busca os pokemons da página

        query = """
        SELECT DISTINCT
            p.pokeapi_id,
            p.nome,
            p.sprite
        """ + base_query


        if where:

            query += " WHERE " + " AND ".join(where)

        offset = (page - 1) * limit

        query += """
        ORDER BY p.pokeapi_id
        LIMIT %s OFFSET %s
        """

        parametros.extend([
            limit,
            offset
        ])


        cursor.execute(
            query,
            parametros
        )

        pokemons = cursor.fetchall()

        return {

            "pokemons": [
                {
                    "pokeapi_id": pokemon[0],
                    "nome": pokemon[1],
                    "sprite": pokemon[2]
                }
                for pokemon in pokemons
            ],

            "total": total
        }

    finally:

        cursor.close()
        conn.close()