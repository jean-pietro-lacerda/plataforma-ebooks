import { Link, useParams } from 'react-router-dom';
import { useApiData } from '../../../hooks/useApiData';
import { ImagemNoticia } from '../../../components/ImagemNoticia/ImagemNoticia';
import styles from './NoticiaDetalhes.module.css';

export function NoticiaDetalhes() {
  const { id } = useParams();
  const valid = /^[1-9]\d*$/.test(id);
  const { data, loading, error, reload } = useApiData(valid ? `/news/${id}` : null);
  return (
    <article className={styles.container} aria-busy={loading}>
      <Link to="/">&lt; voltar ao início</Link>
      {loading && <p role="status">Carregando notícia...</p>}
      {!valid && <p role="alert">Notícia não encontrada.</p>}
      {error && <div role="alert"><p>{error}</p><button type="button" onClick={reload}>Tentar novamente</button></div>}
      {data && <>
        <h1>{data.titulo}</h1>
        {data.data_publicacao && <time dateTime={data.data_publicacao}>{new Date(data.data_publicacao).toLocaleDateString('pt-BR')}</time>}
        {data.imagem_path && <ImagemNoticia key={data.id + '-' + data.imagem_path} noticia={data} className={styles.imagem} />}
        <p className={styles.conteudo}>{data.conteudo}</p>
      </>}
    </article>
  );
}
