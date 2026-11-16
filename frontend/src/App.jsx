import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './auth/AuthProvider';
import { RequireAdmin } from './auth/RequireAdmin';
import { MinhaConta } from './pages/admin/MinhaConta/MinhaConta';
import './assets/global.css';

// Importando o Cabeçalho e o Rodapé
import { HeaderPublico } from './components/HeaderPublico/HeaderPublico';
import { Footer } from './components/Footer/Footer';

// Importando as páginas
import { Home } from './pages/public/Home/Home';
import { Catalogo } from './pages/public/Catalogo/Catalogo';
import { Faq } from './pages/public/Faq/Faq';
import { Login } from './pages/public/Login/Login';
import { EsqueciMinhaSenha } from './pages/public/EsqueciMinhaSenha/EsqueciMinhaSenha';
import { NovaSenha } from './pages/public/NovaSenha/NovaSenha';
import { LivroDetalhes } from './pages/public/LivroDetalhes/LivroDetalhes'; // <-- Novo import aqui

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
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
            <Route path="/esqueci-minha-senha" element={<EsqueciMinhaSenha />} />
            <Route path="/nova-senha" element={<NovaSenha />} />
            <Route path="/livro/:id" element={<LivroDetalhes />} /> {/* <-- Nova rota aqui */}
            <Route path="/admin" element={<RequireAdmin />}>
              <Route index element={<MinhaConta />} />
            </Route>
            <Route path="*" element={<section><h2>Página não encontrada</h2><Link to="/">Voltar ao início</Link></section>} />
          </Routes>
        </main>

        {/* O Footer também fica fora das rotas para aparecer fixo no final */}
        <Footer />
        
      </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
