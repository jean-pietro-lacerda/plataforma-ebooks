import { Link } from 'react-router-dom';
import styles from './LivroCard.module.css';

export function LivroCard({ id, titulo, capaUrl }) {
  return (
    /* Usamos o Link para que, no futuro, clicar no livro leve para a página de detalhes dele */
    <Link to={`/livro/${id}`} className={styles.cardContainer}>
      
      <img 
        src={capaUrl} 
        alt={`Capa do livro ${titulo}`} 
        className={styles.capa} 
      />
      
      <div className={styles.info}>
        <h4 className={styles.titulo}>{titulo}</h4>
      </div>
      
    </Link>
  );
}