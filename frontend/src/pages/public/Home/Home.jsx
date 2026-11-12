import { useState } from 'react';
import styles from './Home.module.css';

// Dados fictícios baseados no protótipo para preencher o carrossel
const NOTICIAS = [
  {
    id: 1,
    titulo: "Edital aberto para novas publicações",
    subtitulo: "Clique aqui para ver o edital",
    imagem: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=1200&auto=format&fit=crop"
  },
  {
    id: 2,
    titulo: "Novos livros disponíveis na plataforma",
    subtitulo: "25 novos livros foram publicados nesse domingo 20/09",
    imagem: "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=1200&auto=format&fit=crop"
  },
  {
    id: 3,
    titulo: "Aluna da UFCA publica seu próprio livro",
    subtitulo: "Aluna da UFCA escreveu e publicou um livro na nossa plataforma",
    imagem: "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1200&auto=format&fit=crop"
  }
];

export function Home() {
  // Estado para controlar qual notícia está a ser apresentada (começa no índice 0)
  const [indiceAtual, setIndiceAtual] = useState(0);

  // Função para avançar a imagem
  const proximaNoticia = () => {
    setIndiceAtual((indice) => (indice === NOTICIAS.length - 1 ? 0 : indice + 1));
  };

  // Função para recuar a imagem
  const noticiaAnterior = () => {
    setIndiceAtual((indice) => (indice === 0 ? NOTICIAS.length - 1 : indice - 1));
  };

  const noticiaEmDestaque = NOTICIAS[indiceAtual];

  return (
    <div className={styles.homeContainer}>
      
      {/* Secção do Carrossel */}
      <section className={styles.carrossel}>
        <img 
          src={noticiaEmDestaque.imagem} 
          alt={noticiaEmDestaque.titulo} 
          className={styles.carrosselImagem} 
        />
        
        <div className={styles.carrosselOverlay}>
          <h2 className={styles.carrosselTitulo}>{noticiaEmDestaque.titulo}</h2>
          <p className={styles.carrosselSubtitulo}>{noticiaEmDestaque.subtitulo}</p>
        </div>

        <button onClick={noticiaAnterior} className={`${styles.seta} ${styles.setaEsquerda}`}>
          &lt;
        </button>
        <button onClick={proximaNoticia} className={`${styles.seta} ${styles.setaDireita}`}>
          &gt;
        </button>
      </section>

      {/* Secção de Apresentação Oficial */}
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