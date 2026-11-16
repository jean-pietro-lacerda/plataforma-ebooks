import { useSearchParams } from 'react-router-dom';
import styles from './Catalogo.module.css';
import { LivroCard } from '../../../components/LivroCard/LivroCard';
import { useApiData } from '../../../hooks/useApiData';

// Rotulos do prototipo associados aos assuntos pesquisaveis no Gutendex.
const TEMAS = [
  ['Artes', 'art'], ['Biologia', 'biology'], ['Culinária', 'cookery'],
  ['Filosofia', 'philosophy'], ['Física', 'physics'], ['Geografia', 'geography'],
  ['Gramática', 'grammar'], ['História', 'history'], ['Literatura', 'literature'],
  ['Matemática', 'mathematics'], ['Música', 'music'], ['Química', 'chemistry'],
];

export function Catalogo() {
  const [parameters, setParameters] = useSearchParams();
  const search = parameters.get('search') || '';
  const topic = parameters.get('topic') || '';
  const requestedPage = Number(parameters.get('page') || 1);
  const page = Number.isSafeInteger(requestedPage) && requestedPage > 0 ? requestedPage : 1;
  const query = new URLSearchParams({ page: String(page) });
  if (search) query.set('search', search);
  if (topic) query.set('topic', topic);
  const { data, loading, error, reload } = useApiData('/books?' + query);

  function update(name, value) {
    setParameters((previous) => {
      const next = new URLSearchParams(previous);
      if (value) next.set(name, value);
      else next.delete(name);
      if (name !== 'page') next.delete('page');
      return next;
    });
  }
  function pesquisar(event) {
    event.preventDefault();
    update('search', new FormData(event.currentTarget).get('search').trim());
  }
  return (
    <div className={styles.catalogoContainer}>
      <aside className={styles.sidebar}>
        <h3 className={styles.tituloSidebar}>Temas</h3>
        <ul className={styles.listaTemas}>
          <li><button type="button" aria-pressed={!topic} className={styles.temaItem + (!topic ? ' ' + styles.temaAtivo : '')} onClick={() => update('topic', '')}>Todos os temas</button></li>
          {TEMAS.map(([label, value]) => (
            <li key={value}>
              <button type="button" aria-pressed={topic === value} className={styles.temaItem + (topic === value ? ' ' + styles.temaAtivo : '')} onClick={() => update('topic', value)}>{label}</button>
            </li>
          ))}
        </ul>
      </aside>
      <section className={styles.conteudoPrincipal} aria-busy={loading}>
        <div className={styles.cabecalhoConteudo}>
          <h2 className={styles.tituloPagina}>Catálogo de Livros</h2>
          <form key={search} className={styles.buscaContainer} onSubmit={pesquisar} role="search">
            <label className={styles.rotuloBusca} htmlFor="catalogo-busca">Pesquisar por título ou autor</label>
            <input id="catalogo-busca" name="search" type="search" placeholder="Pesquise aqui..." defaultValue={search} className={styles.inputBusca} />
            <button type="submit" className={styles.botao}>Pesquisar</button>
          </form>
        </div>
        {loading && <p role="status">Carregando livros...</p>}
        {error && <div role="alert"><p>{error}</p><button type="button" className={styles.botao} onClick={reload}>Tentar novamente</button></div>}
        {data && <>
          <p role="status">{data.count} livro(s) encontrado(s).</p>
          {data.results.length === 0 && <p>Nenhum livro encontrado para esta pesquisa.</p>}
          <div className={styles.gradeLivros}>
            {data.results.map((livro) => <LivroCard key={livro.id} id={livro.id} titulo={livro.titulo} capaUrl={livro.url_capa} />)}
          </div>
          <nav className={styles.paginacao} aria-label="Páginas do catálogo">
            <button type="button" className={styles.botao} disabled={!data.previous || page === 1} onClick={() => update('page', String(page - 1))}>Anterior</button>
            <span>Página {page}</span>
            <button type="button" className={styles.botao} disabled={!data.next} onClick={() => update('page', String(page + 1))}>Próxima</button>
          </nav>
        </>}
      </section>
    </div>
  );
}
