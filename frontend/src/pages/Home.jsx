import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services/api";
import PokemonCard from "../components/PokemonCard";
import "../App.css";

function Home() {

    const [pokemons, setPokemons] = useState([]);
    const [busca, setBusca] = useState("");
    const [pagina, setPagina] = useState(1);
    const [loading, setLoading] = useState(false);
    const [buscaAberta, setBuscaAberta] = useState(false);
    const [tipo, setTipo] = useState("");
    const [geracao, setGeracao] = useState("");
    const [totalPaginas, setTotalPaginas] = useState(1);

    const limite = 50;

    useEffect(() => {

        if (busca || tipo || geracao) {
            pesquisar();
        } else {
            carregarPokemons();
        }

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }, [pagina]);

    async function carregarPokemons() {

        setLoading(true);

        const offset = (pagina - 1) * limite;

        try {

            const resposta = await api.get(
                `/pokemon?limit=${limite}&offset=${offset}`
            );


            setPokemons(resposta.data.pokemons);


            setTotalPaginas(
                Math.ceil(resposta.data.total / limite)
            );


        } catch (erro) {

            console.error(erro);

        } finally {

            setLoading(false);

        }

    }
    
    async function pesquisar() {

        setLoading(true);

        try {

            const params = new URLSearchParams();


            if (busca)
                params.append("nome", busca);


            if (tipo)
                params.append("tipo", tipo);


            if (geracao)
                params.append("geracao", geracao);


            params.append("page", pagina);
            params.append("limit", limite);



            const resposta = await api.get(
                `/pokemon/filter?${params.toString()}`
            );


            setPokemons(resposta.data.pokemons);

            setTotalPaginas(
                Math.ceil(resposta.data.total / limite)
            );


        } catch (erro) {

            console.error(erro);

            setPokemons([]);

        } finally {

            setLoading(false);

        }

    }

    function resetPage() {

        setBusca("");
        setTipo("");
        setGeracao("");
        setPagina(1);

        setTimeout(() => {
            carregarPokemons();
        }, 0);

    }

    function renderPagination() {

        let paginas = [];


        function adicionarPagina(numero) {

            paginas.push(

                <span
                    key={numero}
                    className={
                        `page-number ${
                            numero === pagina
                            ? "active"
                            : ""
                        }`
                    }
                    onClick={() => setPagina(numero)}
                >
                    {numero}
                </span>

            );

        }


        function adicionarReticencias(key) {

            paginas.push(

                <span
                    key={key}
                    className="page-number"
                >
                    ...
                </span>

            );

        }


        // primeira página
        if (pagina > 3) {

            adicionarPagina(1);

            adicionarReticencias("inicio");

        }


        let inicio = Math.max(1, pagina - 2);
        let fim = Math.min(totalPaginas, pagina + 2);


        for(let i = inicio; i <= fim; i++) {

            adicionarPagina(i);

        }


        // última página
        if (pagina < totalPaginas - 2) {

            adicionarReticencias("fim");

            adicionarPagina(totalPaginas);

        }


        return (

            <div className="pagination">

                <span
                    className="page-arrow"
                    onClick={() =>
                        pagina > 1 && setPagina(pagina - 1)
                    }
                >
                    ‹ Anterior
                </span>


                {paginas}


                <span
                    className="page-arrow"
                    onClick={() =>
                        pagina < totalPaginas &&
                        setPagina(pagina + 1)
                    }
                >
                    Próxima ›
                </span>

            </div>

        );

    }

    return (

        <div className="container">

            <Link
                to="/"
                className="logo"
                onClick={resetPage}
            >
                <h1>Pokédex</h1>
            </Link>

            <div className="search-container">

                <button
                    className="search-toggle"
                    type="button"
                    onClick={() =>
                        setBuscaAberta(!buscaAberta)
                    }
                >

                    <img
                        src="/search.svg"
                        alt="SearchIcon"
                        className="search-icon"
                    />

                    <span>
                        Pesquisar
                    </span>

                </button>

                {buscaAberta && (

                    <form
                        className="search-menu"
                        onSubmit={(e) => {

                            e.preventDefault();

                            setPagina(1);

                            pesquisar();

                        }}
                    >
                        <input
                            type="text"
                            placeholder="Buscar Pokémon..."
                            value={busca}
                            onChange={(e) =>
                                setBusca(e.target.value)
                            }
                        />

                        <select
                            value={tipo}
                            onChange={(e) =>
                                setTipo(e.target.value)
                            }
                        >
                            <option value="">Todos os tipos</option>
                            <option value="Normal">Normal</option>
                            <option value="Fire">Fogo</option>
                            <option value="Water">Água</option>
                            <option value="Grass">Planta</option>
                            <option value="Electric">Elétrico</option>
                            <option value="Ice">Gelo</option>
                            <option value="Fighting">Lutador</option>
                            <option value="Poison">Veneno</option>
                            <option value="Ground">Terra</option>
                            <option value="Flying">Voador</option>
                            <option value="Psychic">Psíquico</option>
                            <option value="Bug">Inseto</option>
                            <option value="Rock">Pedra</option>
                            <option value="Ghost">Fantasma</option>
                            <option value="Dragon">Dragão</option>
                            <option value="Dark">Sombrio</option>
                            <option value="Steel">Aço</option>
                            <option value="Fairy">Fada</option>
                        </select>

                        <select
                            value={geracao}
                            onChange={(e) =>
                                setGeracao(e.target.value)
                            }
                        >
                            <option value="">Todas as gerações</option>
                            <option value="I">I</option>
                            <option value="II">II</option>
                            <option value="III">III</option>
                            <option value="IV">IV</option>
                            <option value="V">V</option>
                            <option value="VI">VI</option>
                            <option value="VII">VII</option>
                            <option value="VIII">VIII</option>
                            <option value="IX">IX</option>
                        </select>



                        <button type="submit">
                            Confirmar
                        </button>


                    </form>

                )}


            </div>

            {renderPagination()}
            
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
            {renderPagination()}
        </div>

    );

}

export default Home;