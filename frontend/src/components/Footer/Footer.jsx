import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

export function Footer() {
  return (
    <footer className={styles.footerContainer}>
      <div className={styles.footerContent}>
        
        {/* Informações do Projeto */}
        <div className={styles.footerInfo}>
          <h3 className={styles.footerTitle}>Ebooks</h3>
          <p><strong>Projeto acadêmico</strong></p>
          <p>Desenvolvido na disciplina de Desenvolvimento de Software</p>
          <p>Centro de Informática - UFPE </p>
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
      
      {/* Direitos Autorais*/}
      <div className={styles.footerBottom}>
        <p>
          &copy; {new Date().getFullYear()} Ebooks. Todos os direitos reservados.
        </p>
      </div>
    </footer>
  );
}