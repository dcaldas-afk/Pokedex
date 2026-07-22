import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import "./PokemonDetails.css";

function PokemonDetails() {

    const { nome } = useParams();

    const [pokemon, setPokemon] = useState(null);


    useEffect(() => {

        api.get(`/pokemon/${nome}`)
            .then(resposta => {
                setPokemon(resposta.data);
            });

    }, [nome]);


    if (!pokemon) {
        return <h1>Carregando...</h1>;
    }

    function tipoClasse(tipo) {

    return tipo.toLowerCase();

    }

    return (

        <div className="pokemon-details">

            <h1>
                #{pokemon.pokeapi_id} {pokemon.nome}
            </h1>


            <img
                src={pokemon.sprite}
                alt={pokemon.nome}
            />


            <div className="info">

                <span className="tag">
                    Altura: {pokemon.altura} m
                </span>


                <span className="tag">
                    Peso: {pokemon.peso} kg
                </span>

            </div>



            <h2>Tipo</h2>
            <h3></h3>

            <div>

                {
                    pokemon.tipos.map(tipo => (

                        <span 
                            className={`tag ${tipoClasse(tipo)}`}
                            key={tipo}
                        >
                            {tipo}
                        </span>

                    ))
                }

            </div>


            <h3></h3>
            <h2>Habilidades</h2>

            <ul className="lista">

                {
                    pokemon.habilidades.map(habilidade => (

                        <li key={habilidade.nome}>

                            {habilidade.nome}

                            {
                                habilidade.is_hidden &&
                                " (Oculta)"
                            }

                        </li>

                    ))
                }

            </ul>


        </div>

    );

}


export default PokemonDetails;