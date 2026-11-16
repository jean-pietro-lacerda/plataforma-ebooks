import { Link, useSearchParams } from 'react-router-dom';
import { useApiData } from '../../../hooks/useApiData';
import { ImagemNoticia } from '../../../components/ImagemNoticia/ImagemNoticia';
import styles from '../NoticiaDetalhes/NoticiaDetalhes.module.css';

const PAGE_SIZE = 20;

export function Noticias() {
  const [parameters, setParameters] = useSearchParams();
  const value = Number(parameters.get('page') || 1);
  const page = Number.isSafeInteger(value) && value > 0 && Number.isSafeInteger((value - 1) * PAGE_SIZE) ? value : 1;
  const { data, error, loading, reload } = useApiData(`/news?offset=${(page - 1) * PAGE_SIZE}&limit=${PAGE_SIZE}`);
  return (
    <section className={styles.container} aria-busy={loading}>
      <h2>Notícias</h2>
      <Link to="/">&lt; voltar ao início</Link>
      {loading && <p role="status">Carregando notícias...</p>}
      {error && <div role="alert"><p>{error}</p><button type="button" onClick={reload}>Tentar novamente</button></div>}
      {data && <>
        {data.length === 0 && <p>Nenhuma notícia publicada nesta página.</p>}
        {data.map((item) => <article key={item.id} className={styles.resumo}>
          {item.imagem_path && <ImagemNoticia key={item.id + '-' + item.imagem_path} noticia={item} className={styles.miniatura} />}
          <div>
            <h3><Link to={`/noticias/${item.id}`}>{item.titulo}</Link></h3>
            <p>{item.conteudo.length > 180 ? item.conteudo.slice(0, 180) + '…' : item.conteudo}</p>
          </div>
        </article>)}
        <nav className={styles.paginacao} aria-label="Páginas das notícias públicas">
          <button type="button" disabled={page === 1} onClick={() => setParameters({ page: String(page - 1) })}>Anterior</button>
          <span>Página {page}</span>
          <button type="button" disabled={data.length < PAGE_SIZE} onClick={() => setParameters({ page: String(page + 1) })}>Próxima</button>
        </nav>
      </>}
    </section>
  );
}
