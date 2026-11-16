# Sprint 3 — Planejamento de testes e matriz de rastreabilidade

**Projeto:** Plataforma de e-books  
**Base:** histórias da Sprint 2 fornecidas pela equipe + código da `main` consultado em 15/11/2026  
**Status:** rascunho para revisão da equipe, **elaborado com apoio de IA**  
**Escopo:** testes das funcionalidades existentes; sem exigir que telas ainda demonstrativas sejam tratadas como completas.

> **Atenção acadêmica:** a atividade solicita um projeto *manual* antes da geração da suíte pela LLM. Este documento é um rascunho estruturado com IA e **não deve ser apresentado como elaboração exclusivamente manual**. A equipe precisa revisar, ajustar e assumir os critérios de aceitação, as partições e os oráculos antes do commit.

## 1. Triagem das histórias antigas

As histórias de alunos, professores e funcionários foram consolidadas considerando o sistema atual: acesso público às informações e perfil autenticado de **administrador**.

| História(s) originais | Decisão | Justificativa |
|---|---|---|
| Aluno: download de livros | Adaptar e agrupar em US-01 | Página de detalhes oferece links de acesso à versão digital quando disponíveis; download direto depende do formato externo. |
| Aluno: pesquisar livros pelo nome | Adaptar e agrupar em US-01 | Busca por parâmetro search disponível no backend; interface do catálogo ainda demonstrativa na main consultada. |
| Professor/funcionário: pesquisar livros pelo nome | Unificar em US-01 | Busca pública; não depende de papéis específicos. |
| Aluno/funcionário: acessar notícias | Adaptar e agrupar em US-02 | Leitura pública pelo backend, mas página inicial ainda demonstra dados fictícios. |
| Funcionário: adicionar/remover notícias | Transformar em US-03 (administrador) | CRUD de notícias protegido por token de administrador. |
| Aluno: tirar uma dúvida | Aplicável, fora da amostra | FAQ com perguntas expansíveis implementada no frontend; mantida fora dos testes selecionados para simplificar. |
| Aluno: pesquisar livros por filtros | Pendente, fora da amostra | Lista de temas na interface sem comportamento de filtragem confirmado. |
| Professor: separar publicações por temas | Fora da amostra / não confirmado | Não foi identificada regra correspondente de gerenciamento de livros. |
| Professor/funcionário: criar conta | Descontinuar na versão atual | O sistema atual tem autenticação administrativa, não contas públicas desses perfis. |
| Professor: cadastrar livros; funcionário: adicionar/remover/publicar livros | Não selecionar | Na main consultada, a API de livros é de leitura e busca; não há CRUD próprio de livros confirmado. |
| Professor: ver solicitações dos alunos; funcionário: avaliar cadastro de professores | Descontinuar na versão atual | Papéis e fluxos de solicitação não correspondem ao sistema atual. |

## 2. Histórias selecionadas (até 6 permitidas; foram escolhidas 3)

### US-01 — Pesquisar e acessar livros digitais

Como visitante da plataforma, quero pesquisar livros e consultar os detalhes de uma obra para encontrar leituras e acessar sua versão digital quando o catálogo disponibilizar um link.

**Estado verificado:** Busca e consulta por API já existentes; a interface visual do catálogo ainda tinha dados demonstrativos na main consultada.

**Código de referência:** `backend/app/api/routes/books.py`; `backend/app/schemas/books.py`; `frontend/src/pages/public/LivroDetalhes/LivroDetalhes.jsx`.

### US-02 — Consultar notícias e destaques

Como visitante, quero consultar notícias publicadas e os destaques para acompanhar as novidades da plataforma.

**Estado verificado:** Leitura pública implementada no backend; a página inicial ainda exibia notícias de exemplo na main consultada.

**Código de referência:** `backend/app/api/routes/news.py`.

### US-03 — Administrar notícias

Como administrador, quero cadastrar, editar, publicar, despublicar e excluir notícias para manter a comunicação da plataforma atualizada.

**Estado verificado:** CRUD e proteção por autenticação administrativa no backend; não pressupõe tela administrativa completa.

**Código de referência:** `backend/app/api/routes/news.py`; `backend/app/schemas/news.py`; `backend/app/api/dependencies.py`.

## 3. Critérios de aceitação

