import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../auth/context';
import styles from '../../pages/admin/Admin.module.css';

export function HeaderAdmin() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  function sair() {
    logout();
    navigate('/login', { replace: true });
  }
  return (
    <nav className={styles.navigation} aria-label="Administração">
      <Link to="/admin">Minha conta</Link>
      <Link to="/admin/noticias">Notícias</Link>
      <button type="button" onClick={sair}>Sair</button>
    </nav>
  );
}
