import styles from './Login.module.css';

export function Login() {
  return (
    <div className={styles.loginContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Login</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formLogin}>
        <label htmlFor="login-email" className={styles.tituloInputLogin}>Email</label>
        <input id="login-email" type="email" className={styles.inputLogin} />
        <label htmlFor="login-senha" className={styles.tituloInputLogin}>Senha</label>
        <input id="login-senha" type="password" className={styles.inputLogin} /> <br/>
        <a className={styles.textoFormLogin}>Esqueci minha senha</a>
        <a className={styles.botaoLogin}>Entrar</a>
      </div>
      </section>
    </div>

  );
}
