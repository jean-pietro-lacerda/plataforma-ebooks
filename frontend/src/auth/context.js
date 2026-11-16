import { createContext, useContext } from 'react';

export const AuthContext = createContext(null);

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('Autenticação fora do provedor.');
  return context;
}
