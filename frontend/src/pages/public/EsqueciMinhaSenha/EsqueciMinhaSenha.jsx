import styles from './EsqueciMinhaSenha.module.css';

export function EsqueciMinhaSenha() {
  return (
    <div className={styles.esqueciMinhaSenhaContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Esqueci minha senha</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formEsqueciMinhaSenha}>
        <p role="status" className={styles.textoFormEsqueciMinhaSenha}>A recuperação de senha por email ainda não está disponível.</p>
        <label htmlFor="recuperacao-email" className={styles.tituloInputEsqueciMinhaSenha}>Email</label>
        <input id="recuperacao-email" type="email" disabled className={styles.inputEsqueciMinhaSenha} />
        <button type="button" disabled className={styles.botaoEsqueciMinhaSenha}>Confirmar</button>
        <Link to="/login" className={styles.textoFormEsqueciMinhaSenha}>Voltar ao login</Link>
      </div>
      </section>
    </div>

  );
}
import { Link } from 'react-router-dom';
