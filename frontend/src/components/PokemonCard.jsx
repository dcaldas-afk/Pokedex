import "./PokemonCard.css";
import { Link } from "react-router-dom";


function PokemonCard({ pokemon }) {

    return (

        <Link to={`/pokemon/${pokemon.nome.toLowerCase()}`}>

            <div className="card">

                <img
                    src={pokemon.sprite}
                    alt={pokemon.nome}
                />

                <h2>
                    #{pokemon.pokeapi_id}
                </h2>

                <h3>
                    {pokemon.nome}
                </h3>

            </div>

        </Link>

    );
}


export default PokemonCard;