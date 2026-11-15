import styles from './NovaSenha.module.css';

export function NovaSenha() {
  return (
    <div className={styles.novaSenhaContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Nova senha</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formNovaSenha}>
        <label htmlFor="nova-senha" className={styles.tituloInputNovaSenha}>Digite sua nova senha:</label>
        <input id="nova-senha" type="password" className={styles.inputNovaSenha} />
        <label htmlFor="confirmacao-senha" className={styles.tituloInputNovaSenha}>Confirme sua nova senha:</label>
        <input id="confirmacao-senha" type="password" className={styles.inputNovaSenha} /> <br/>
        <a className={styles.botaoNovaSenha}>Confirmar</a>
      </div>
      </section>
    </div>

  );
}
