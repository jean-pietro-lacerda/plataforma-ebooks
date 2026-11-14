import { useState } from 'react';
import styles from './Faq.module.css';

export function Faq() {
  return (
    <div className={styles.faqContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Dúvidas Frequentes</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
      <button className={"w-full max-w-lg border-b pb-4"}>1. Como acessar a plataforma?</button>
      <div className={styles.formFaq}>

      </div>

      </section>
    </div>

  );
}