| US | Critério | Comportamento esperado |
|---|---|---|
| US-01 | CA-01.1 | A consulta de livros aceita busca textual e devolve a lista normalizada com count, next, previous e results. |
| US-01 | CA-01.2 | A paginação aceita valores de página a partir de 1 e rejeita valores menores. |
| US-01 | CA-01.3 | O detalhe de um livro exige ID positivo; retorna dados quando encontrado, 404 quando ausente e 422 para ID fora da faixa. |
| US-01 | CA-01.4 | Links digitais e de página oficial são disponibilizados quando retornados pelo catálogo externo; indisponibilidade do serviço é informada por erro apropriado. |
| US-02 | CA-02.1 | A listagem pública retorna somente notícias publicadas. |
| US-02 | CA-02.2 | O detalhe público de notícia não revela notícia não publicada ou inexistente. |
| US-02 | CA-02.3 | Destaques contêm somente notícias publicadas marcadas como destaque, na ordem configurada. |
| US-02 | CA-02.4 | A paginação aceita offset a partir de 0 e limit entre 1 e 100; valores fora dessas faixas são rejeitados. |
| US-03 | CA-03.1 | Operações administrativas exigem token válido de administrador. |
| US-03 | CA-03.2 | Cadastro valida título de 1 a 255 caracteres, conteúdo não vazio e ordem não negativa; a notícia começa não publicada por padrão. |
| US-03 | CA-03.3 | Alterações de publicação controlam a visibilidade pública e rejeitam campo explicitamente nulo. |
| US-03 | CA-03.4 | Exclusão autenticada remove notícia existente com HTTP 204 e informa 404 para ID inexistente. |

## 4. Matriz de rastreabilidade — projeto inicial

**Legenda:** “—” = não avaliado. Após a geração e execução, preencher v1/v2 com **Sim**, **Não** ou **Parcial**, sempre respaldado no código de teste. Os CTs abaixo são *propostas de teste*, não testes já executados.

### US-01

| Caso | Critério | Variável | Partição / limite | Entrada / cenário | Resultado esperado (oráculo) | v1 | v2 |
|---|---|---|---|---|---|:---:|:---:|
| CT-01-01 | CA-01.1 | search | texto informado | GET /books?search=historia, com Gutendex simulado | 200; parametro repassado; lista com count, next, previous e results | — | — |
| CT-01-02 | CA-01.1 | search | ausente | GET /books, com Gutendex simulado | 200; listagem sem filtro de busca | — | — |
| CT-01-03 | CA-01.2 | page | limite válido: 1 | GET /books?page=1 | 200; pagina 1 aceita | — | — |
| CT-01-04 | CA-01.2 | page | fora do limite: 0 | GET /books?page=0 | 422; valor rejeitado | — | — |
| CT-01-05 | CA-01.3 | book_id | válido: inteiro positivo | GET /books/1; simular livro existente | 200; dados de id, titulo, autores e links opcionais | — | — |
| CT-01-06 | CA-01.3 | book_id | limite inválido: 0 | GET /books/0 | 422; ID rejeitado | — | — |
| CT-01-07 | CA-01.3 | book_id | positivo inexistente | GET /books/999999; simular não encontrado | 404; livro não encontrado | — | — |
| CT-01-08 | CA-01.4 | link_download | link presente | GET /books/1; mock com link_download | 200; JSON preserva o link de acesso digital | — | — |
| CT-01-09 | CA-01.4 | Gutendex | indisponível | GET /books/1; simular indisponibilidade externa | 503; falha de serviço externo | — | — |

### US-02

| Caso | Critério | Variável | Partição / limite | Entrada / cenário | Resultado esperado (oráculo) | v1 | v2 |
|---|---|---|---|---|---|:---:|:---:|
| CT-02-01 | CA-02.1 | publicada | true e false | GET /news com uma publicada e outra rascunho | 200; apenas a publicada na lista | — | — |
| CT-02-02 | CA-02.2 | news_id | publicada existente | GET /news/{id_publicada} | 200; dados da notícia | — | — |
| CT-02-03 | CA-02.2 | news_id | não publicada | GET /news/{id_rascunho} | 404; sem exposição do rascunho | — | — |
| CT-02-04 | CA-02.3 | publicada; destaque; ordem | combinações de flags | GET /news/highlights com notícias de teste | 200; apenas publicada=true e destaque=true; ordem crescente | — | — |
| CT-02-05 | CA-02.4 | offset | limite inválido: -1 | GET /news?offset=-1 | 422; offset rejeitado | — | — |
| CT-02-06 | CA-02.4 | offset | limite válido: 0 | GET /news?offset=0 | 200; offset aceito | — | — |
| CT-02-07 | CA-02.4 | limit | limite inválido: 0 | GET /news?limit=0 | 422; limit rejeitado | — | — |
| CT-02-08 | CA-02.4 | limit | limites válidos: 1 e 100 | GET /news?limit=1 e GET /news?limit=100 | 200 em ambos; no máximo o limite solicitado | — | — |
| CT-02-09 | CA-02.4 | limit | limite inválido: 101 | GET /news?limit=101 | 422; limit rejeitado | — | — |

### US-03

