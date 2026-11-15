import { useState } from 'react';
import styles from './Faq.module.css';

export function Faq() {
  return (
    <div className={styles.faqContainer}>
      <div className={styles.cabecalhoConteudo}>
        <h2>Dúvidas Frequentes</h2>
      </div>
      <section className={styles.conteudoPrincipal}>
{/*
      <button className={"w-full max-w-lg border-b pb-4"}>1. Como acessar a plataforma?</button>
*/}
        <details className={styles.faqDetails}>
          <summary className={styles.faqSummary}>
            1. Como acessar a plataforma?
          </summary>
            <span className={styles.faqSpan}>
              <p className={styles.faqP}>
                Caso você seja estudante, é possível utilizar livremente a plataforma sem a necessidade de criar uma conta.
              </p>
            </span>
        </details>
        <details className={styles.faqDetails}>
          <summary className={styles.faqSummary}>
            2. Como Publicar ebooks?
          </summary>
            <span className={styles.faqSpan}>
              <p className={styles.faqP}>
                Somente administradores podem publicar livros.
              </p>
            </span>
        </details>
        <details className={styles.faqDetails}>
          <summary className={styles.faqSummary}>
            3. Como encontrar um livro específico?
{/*            <div className={styles.arrow}></div>*/}
          </summary>
            <span className={styles.faqSpan}>
              <p className={styles.faqP}>
                Na parte do catálogo, você pode pesquisar pelo nome do livro ou filtrar livros por tema.
              </p>
                
            </span>
        </details>
      </section>
    </div>

  );
}