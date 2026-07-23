import os
import requests
import psycopg2
from dotenv import load_dotenv
from tqdm import tqdm


load_dotenv()


conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = conn.cursor()



def get_gen(id):

    resposta = requests.get(
        f"https://pokeapi.co/api/v2/pokemon-species/{id}",
        timeout=10
    )

    resposta.raise_for_status()

    especie = resposta.json()

    geracao = especie["generation"]["name"]

    mapa = {
        "generation-i": "I",
        "generation-ii": "II",
        "generation-iii": "III",
        "generation-iv": "IV",
        "generation-v": "V",
        "generation-vi": "VI",
        "generation-vii": "VII",
        "generation-viii": "VIII",
        "generation-ix": "IX"
    }

    return mapa[geracao]



try:

    cursor.execute("""
        SELECT pokeapi_id
        FROM pokemon
        ORDER BY pokeapi_id;
    """)

    pokemons = cursor.fetchall()


    barra = tqdm(
        pokemons,
        desc="Atualizando gerações",
        unit=" pokémon"
    )


    for (poke_id,) in barra:

        try:

            geracao = get_gen(poke_id)


            cursor.execute("""
                UPDATE pokemon
                SET geracao = %s
                WHERE pokeapi_id = %s;
            """,
            (
                geracao,
                poke_id
            ))


            conn.commit()


            barra.set_postfix_str(
                f"#{poke_id} | Geração {geracao}"
            )


        except Exception as erro:

            conn.rollback()

            tqdm.write(
                f"Erro no Pokémon #{poke_id}: {erro}"
            )


finally:

    cursor.close()
    conn.close()


print("\nAtualização concluída!")