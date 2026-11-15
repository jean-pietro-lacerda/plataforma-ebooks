import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import styles from './LivroDetalhes.module.css';

export function LivroDetalhes() {
  const { id } = useParams();
  const [resultado, setResultado] = useState(null);
  const [capaIndisponivel, setCapaIndisponivel] = useState(false);
  const [erro, setErro] = useState('');

  useEffect(() => {
    const controller = new AbortController();
    setResultado(null);
    setErro('');
    setCapaIndisponivel(false);

    if (!/^[1-9]\d*$/.test(id)) {
      setResultado({ id, livro: null });
      setErro('Livro não encontrado.');
      return () => controller.abort();
    }

    const apiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

    async function buscarLivro() {
      try {
        const response = await fetch(`${apiUrl}/books/${id}`, { signal: controller.signal });
        if (!response.ok) {
          throw new Error(response.status === 404
            ? 'Livro não encontrado.'
            : 'Não foi possível carregar o livro. Tente novamente mais tarde.');
        }
        const livro = await response.json();
        if (!controller.signal.aborted) {
          setResultado({ id, livro });
        }
      } catch (error) {
        if (!controller.signal.aborted) {
          setResultado({ id, livro: null });
          setErro(error instanceof TypeError
            ? 'Não foi possível conectar à biblioteca. Tente novamente mais tarde.'
            : error.message);
        }
      }
    }

    buscarLivro();
    return () => controller.abort();
  }, [id]);

  const carregando = resultado?.id !== id;
  const livro = carregando ? null : resultado.livro;

  return (
    <div className={styles.detalhesContainer}>
      <Link to="/catalogo" className={styles.voltarLink}>
        &lt; voltar
      </Link>

      {carregando && <p role="status">Carregando livro...</p>}
      {!carregando && erro && <p role="alert">{erro}</p>}

      {livro && (
        <div className={styles.conteudoPrincipal}>
          <aside className={styles.colunaEsquerda}>
            {livro.url_capa && !capaIndisponivel ? (
              <img
                src={livro.url_capa}
                alt={`Capa do livro ${livro.titulo}`}
                className={styles.capaLivro}
                onError={() => setCapaIndisponivel(true)}
              />
            ) : <p>Capa indisponível.</p>}

            <div className={styles.autoresBox}>
              <strong>Autores:</strong>
              {livro.autores.length > 0
                ? livro.autores.map((autor, index) => <div key={index}>{autor}</div>)
                : <p>Autoria não informada.</p>}
            </div>

            {livro.url_pagina_oficial && (
              <a href={livro.url_pagina_oficial} className={styles.botaoBaixar} target="_blank" rel="noopener noreferrer">
                Acessar livro
              </a>
            )}
            {livro.link_download && (
              <a href={livro.link_download} className={styles.botaoBaixar} target="_blank" rel="noopener noreferrer">
                Abrir versão digital
              </a>
            )}
            {!livro.url_pagina_oficial && !livro.link_download && <p>Acesso indisponível.</p>}
          </aside>

          <section className={styles.colunaDireita}>
            <h1 className={styles.tituloLivro}>{livro.titulo}</h1>
          </section>
        </div>
      )}
    </div>
  );
}
