import { useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../auth/context';
import styles from './Login.module.css';

export function Login() {
  const { admin, login, expired } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');
  const [enviando, setEnviando] = useState(false);
  const from = location.state?.from;
  const destination = typeof from === 'string' && (from === '/admin' || from.startsWith('/admin/')) ? from : '/admin';

  async function entrar(event) {
    event.preventDefault();
    if (enviando) return;
    if (!usuario.trim() || !senha) {
      setErro('Informe seu usuário e sua senha.');
      return;
    }
    setErro('');
    setEnviando(true);
    try {
      await login(usuario.trim(), senha);
      navigate(destination, { replace: true });
    } catch (error) {
      setErro(error.status === 401 ? 'Usuário ou senha inválidos.' : error.message);
    } finally {
      setSenha('');
      setEnviando(false);
    }
  }

  if (admin) return <Navigate to={destination} replace />;
  return (
    <div className={styles.loginContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Login</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <form className={styles.formLogin} onSubmit={entrar} aria-busy={enviando}>
        {expired && <p role="status" className={styles.mensagem}>Sua sessão expirou ou foi invalidada. Entre novamente.</p>}
        {erro && <p role="alert" className={styles.mensagem}>{erro}</p>}
        <label htmlFor="login-usuario" className={styles.tituloInputLogin}>Usuário</label>
        <input id="login-usuario" name="usuario" type="text" autoComplete="username" maxLength={100} required value={usuario} onChange={(event) => setUsuario(event.target.value)} disabled={enviando} className={styles.inputLogin} />
        <label htmlFor="login-senha" className={styles.tituloInputLogin}>Senha</label>
        <input id="login-senha" name="senha" type="password" autoComplete="current-password" maxLength={128} required value={senha} onChange={(event) => setSenha(event.target.value)} disabled={enviando} className={styles.inputLogin} /> <br/>
        <Link to="/esqueci-minha-senha" className={styles.textoFormLogin}>Esqueci minha senha</Link>
        <button type="submit" disabled={enviando} className={styles.botaoLogin}>{enviando ? 'Entrando...' : 'Entrar'}</button>
      </form>
      </section>
    </div>

  );
}
