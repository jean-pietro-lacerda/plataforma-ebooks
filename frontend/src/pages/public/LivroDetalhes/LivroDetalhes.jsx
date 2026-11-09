import { useParams, Link } from 'react-router-dom';
import styles from './LivroDetalhes.module.css';

// Dados fictícios baseados no protótipo "Artes"
const LIVRO_MOCK = {
  id: 1,
  titulo: "Artes: Propostas e acessos",
  autores: ["Adriana Gomes de Oliveira", "Ana Lucia Iara Gaborim-Moreira"],
  capaUrl: "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=400&auto=format&fit=crop",
  descricao: [
    "Este livro apresenta 23 capítulos com artigos de pesquisadores das artes atuantes em diferentes instituições de ensino superior no país e no exterior.",
    "Inicialmente, é apresentada uma discussão teórica a respeito das propostas epistêmico-terminológicas dos termos \"arte\" e \"artes\". Em seguida, textos abordando diversas áreas artísticas são organizados de acordo com as experiências e reflexões dos autores relacionadas ao cinema, fotografia, teatro, dança, música, e suas inter-relações, além da educação das artes.",
    "A coletânea se encerra com dois artigos que entrelaçam explicitamente as pesquisas em arte com o momento atual que a humanidade enfrenta: o isolamento social devido à pandemia que alterou a vida de todos nós."
  ],
  pdfUrl: "#"
};

export function LivroDetalhes() {
  const { id } = useParams(); // Prepara o componente para buscar o livro correto na base de dados futuramente

  return (
    <div className={styles.detalhesContainer}>
      
      <Link to="/catalogo" className={styles.voltarLink}>
        &lt; voltar
      </Link>

      <div className={styles.conteudoPrincipal}>
        
        {/* Lado Esquerdo: Capa, Autores e Botão */}
        <aside className={styles.colunaEsquerda}>
          <img 
            src={LIVRO_MOCK.capaUrl} 
            alt={`Capa do livro ${LIVRO_MOCK.titulo}`} 
            className={styles.capaLivro} 
          />
          
          <div className={styles.autoresBox}>
            <strong>Autores:</strong>
            {LIVRO_MOCK.autores.map((autor, index) => (
              <div key={index}>{autor}</div>
            ))}
          </div>

          <a href={LIVRO_MOCK.pdfUrl} className={styles.botaoBaixar} download>
            Baixar pdf
          </a>
        </aside>

        {/* Lado Direito: Título e Descrição */}
        <main className={styles.colunaDireita}>
          <h1 className={styles.tituloLivro}>{LIVRO_MOCK.titulo}</h1>
          
          <div className={styles.descricao}>
            {LIVRO_MOCK.descricao.map((paragrafo, index) => (
              <p key={index}>{paragrafo}</p>
            ))}
          </div>
        </main>

      </div>
    </div>
  );
}