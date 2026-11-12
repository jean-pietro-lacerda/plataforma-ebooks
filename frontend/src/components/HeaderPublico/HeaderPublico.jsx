import { Link } from 'react-router-dom';
import styles from './HeaderPublico.module.css';

// Importa a imagem que você acabou de salvar na pasta assets
import logoImg from '../../assets/logo-ebooks.png'; 

// Importa os ícones do menu
import inicioIcon from '../../assets/icons/home_icone.png';
import catalogoIcon from '../../assets/icons/livro_icone.png';
import loginIcon from '../../assets/icons/cabeca_icone.png';
import duvidasIcon from '../../assets/icons/interrogacao_icone.png';

export function HeaderPublico() {
  return (
    <header className={styles.headerContainer}>
      
      {/* Container da Logo + Texto da Universidade */}
      <div className={styles.logoBox}>
        <img src={logoImg} alt="Logo E-Books" className={styles.logoImg} />
      </div>

      <nav>
        <ul className={styles.navMenu}>
          <li className={styles.navItem}>
            <Link to="/" className={styles.navLink}>
              <img src={inicioIcon} alt="" className={styles.navIcon} />
              Início
            </Link>
          </li>
          <li className={styles.navItem}>
            <Link to="/catalogo" className={styles.navLink}>
              <img src={catalogoIcon} alt="" className={styles.navIcon} />
              Catálogo
            </Link>
          </li>
          <li className={styles.navItem}>
            <Link to="/login" className={styles.navLink}>
              <img src={loginIcon} alt="" className={styles.navIcon} />
              Login
            </Link>
          </li>
          <li className={styles.navItem}>
            <Link to="/faq" className={styles.navLink}>
              <img src={duvidasIcon} alt="" className={styles.navIcon} />
              Dúvidas Frequentes
            </Link>
          </li>
        </ul>
      </nav>

    </header>
  );
}