import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './assets/global.css';

// Importando o Cabeçalho e o Rodapé
import { HeaderPublico } from './components/HeaderPublico/HeaderPublico';
import { Footer } from './components/Footer/Footer';

// Importando as páginas
import { Home } from './pages/public/Home/Home';
import { Catalogo } from './pages/public/Catalogo/Catalogo';
import { Faq } from './pages/public/Faq/Faq';
import { Login } from './pages/public/Login/Login';

function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        
        {/* O Header fica fora das rotas para aparecer fixo em todas as telas */}
        <HeaderPublico />
        
        {/* Aqui é o "miolo" do site, onde o conteúdo vai mudar dependendo da URL */}
        <main style={{ flex: 1, padding: '20px 5%' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/catalogo" element={<Catalogo />} />
            <Route path="/faq" element={<Faq />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>

        {/* O Footer também fica fora das rotas para aparecer fixo no final */}
        <Footer />
        
      </div>
    </BrowserRouter>
  );
}

export default App;