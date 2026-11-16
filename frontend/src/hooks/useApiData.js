import { useEffect, useState } from 'react';
import { apiRequest } from '../services/api';

export function useApiData(path) {
  const [result, setResult] = useState(null);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    if (!path) return undefined;
    const controller = new AbortController();
    apiRequest(path, { signal: controller.signal })
      .then((data) => { if (!controller.signal.aborted) setResult({ path, attempt, data, error: '' }); })
      .catch((error) => {
        if (!controller.signal.aborted) setResult({ path, attempt, data: null, error: error.message });
      });
    return () => controller.abort();
  }, [path, attempt]);
  const ready = result?.path === path && result?.attempt === attempt;
  return { data: ready ? result.data : null, error: ready ? result.error : '', loading: Boolean(path) && !ready, reload: () => setAttempt((value) => value + 1) };
}
