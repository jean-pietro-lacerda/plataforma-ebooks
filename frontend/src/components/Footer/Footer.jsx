import styles from './Footer.module.css';

export function Footer() {
  return (
    <footer className={styles.footerContainer}>
      <div className={styles.footerContent}>
        
        {/* Contatos */}
          <div className={styles.footerInfo}>
            <h3 className={styles.footerTitle}>Contato</h3>

            <ul className={styles.footerContactList}>
              <li><a href="mailto:mgpf@cin.ufpe.br">mgpf@cin.ufpe.br</a></li>
              <li><a href="mailto:slso2@cin.ufpe.br">slso2@cin.ufpe.br</a></li>
              <li><a href="mailto:peba@cin.ufpe.br">peba@cin.ufpe.br</a></li>
              <li><a href="mailto:jasac@cin.ufpe.br">jasac@cin.ufpe.br</a></li>
              <li><a href="mailto:jplls@cin.ufpe.br">jplls@cin.ufpe.br</a></li>
              <li><a href="mailto:vpg2@cin.ufpe.br">vpg2@cin.ufpe.br</a></li>
              <li><a href="mailto:tvbs@cin.ufpe.br">tvbs@cin.ufpe.br</a></li>
              <li><a href="mailto:rcfm@cin.ufpe.br">rcfm@cin.ufpe.br</a></li>
            </ul>
          </div>
        
        {/* Localização */}
        <div className={styles.footerMap}>
          <h3 className={styles.footerTitle}>Localização</h3>

          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7971.085447880784!2d-34.95537543864126!3d-8.057362342924922!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x7ab1be2115430ab%3A0x20ceccca91a11dd3!2sCIn%20-%20Centro%20de%20Inform%C3%A1tica%20-%20UFPE!5e1!3m2!1spt-BR!2sbr!4v1794523235693!5m2!1spt-BR!2sbr"
            title="Localização do CIn - UFPE"
            loading="lazy"
            allowFullScreen
            referrerPolicy="strict-origin-when-cross-origin"
          />
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