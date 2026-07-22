import os
import requests
import psycopg2
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# Conexão com o Supabase (usando o PostgreSQL)
# ==========================

conn = psycopg2.connect(os.getenv("DATABASE_URL"))

cursor = conn.cursor()


def get_id(cursor, tabela, nome):

    tabelas_permitidas = {
        "tipo",
        "habilidade"
    }

    if tabela not in tabelas_permitidas:
        raise ValueError("Tabela inválida")

    cursor.execute(
        f"""
        SELECT id
        FROM {tabela}
        WHERE nome = %s
        """,
        (nome,)
    )

    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        f"""
        INSERT INTO {tabela} (nome)

        VALUES (%s)

        RETURNING id
        """,
        (nome,)
    )

    return cursor.fetchone()[0]


# Função pra importar coisas da PokéAPI + validações
# ==========================
def poke_import(n):

    resp = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{n}",
        timeout=10
    )

    # Gera erro caso a API retorne 404, 500, etc.
    resp.raise_for_status()

    pokemon = resp.json()

    cursor.execute(
        "SELECT id FROM pokemon WHERE pokeapi_id = %s",
        (pokemon["id"],)
    )

    resultado = cursor.fetchone()

    if resultado is not None:

        #print(f"Pokémon #{n} já existe no banco.")
        pokemon_id = resultado[0]

    else:

        cursor.execute("""
            INSERT INTO pokemon
            (
                pokeapi_id,
                nome,
                altura,
                peso,
                sprite
            )

            VALUES (%s,%s,%s,%s,%s)

            RETURNING id
        """,
        (
            pokemon["id"],
            pokemon["name"].capitalize(),
            pokemon["height"] / 10,
            pokemon["weight"] / 10,
            pokemon["sprites"].get("front_default")
        ))

        pokemon_id = cursor.fetchone()[0]

        #print(f"Pokémon #{n} inserido com sucesso.")

    # Inserindo os tipos
    # ==========================

    for tipo in pokemon.get("types", []):

        nome_tipo = tipo["type"]["name"].capitalize()

        tipo_id = get_id(
            cursor,
            "tipo",
            nome_tipo
        )

        cursor.execute("""
            INSERT INTO pokemon_tipo
            (
                pokemon_id,
                tipo_id
            )

            VALUES (%s,%s)

            ON CONFLICT DO NOTHING
        """,
        (
            pokemon_id,
            tipo_id
        ))

    #print(f"Tipos do Pokémon #{n} cadastrados com sucesso.")


    # Inserindo as habilidades
    # ==========================

    for habilidade in pokemon.get("abilities", []):

        nome_habilidade = habilidade["ability"]["name"].capitalize()

        habilidade_id = get_id(
            cursor,
            "habilidade",
            nome_habilidade
        )

        cursor.execute("""
            INSERT INTO pokemon_habilidade
            (
                pokemon_id,
                habilidade_id,
                is_hidden
            )

            VALUES (%s,%s,%s)

            ON CONFLICT DO NOTHING
        """,
        (
            pokemon_id,
            habilidade_id,
            habilidade["is_hidden"]
        ))

    #print(f"Habilidades do Pokémon #{n} cadastradas com sucesso.")
    return pokemon["name"].capitalize()



# Importando tudo e sabendo se deu certo
# ==========================

poke_total = 1025

bar = tqdm(
    range(1, poke_total + 1),
    desc="Importando",
    unit=" pokémon"
)

try:

    for n in bar:

        try:
            poke_name = poke_import(n)
            conn.commit()

            bar.set_description(f"Importando")
            bar.set_postfix_str(f"{poke_name} | Tipos: OK | Habilidades: OK")

        except Exception as erro:
            conn.rollback()

            bar.set_description(f"#{n}")
            bar.set_postfix_str("status: Erro")

            tqdm.write(f"Erro no Pokémon #{n}: {erro}")

finally:
    cursor.close()
    conn.close()


print("\nImportação concluída!")