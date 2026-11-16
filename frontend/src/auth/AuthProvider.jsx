import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { apiRequest, ApiError } from '../services/api';
import { AuthContext } from './context';

function expiration(token) {
  try {
    const encoded = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    const expiresAt = Number(JSON.parse(atob(encoded)).exp) * 1000;
    if (Number.isFinite(expiresAt) && expiresAt > Date.now()) return expiresAt;
  } catch {
    // A identidade é confirmada pelo servidor em /auth/me, nunca por este payload.
  }
  throw new ApiError('A sessão recebida é inválida ou expirou. Tente entrar novamente.');
}

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null);
  const [expired, setExpired] = useState(false);
  const current = useRef(null);
  const loginAttempt = useRef(0);

  const endSession = useCallback((wasExpired = false) => {
    loginAttempt.current += 1;
    current.current = null;
    setSession(null);
    setExpired(wasExpired);
  }, []);

  const login = useCallback(async (usuario, senha) => {
    const attempt = ++loginAttempt.current;
    const result = await apiRequest('/auth/login', { method: 'POST', body: { usuario, senha } });
    if (typeof result.access_token !== 'string' || result.token_type !== 'bearer') {
      throw new ApiError('A plataforma retornou uma sessão inválida.');
    }
    const expiresAt = expiration(result.access_token);
    const admin = await apiRequest('/auth/me', { token: result.access_token });
    if (attempt !== loginAttempt.current) throw new ApiError('A entrada foi cancelada. Tente novamente.');
    const next = { token: result.access_token, admin, expiresAt };
    current.current = next;
    setSession(next);
    setExpired(false);
  }, []);

  const request = useCallback(async (path, options) => {
    const active = current.current;
    if (!active || Date.now() >= active.expiresAt) {
      endSession(true);
      throw new ApiError('Sua sessão expirou. Entre novamente.', 401);
    }
    try {
      return await apiRequest(path, { ...options, token: active.token });
    } catch (error) {
      if (error.status === 401 && current.current === active) endSession(true);
      throw error;
    }
  }, [endSession]);

  useEffect(() => {
    if (!session) return undefined;
    let timer;
    function checkExpiration() {
      if (current.current !== session) return;
      const remaining = session.expiresAt - Date.now();
      if (remaining <= 0) endSession(true);
      else {
        clearTimeout(timer);
        timer = setTimeout(checkExpiration, Math.min(remaining, 2147483647));
      }
    }
    checkExpiration();
    window.addEventListener('focus', checkExpiration);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('focus', checkExpiration);
    };
  }, [session, endSession]);

  const value = useMemo(() => ({
    admin: session?.admin ?? null, expired, login, request,
    logout: () => endSession(false),
  }), [session, expired, login, request, endSession]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
