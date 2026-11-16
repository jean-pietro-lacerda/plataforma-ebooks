import { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './LivroCard.module.css';

export function LivroCard({ id, titulo, capaUrl }) {
  const [failedCover, setFailedCover] = useState(null);
  return (
    /* Usamos o Link para que, no futuro, clicar no livro leve para a página de detalhes dele */
    <Link to={`/livro/${id}`} className={styles.cardContainer}>
      
      {capaUrl && failedCover !== capaUrl ? <img
        src={capaUrl} 
        alt={`Capa do livro ${titulo}`} 
        className={styles.capa} 
        loading="lazy"
        onError={() => setFailedCover(capaUrl)}
      /> : <div className={`${styles.capa} ${styles.semCapa}`}>Capa indisponível</div>}
      
      <div className={styles.info}>
        <h4 className={styles.titulo}>{titulo}</h4>
      </div>
      
    </Link>
  );
}
