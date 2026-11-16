import styles from './NovaSenha.module.css';

export function NovaSenha() {
  return (
    <div className={styles.novaSenhaContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Nova senha</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formNovaSenha}>
        <p role="status" className={styles.textoFormNovaSenha}>A redefinição de senha ainda não está disponível.</p>
        <label htmlFor="nova-senha" className={styles.tituloInputNovaSenha}>Digite sua nova senha:</label>
        <input id="nova-senha" type="password" disabled className={styles.inputNovaSenha} />
        <label htmlFor="confirmacao-senha" className={styles.tituloInputNovaSenha}>Confirme sua nova senha:</label>
        <input id="confirmacao-senha" type="password" disabled className={styles.inputNovaSenha} /> <br/>
        <button type="button" disabled className={styles.botaoNovaSenha}>Confirmar</button>
        <Link to="/login" className={styles.textoFormNovaSenha}>Voltar ao login</Link>
      </div>
      </section>
    </div>

  );
}
import { Link } from 'react-router-dom';