| Caso | Critério | Variável | Partição / limite | Entrada / cenário | Resultado esperado (oráculo) | v1 | v2 |
|---|---|---|---|---|---|:---:|:---:|
| CT-03-01 | CA-03.1 | Authorization | ausente | POST /news com JSON válido e sem token | 401; autenticação necessária | — | — |
| CT-03-02 | CA-03.1 | Authorization | válido | POST /news com token de admin de teste | 201; ação autorizada | — | — |
| CT-03-03 | CA-03.2 | titulo | limite inválido: 0 caractere | POST /news com titulo="" | 422; título rejeitado | — | — |
| CT-03-04 | CA-03.2 | titulo | limites válidos: 1 e 255 | POST /news, titulo com 1 e 255 caracteres | 201 nos dois casos | — | — |
| CT-03-05 | CA-03.2 | titulo | limite inválido: 256 | POST /news, titulo com 256 caracteres | 422; título rejeitado | — | — |
| CT-03-06 | CA-03.2 | conteudo | vazio | POST /news com conteudo="" | 422; conteúdo rejeitado | — | — |
| CT-03-07 | CA-03.2 | ordem; publicada | ordem=-1 e ordem=0 | POST /news ordem=-1 e POST /news ordem=0 | 422 para -1; 201 para 0; publicada=false por padrão | — | — |
| CT-03-08 | CA-03.3 | publicada | mudança false para true | PATCH /news/{id} com publicada=true | 200; GET /news/{id} passa a retornar 200 | — | — |
| CT-03-09 | CA-03.3 | publicada | mudança true para false | PATCH /news/{id} com publicada=false | 200; GET /news/{id} passa a retornar 404 | — | — |
| CT-03-10 | CA-03.3 | titulo | nulo explícito | PATCH /news/{id} com titulo=null | 422; campo nulo rejeitado | — | — |
| CT-03-11 | CA-03.4 | news_id | existente | DELETE /news/{id_existente} com admin válido | 204; noticia removida | — | — |
| CT-03-12 | CA-03.4 | news_id | inexistente | DELETE /news/{id_inexistente} com admin válido | 404; notícia não encontrada | — | — |

## 5. Preparação, medições e registros pendentes

A matriz acima é um **plano de casos**, não uma suíte executada. Ao rodar cada versão, registrar: testes gerados/passando/falhando/não compilados; cobertura de linhas e de branches; cobertura de critérios, partições e limites; testes com asserções fracas; defeitos reais encontrados. **Não preencher métricas antecipadamente.**

| Indicador | v1 (LLM) | v2 (melhorada) |
|---|:---:|:---:|
| Testes gerados / passando / falhando / não compilam | — | — |
| Cobertura de linhas (%) | — | — |
| Cobertura de branches (%) | — | — |
| Cobertura de critérios (%) | — | — |
| Partições cobertas (%) | — | — |
| Valores-limite cobertos (%) | — | — |
| Testes sem asserção / trivial | — | — |
| Defeitos reais encontrados | — | — |

**Sequência exigida:** revisar a matriz com a equipe → fazer commit de `docs/testes/matriz-rastreabilidade.md` → pedir à LLM a v1 *sem mostrar a matriz* (usar somente critérios/user stories e módulos) → preservar v1 → executar e medir → melhorar v2 → relatório crítico em PDF → análise de dívida técnica e três refatorações com testes v2.

**Arquivos que não são possíveis nesta fase:** `tests/v1-llm/`, `tests/v2/`, `docs/testes/llm-log.md`, relatórios de cobertura, relatório crítico e relatório de refatoração exigem execução/documentação de etapas posteriores; nenhum resultado foi inventado.

## 6. Referências, restrições e revisão

- **Base utilizada:** Histórias de usuário originais fornecidas pela equipe e leitura do código da branch main em 15/11/2026. Não houve consulta ao planejamento completo da Sprint 2 nem à branch local integracao-funcional ainda em desenvolvimento.
- **Status do documento:** Rascunho de planejamento elaborado com apoio de IA. A equipe deve validar manualmente os critérios, partições, limites e oráculos antes do commit. Não declarar autoria exclusivamente humana se isso não aconteceu.
- **Escopo da matriz:** APIs implementadas para pesquisa/detalhe de livros, leitura de notícias e administração de notícias. Não representa validação de funcionalidades ainda visuais ou não integradas.
- **Ambiente de teste sugerido:** FastAPI TestClient, banco SQLite temporário para notícias, dependências de autenticação configuradas com usuário fictício, mocks para Gutendex. Não usar banco real nem Docker.
- **Colunas v1/v2:** Devem permanecer como — até os testes serem realmente gerados e executados. Não completar por suposição.
- **Oráculos:** Os resultados esperados foram derivados do contrato do código e precisam ser conferidos contra os requisitos oficiais antes da medição; não usar o código como única fonte da especificação.
- **Ordem obrigatória:** Revisar e registrar matriz primeiro → commit da matriz → geração v1 sem mostrar matriz à LLM → executar/medir v1 → construir/medir v2 → análise crítica → refatoração baseada na v2.

**Pontos que exigem conferência da equipe:** requisitos oficiais da Sprint 2; se todas as histórias selecionadas pertenciam à Sprint 2; comportamento final dos fluxos em desenvolvimento; versões de branches após novos merges; números efetivamente medidos.


## Proveniência do planejamento

Planejamento fornecido, revisado e aprovado pela responsável antes da geração da suíte v1. O planejamento teve apoio de IA. Os casos planejados não serão consultados durante a geração independente da v1; a comparação será realizada somente após preservá-la.
