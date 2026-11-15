import { useState } from 'react';
import styles from './Login.module.css';

export function Login() {
  return (
    <div className={styles.loginContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Login</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <div className={styles.formLogin}>
        <h3 className={styles.tituloInputLogin}>Email</h3>
        <input className={styles.inputLogin}></input>
        <h3 className={styles.tituloInputLogin}>Senha</h3>
        <input className={styles.inputLogin}></input> <br/>
        <a className={styles.textoFormLogin}>Esqueci minha senha</a>
        <a className={styles.botaoLogin}>Entrar</a>
      </div>
      </section>
    </div>

  );
}