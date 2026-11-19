# Contexto enviado para a geracao v1

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


Modulos: backend/app/api/routes/books.py; backend/app/api/routes/news.py; backend/app/api/dependencies.py; backend/app/schemas/books.py; backend/app/schemas/news.py; backend/app/services/gutendex.py.
