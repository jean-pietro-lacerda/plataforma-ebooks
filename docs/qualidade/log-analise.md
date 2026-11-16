# Log de analise - Sprint 3
Data inicial: 2026-11-15, America/Sao_Paulo. Execucao local, sem fetch/push/branch nova.

Ferramenta: tests/analise_qualidade.py, biblioteca ast do Python; conta linhas, decisoes sintaticas, imports e ocorrencias de mensagem. Nao e Sonar/ESLint e a contagem de decisoes nao e complexidade cognitiva certificada. Resultado integral: evidencias-ast.json.

LLM: OpenAI Codex baseado em GPT-6, snapshot nao exposto. Leitura dirigida tambem feita pelo assistente; nao se alega inspecao humana independente.

Prompts completos, um modulo por vez:
1. Para backend/app/services/gutendex.py: "Leia este modulo e aponte propriedades de projeto, SOLID e smells reais com funcao/trecho. Confronte com numero de linhas, decisoes AST e repeticao de mensagens. Nao chame convencoes de defeitos."
Resposta: normalize_book mistura validacao/normalizacao (DT-01); mensagem repetida tres vezes (DT-02); cliente HTTP concreto em _get_json acopla transporte (DT-04).
2. Para backend/app/api/routes/news.py: "Identifique duplicacoes e responsabilidades nos manipuladores HTTP, indicando a funcao. Separe codigo de protocolo de politica de negocio."
Resposta: politica 100 repetida (DT-03), upload coordena HTTP/arquivo/transacao (DT-05), commit/refresh repetidos (DT-06). Codigos HTTP nao foram aceitos como divida automaticamente.
3. Para backend/app/schemas/news.py: "Compare responsabilidades e restricoes; nao invente heranca nem violacao LSP."
Resposta: restricoes repetidas podem divergir (DT-07); proposta de violacao LSP descartada.
4. Para frontend/src/pages/admin/PainelNoticias/PainelNoticias.jsx: "Identifique responsabilidades efetivamente presentes, sem propor funcionalidades ou reescrever o componente."
Resposta: formulario, consulta, pagina e upload compartilham estado/modulo (DT-08). Inspecao textual, sem alegar medicao Python sobre JSX.

Confirmacao: trechos lidos diretamente e contrastados com evidencias AST. A ferramenta mede sinais locais; leitura e LLM relacionam consequencias e contratos. Oito itens registrados; apenas DT-01/02/03 selecionados. Demais permanecem abertos. Nao foi encontrada violacao LSP/ISP que pudesse ser afirmada honestamente.

Teste anterior: v2 e executada explicitamente como fase 'antes', sem testes antigos de integracao funcional. Testes depois: fases DT-01, DT-02 e DT-03, sempre os mesmos 78 casos. Novos testes de caracterizacao ja estavam na v2 antes de refatorar; nenhum trecho selecionado fica sem protecao relevante.
