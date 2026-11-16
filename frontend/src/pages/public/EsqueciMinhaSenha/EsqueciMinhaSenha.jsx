import styles from './EsqueciMinhaSenha.module.css';

export function EsqueciMinhaSenha() {
  return (
    <div className={styles.esqueciMinhaSenhaContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Esqueci minha senha</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formEsqueciMinhaSenha}>
        <label htmlFor="recuperacao-email" className={styles.tituloInputEsqueciMinhaSenha}>Email</label>
        <input id="recuperacao-email" type="email" className={styles.inputEsqueciMinhaSenha} />
        <a className={styles.botaoEsqueciMinhaSenha}>Confirmar</a>
      </div>
      </section>
    </div>

  );
}
