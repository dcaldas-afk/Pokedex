import { useEffect, useState } from "react";
import api from "../services/api";
import PokemonCard from "../components/PokemonCard";
import "../App.css";

function Home() {

    const [pokemons, setPokemons] = useState([]);
    const [busca, setBusca] = useState("");


    useEffect(() => {

        carregarPokemons();

    }, []);


    function carregarPokemons() {

        api.get("/pokemon")
            .then(resposta => {

                console.log(resposta.data);

                setPokemons(resposta.data);

            });

    }


    async function pesquisar() {

        if (busca === "") {
            carregarPokemons();
            return;
        }


        try {

            const resposta = await api.get(
                `/pokemon/search/${busca.toLowerCase()}`
            );

            setPokemons(resposta.data);

        } catch (erro){

            console.error(erro);
            setPokemons([]);

        }

    }

    return (

        <div className="container">


            <h1>Pokédex</h1>


            <form onSubmit={(e) => {
                e.preventDefault();
                pesquisar();
            }}>

                <input
                    type="text"
                    placeholder="Buscar Pokémon..."
                    value={busca}
                    onChange={(e) => setBusca(e.target.value)}
                />
                


                <button type="submit">
                    Buscar
                </button>
                <h3></h3>
            </form>



            <div className="lista-pokemon">

                {
                    pokemons.map(pokemon => (

                        <PokemonCard
                            key={pokemon.pokeapi_id}
                            pokemon={pokemon}
                        />

                    ))
                }

            </div>


        </div>

    );

}


export default Home;