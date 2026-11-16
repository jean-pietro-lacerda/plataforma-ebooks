import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { HeaderAdmin } from '../components/HeaderAdmin/HeaderAdmin';
import { useAuth } from './context';

export function RequireAdmin() {
  const { admin } = useAuth();
  const location = useLocation();
  if (!admin) return <Navigate to="/login" replace state={{ from: location.pathname + location.search }} />;
  return <><HeaderAdmin /><Outlet /></>;
}
