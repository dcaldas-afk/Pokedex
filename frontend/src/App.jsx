import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PokemonDetails from "./pages/PokemonDetails";


function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Home />}
                />

                <Route
                    path="/pokemon/:nome"
                    element={<PokemonDetails />}
                />

            </Routes>

        </BrowserRouter>

    );
}


export default App;