import styles from './Catalogo.module.css';
import { LivroCard } from '../../../components/LivroCard/LivroCard';

// Lista de temas baseada no protótipo
const TEMAS = [
  "Artes", "Biologia", "Culinária", "Filosofia", 
  "Física", "Geografia", "Gramática", "História", 
  "Literatura", "Matemática", "Música", "Química"
];

// Dados provisórios para visualizarmos a grelha
const LIVROS_EXEMPLO = [
  { id: 1, titulo: "Artes: Propostas...", capa: "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=300&auto=format&fit=crop" },
  { id: 2, titulo: "Biologia Marinha", capa: "https://images.unsplash.com/photo-1582967201267-27a3f3b64c01?q=80&w=300&auto=format&fit=crop" },
  { id: 3, titulo: "A ciência da co...", capa: "https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=300&auto=format&fit=crop" },
  { id: 4, titulo: "A metafísica dos...", capa: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=300&auto=format&fit=crop" },
  { id: 5, titulo: "A história da físi...", capa: "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?q=80&w=300&auto=format&fit=crop" },
  { id: 6, titulo: "Geografia Física", capa: "https://images.unsplash.com/photo-1529156069898-49953eb1b5b6?q=80&w=300&auto=format&fit=crop" },
  { id: 7, titulo: "A história do Bra...", capa: "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=300&auto=format&fit=crop" },
  { id: 8, titulo: "A hora da estrela", capa: "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=300&auto=format&fit=crop" }
];

export function Catalogo() {
  return (
    <div className={styles.catalogoContainer}>
      
      {/* Barra Lateral de Filtros */}
      <aside className={styles.sidebar}>
        <h3 className={styles.tituloSidebar}>Temas</h3>
        <ul className={styles.listaTemas}>
          {TEMAS.map((tema) => (
            <li key={tema} className={styles.temaItem}>
              {tema}
            </li>
          ))}
        </ul>
      </aside>

      {/* Conteúdo Central */}
      <section className={styles.conteudoPrincipal}>
        
        {/* Cabeçalho com Título e Busca */}
        <div className={styles.cabecalhoConteudo}>
          <h2 className={styles.tituloPagina}>Catálogo de Livros</h2>
          
          <div className={styles.buscaContainer}>
            <input 
              type="text" 
              placeholder="Pesquise aqui..." 
              className={styles.inputBusca}
            />
          </div>
        </div>

        {/* Grelha de Livros */}
        <div className={styles.gradeLivros}>
          {LIVROS_EXEMPLO.map((livro) => (
            <LivroCard 
              key={livro.id} 
              id={livro.id} 
              titulo={livro.titulo} 
              capaUrl={livro.capa} 
            />
          ))}
        </div>

      </section>

    </div>
  );
}