import { useState } from 'react';
import styles from './NovaSenha.module.css';

export function NovaSenha() {
  return (
    <div className={styles.novaSenhaContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Esqueci minha senha</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formNovaSenha}>
        <h3 className={styles.tituloInputNovaSenha}>Digite sua nova senha:</h3>
        <input className={styles.inputNovaSenha}></input>
        <h3 className={styles.tituloInputNovaSenha}>Confirme sua nova senha:</h3>
        <input className={styles.inputNovaSenha}></input> <br/>
        <a className={styles.botaoNovaSenha}>Confirmar</a>
      </div>
      </section>
    </div>

  );
}