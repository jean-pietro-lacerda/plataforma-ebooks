import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

export function Footer() {
  return (
    <footer className={styles.footerContainer}>
      <div className={styles.footerContent}>
        
        {/* Informações Institucionais */}
        <div className={styles.footerInfo}>
          <h3 className={styles.footerTitle}>Plataforma E-books UFCA</h3>
          <p><strong>Universidade Federal do Cariri</strong></p>
          <p>Pró-Reitoria de Pesquisa, Pós-graduação e Inovação (PRPI)</p>
        </div>
        
        {/* Links Rápidos */}
        <div className={styles.footerLinks}>
          <h4>Navegação</h4>
          <ul>
            <li><Link to="/">Início</Link></li>
            <li><Link to="/catalogo">Catálogo</Link></li>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/faq">Dúvidas Frequentes</Link></li>
          </ul>
        </div>
        
      </div>
      
      {/* Direitos Autorais e Site */}
      <div className={styles.footerBottom}>
        <p>
          &copy; {new Date().getFullYear()} Plataforma de E-books UFCA. Todos os direitos reservados. 
          <br /> {/* Quebra a linha para o site ficar embaixo */}
          <a href="https://www.ufca.edu.br" target="_blank" rel="noopener noreferrer" className={styles.siteUrl}>
            www.ufca.edu.br
          </a>
        </p>
      </div>
    </footer>
  );
}