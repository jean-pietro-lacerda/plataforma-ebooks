import { useAuth } from '../../../auth/context';
import styles from '../Admin.module.css';

export function MinhaConta() {
  const { admin } = useAuth();
  return (
    <section className={styles.container}>
      <h2>Minha conta</h2>
      <p>Você está conectado como administrador.</p>
      <p><strong>Usuário:</strong> {admin.usuario}</p>
      <Link to="/admin/noticias">Gerenciar notícias e destaques</Link>
    </section>
  );
}
import { Link } from 'react-router-dom';
