import { useState } from 'react';
import styles from './EsqueciMinhaSenha.module.css';

export function EsqueciMinhaSenha() {
  return (
    <div className={styles.esqueciMinhaSenhaContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Esqueci minha senha</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formEsqueciMinhaSenha}>
        <h3 className={styles.tituloInputEsqueciMinhaSenha}>Email</h3>
        <input className={styles.inputEsqueciMinhaSenha}></input>
        <a className={styles.botaoEsqueciMinhaSenha}>Confirmar</a>
      </div>
      </section>
    </div>

  );
}