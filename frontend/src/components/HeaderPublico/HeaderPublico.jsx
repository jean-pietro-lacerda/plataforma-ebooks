import { Link } from 'react-router-dom';
import styles from './HeaderPublico.module.css';

// Importa a imagem que você acabou de salvar na pasta assets
import logoImg from '../../assets/logo-ebooks.png'; 

export function HeaderPublico() {
  return (
    <header className={styles.headerContainer}>
      
      {/* Container da Logo + Texto da Universidade */}
      <div className={styles.logoBox}>
        <img src={logoImg} alt="Logo E-Books" className={styles.logoImg} />
        <p className={styles.logoSubtitle}>
          UNIVERSIDADE<br />FEDERAL DO CARIRI
        </p>
      </div>

      <nav>
        <ul className={styles.navMenu}>
          <li className={styles.navItem}>
            <Link to="/" className={styles.navLink}>Início</Link>
          </li>
          <li className={styles.navItem}>
            <Link to="/catalogo" className={styles.navLink}>Catálogo</Link>
          </li>
          <li className={styles.navItem}>
            <Link to="/login" className={styles.navLink}>Login</Link>
          </li>
          <li className={styles.navItem}>
            <Link to="/faq" className={styles.navLink}>Dúvidas Frequentes</Link>
          </li>
        </ul>
      </nav>

    </header>
  );
}