# Divida tecnica - Sprint 3

Escopo: modulos das tres historias selecionadas; leitura dirigida assistida por IA e analise AST local (evidencias-ast.json). A equipe ainda deve fazer sua revisao humana independente. Nao foi realizada auditoria geral do sistema.

| ID | Local | Problema / categoria | Consequencia concreta | Descoberta | Status |
|---|---|---|---|---|---|
| DT-01 | backend/app/services/gutendex.py:35 normalize_book | Validacao de formatos misturada a normalizacao; SRP/coesao | 29 linhas e cinco decisoes AST misturam duas regras que mudam separadamente | Leitura + AST + LLM | Aberto |
| DT-02 | gutendex.py _get_json/fetch_books/fetch_book_by_id | Mensagem identica repetida 3 vezes; Duplicated Code/integridade conceitual | Alteracao de texto pode divergir entre lista, detalhe e JSON invalido | Contagem de literais + leitura + LLM | Aberto |
| DT-03 | api/routes/news.py list_news/list_admin_news | Politica 100 repetida em defaults e validacao; Magic Literal | Limites publico e administrativo podem divergir numa manutencao | Leitura + ocorrencias Query + LLM | Aberto |
| DT-04 | gutendex.py:88 _get_json | Cliente HTTP concreto criado dentro da operacao; acoplamento/DIP | Testes precisam substituir globalmente AsyncClient; mudar transporte exige editar servico | Leitura dos testes e imports AST + LLM | Aberto |
| DT-05 | api/routes/news.py:78 upload_image | HTTP, arquivo e transacao no mesmo procedimento; SRP | Alterar persistencia exige revisar fechamento de arquivo e rollback juntos | Leitura dirigida + LLM | Aberto |
| DT-06 | api/routes/news.py create_news/update_news | Sequencia commit/refresh repetida; duplicacao/coesao | Politica de persistencia deve ser mantida em dois manipuladores HTTP | Leitura + AST + LLM | Aberto |
| DT-07 | schemas/news.py NewsCreate/NewsUpdate | Restricoes titulo/conteudo/ordem repetidas; duplicacao | Alterar restricao em apenas um schema deixa cadastro e edicao inconsistentes | Leitura + LLM | Aberto |
| DT-08 | frontend/src/pages/admin/PainelNoticias/PainelNoticias.jsx | Estado de formulario, lista, paginacao e upload no mesmo componente; SRP/Long Component | Mudancas de formulario e consulta interferem no mesmo modulo e dificultam testes isolados | Leitura dirigida + LLM; nao medido por AST Python | Aberto |

## Escolhas
DT-01: extrair validacao ja exercitada por None/dicionario/formatos invalidos na v2, reduzindo responsabilidades sem mudar contrato.
DT-02: unificar mensagem ja afirmada nos testes v2, eliminando divergencia de manutencao.
DT-03: dar nome a politica repetida. A v2 adicionou ANTES os limites publico e administrativo 0/1/100/101, inclusive cardinalidade, para cobrir a segunda rota.

## Falsos positivos descartados
- Codigos HTTP 404/422 nao sao automaticamente Magic Numbers: sao vocabulario padronizado e legivel.
- NewsUpdate nao viola LSP: nao ha relacao de heranca entre ele e NewsCreate. Duplicacao de restricoes e risco real, herdar indiscriminadamente seria erro.
- PATCH vazio nao e defeito confirmado: contrato permite ausencia de alteracoes.
- Titulo com espacos nao e defeito confirmado: requisito diz comprimento, nao exige trim.
- Falhas de infraestrutura externa nao foram tratadas como code smell ou defeito funcional desta atividade.
