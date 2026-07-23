SEARCH_POKEMON = """
SELECT
    id,
    pokeapi_id,
    nome,
    altura,
    peso,
    sprite
FROM pokemon
WHERE nome ILIKE %s;
"""

SEARCH_POKEMON_TYPES = """
SELECT
    t.nome
FROM pokemon_tipo pt
JOIN tipo t
ON pt.tipo_id = t.id
WHERE pt.pokemon_id = %s;
"""

SEARCH_ABILITY = """
SELECT
    h.nome,
    ph.is_hidden
FROM pokemon_habilidade ph
JOIN habilidade h
ON ph.habilidade_id = h.id
WHERE ph.pokemon_id = %s;
"""

LIST_POKEMON = """
SELECT
    pokeapi_id,
    nome,
    altura,
    peso,
    sprite
FROM pokemon
ORDER BY pokeapi_id
LIMIT %s OFFSET %s;
"""

SEARCH_POKEMON_BY_TYPE = """
SELECT
    p.pokeapi_id,
    p.nome,
    p.sprite
FROM pokemon p
JOIN pokemon_tipo pt
ON p.id = pt.pokemon_id
JOIN tipo t
ON pt.tipo_id = t.id
WHERE t.nome ILIKE %s
ORDER BY p.pokeapi_id;
"""
SEARCH_POKEMON_NAME = """
SELECT
    pokeapi_id,
    nome,
    sprite
FROM pokemon
WHERE nome ILIKE %s
ORDER BY pokeapi_id;
"""

SEARCH_POKEMON_BY_GEN = """
SELECT
    pokeapi_id,
    nome,
    sprite
FROM pokemon
WHERE geracao = %s
ORDER BY pokeapi_id;
"""