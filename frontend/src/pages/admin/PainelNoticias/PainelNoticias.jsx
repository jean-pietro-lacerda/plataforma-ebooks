import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../../auth/context';
import styles from '../Admin.module.css';

const INITIAL = { titulo: '', conteudo: '', publicada: false, destaque: false, ordem: '0' };
const PAGE_SIZE = 20;
const IMAGE_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp']);

export function PainelNoticias() {
  const { request } = useAuth();
  const [offset, setOffset] = useState(0);
  const [version, setVersion] = useState(0);
  const [listing, setListing] = useState(null);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(INITIAL);
  const [file, setFile] = useState(null);
  const [fileKey, setFileKey] = useState(0);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const ready = listing?.offset === offset && listing?.version === version;
  const items = ready ? listing.items : [];
  const busy = saving || deleting;

  useEffect(() => {
    const controller = new AbortController();
    request('/news/admin?offset=' + offset + '&limit=' + PAGE_SIZE, { signal: controller.signal })
      .then((data) => { if (!controller.signal.aborted) setListing({ offset, version, items: data, error: '' }); })
      .catch((err) => { if (!controller.signal.aborted) setListing({ offset, version, items: [], error: err.message }); });
    return () => controller.abort();
  }, [request, offset, version]);

  function reset() {
    setEditing(null); setForm(INITIAL); setFile(null); setFileKey((value) => value + 1);
  }
  function change(event) {
    const { name, type, checked, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: type === 'checkbox' ? checked : value }));
  }
  function edit(item) {
    setEditing(item.id);
    setForm({ titulo: item.titulo, conteudo: item.conteudo, publicada: item.publicada, destaque: item.destaque, ordem: String(item.ordem) });
    setFile(null); setFileKey((value) => value + 1); setError(''); setMessage('');
    document.getElementById('noticia-titulo')?.focus();
  }
  async function save(event) {
    event.preventDefault();
    if (busy) return;
    if (!form.titulo.trim() || !form.conteudo.trim()) { setError('Informe o título e o conteúdo.'); return; }
    if (file && (!IMAGE_TYPES.has(file.type) || file.size > 5 * 1024 * 1024)) {
      setError('Use uma imagem JPEG, PNG ou WebP de até 5 MiB.'); return;
    }
    setSaving(true); setError(''); setMessage('');
    let saved = false;
    try {
      const item = await request(editing ? '/news/' + editing : '/news', {
        method: editing ? 'PATCH' : 'POST',
        body: { ...form, titulo: form.titulo.trim(), ordem: Number(form.ordem) },
      });
      saved = true;
      setEditing(item.id);
      if (file) {
        const upload = new FormData();
        upload.append('file', file);
        await request('/news/' + item.id + '/image', { method: 'POST', body: upload });
      }
      reset(); setMessage('Notícia salva com sucesso.'); setOffset(0);
    } catch (err) {
      setError(saved ? 'A notícia foi salva, mas a imagem não foi enviada. Tente novamente. ' + err.message : err.message);
    } finally {
      setVersion((value) => value + 1);
      setSaving(false);
    }
  }
  async function remove(id) {
    if (busy) return;
    setDeleting(true); setError(''); setMessage('');
    try {
      await request('/news/' + id, { method: 'DELETE' });
      if (editing === id) reset();
      setConfirmDelete(null); setMessage('Notícia excluída.');
      if (items.length === 1 && offset > 0) setOffset((value) => Math.max(0, value - PAGE_SIZE));
      setVersion((value) => value + 1);
    } catch (err) { setError(err.message); }
    finally { setDeleting(false); }
  }

  return (
    <section className={styles.container}>
      <h2>Notícias e destaques</h2>
      {error && <p role="alert" className={styles.message}>{error}</p>}
      {message && <p role="status">{message}</p>}
      <form className={styles.editor} onSubmit={save} aria-busy={saving}>
        <fieldset disabled={busy} className={styles.fields}>
          <legend>{editing ? 'Editar notícia' : 'Nova notícia'}</legend>
          <label htmlFor="noticia-titulo">Título</label>
          <input id="noticia-titulo" name="titulo" maxLength={255} required value={form.titulo} onChange={change} />
          <label htmlFor="noticia-conteudo">Conteúdo</label>
          <textarea id="noticia-conteudo" name="conteudo" rows={6} required value={form.conteudo} onChange={change} />
          <label className={styles.checkbox}><input name="publicada" type="checkbox" checked={form.publicada} onChange={change} />Publicada</label>
          <label className={styles.checkbox}><input name="destaque" type="checkbox" checked={form.destaque} onChange={change} />Em destaque</label>
          <label htmlFor="noticia-ordem">Ordem dos destaques</label>
          <input id="noticia-ordem" name="ordem" type="number" min="0" step="1" required value={form.ordem} onChange={change} />
          <label htmlFor="noticia-imagem">Imagem (JPEG, PNG ou WebP, até 5 MiB)</label>
          <input key={fileKey} id="noticia-imagem" type="file" accept="image/jpeg,image/png,image/webp" onChange={(event) => setFile(event.target.files[0] || null)} />
          <div className={styles.actions}>
            <button type="submit">{saving ? 'Salvando...' : 'Salvar notícia'}</button>
            {editing && <button type="button" onClick={() => { reset(); setError(''); }}>Cancelar edição</button>}
          </div>
        </fieldset>
      </form>
      <h3>Notícias cadastradas</h3>
      {!ready && <p role="status">Carregando notícias...</p>}
      {ready && listing.error && <div role="alert"><p>{listing.error}</p><button type="button" onClick={() => setVersion((value) => value + 1)}>Tentar novamente</button></div>}
      {ready && !listing.error && items.length === 0 && <p>Nenhuma notícia cadastrada nesta página.</p>}
      <div className={styles.items} aria-busy={!ready}>
        {items.map((item) => (
          <article key={item.id} id={'noticia-' + item.id} className={styles.item}>
            <h4>{item.titulo}</h4>
            <p>{item.publicada ? 'Publicada' : 'Rascunho'} · {item.destaque ? 'Em destaque' : 'Sem destaque'} · Ordem: {item.ordem}</p>
            {item.imagem_path && <p>Imagem cadastrada.</p>}
            {item.publicada && <Link to={'/noticias/' + item.id}>Visualizar notícia</Link>}
            <div className={styles.actions}>
              <button type="button" disabled={busy} onClick={() => edit(item)}>Editar</button>
              {confirmDelete === item.id ? <>
                <span>Excluir esta notícia?</span>
                <button type="button" disabled={busy} onClick={() => remove(item.id)}>Confirmar exclusão</button>
                <button type="button" disabled={busy} onClick={() => setConfirmDelete(null)}>Cancelar</button>
              </> : <button type="button" disabled={busy} onClick={() => setConfirmDelete(item.id)}>Excluir</button>}
            </div>
          </article>
        ))}
      </div>
      <nav className={styles.actions} aria-label="Páginas das notícias">
        <button type="button" disabled={offset === 0 || busy || !ready} onClick={() => setOffset((value) => Math.max(0, value - PAGE_SIZE))}>Anterior</button>
        <span>Página {Math.floor(offset / PAGE_SIZE) + 1}</span>
        <button type="button" disabled={items.length < PAGE_SIZE || busy || !ready} onClick={() => setOffset((value) => value + PAGE_SIZE)}>Próxima</button>
      </nav>
    </section>
  );
}
