import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useApiData } from '../../../hooks/useApiData';
import { ImagemNoticia } from '../../../components/ImagemNoticia/ImagemNoticia';
import styles from './Home.module.css';

export function Home() {
  const { data: noticias, loading, error, reload } = useApiData('/news/highlights');
  const [selected, setSelected] = useState(null);
  const index = Math.max(0, noticias?.findIndex((item) => item.id === selected) ?? 0);
  const noticia = noticias?.[index];
  function mudar(delta) {
    setSelected(noticias[(index + delta + noticias.length) % noticias.length].id);
  }
  return (
    <div className={styles.homeContainer}>
      <section className={styles.carrossel} aria-label="Notícias em destaque" aria-busy={loading}>
        {loading && <p role="status" className={styles.aviso}>Carregando destaques...</p>}
        {error && <div role="alert" className={styles.aviso}><p>{error}</p><button type="button" onClick={reload}>Tentar novamente</button></div>}
        {noticias?.length === 0 && <p role="status" className={styles.aviso}>Não há destaques publicados no momento.</p>}
        {noticia && <>
          <ImagemNoticia key={noticia.id + '-' + noticia.imagem_path} noticia={noticia} className={styles.carrosselImagem} />
          <div className={styles.carrosselOverlay}>
            <Link to={'/noticias/' + noticia.id} className={styles.carrosselLink}>
              <h2 className={styles.carrosselTitulo}>{noticia.titulo}</h2>
              <p className={styles.carrosselSubtitulo}>{noticia.conteudo.length > 180 ? noticia.conteudo.slice(0, 180) + '…' : noticia.conteudo}</p>
            </Link>
          </div>
          {noticias.length > 1 && <>
            <button type="button" aria-label="Notícia anterior" onClick={() => mudar(-1)} className={styles.seta + ' ' + styles.setaEsquerda}>&lt;</button>
            <button type="button" aria-label="Próxima notícia" onClick={() => mudar(1)} className={styles.seta + ' ' + styles.setaDireita}>&gt;</button>
          </>}
        </>}
      </section>
      <section className={styles.apresentacao}>
        <h3 className={styles.apresentacaoTitulo}>Apresentação</h3>
        <p className={styles.apresentacaoTexto}>
          Bem-vindo ao nosso universo de eBooks! Aqui, você encontra uma variedade de livros digitais para
          explorar novos conhecimentos, descobrir histórias incríveis e mergulhar no mundo da leitura. Nossa
          plataforma foi criada para oferecer uma experiência simples, prática e acessível, permitindo que você
          encontre suas próximas leituras favoritas em poucos cliques. Explore nosso catálogo e descubra um
          mundo de possibilidades a cada página!
        </p>
      </section>
    </div>
  );
}
