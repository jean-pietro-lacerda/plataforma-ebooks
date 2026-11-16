import { useState } from 'react';
import { apiUrl } from '../../services/api';

export function ImagemNoticia({ noticia, className }) {
  const [failed, setFailed] = useState(false);
  if (!noticia.imagem_path || failed) return <div className={className} role="img" aria-label="Notícia sem imagem disponível" />;
  return <img className={className} src={apiUrl(`/news/${noticia.id}/image`)} alt={noticia.titulo} loading="lazy" onError={() => setFailed(true)} />;
}
