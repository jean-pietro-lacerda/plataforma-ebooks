const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

export class ApiError extends Error {
  constructor(message, status = 0) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

export function apiUrl(path) {
  return `${baseUrl}${path}`;
}

export async function apiRequest(path, { token, body, headers, ...options } = {}) {
  const requestHeaders = new Headers(headers);
  if (token) requestHeaders.set('Authorization', `Bearer ${token}`);
  if (body !== undefined && !(body instanceof FormData)) {
    requestHeaders.set('Content-Type', 'application/json');
    body = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(apiUrl(path), { ...options, body, headers: requestHeaders, credentials: 'omit' });
  } catch (error) {
    if (options.signal?.aborted) throw error;
    throw new ApiError('Não foi possível conectar à plataforma. Verifique sua conexão e tente novamente.');
  }
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const message = typeof data?.detail === 'string' ? data.detail
      : response.status === 422 ? 'Confira os dados informados e tente novamente.'
      : 'Não foi possível concluir a solicitação. Tente novamente mais tarde.';
    throw new ApiError(message, response.status);
  }
  if (data === null) throw new ApiError('A plataforma retornou uma resposta inválida.', 502);
  return data;
}
