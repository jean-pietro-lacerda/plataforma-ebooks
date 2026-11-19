# Log LLM — Sprint 3
Data: 2026-11-15 (America/Sao_Paulo).
Ferramenta: OpenAI Codex, modelo baseado em GPT-6 conforme identificação da sessão. Identificador exato de versão/snapshot não disponibilizado; não foi inventado.
Planejamento: fornecido e aprovado pela responsável, com apoio de IA. Não se declara planejamento humano independente. A matriz foi commitada antes da geração; somente histórias e critérios foram extraídos, sem leitura das linhas de casos planejados.

## Rodada 1 — geração v1 independente
Prompt integral:
> Gere uma suíte pytest executável para as histórias US-01 (pesquisar/acessar livros), US-02 (consultar notícias/destaques) e US-03 (administrar notícias), com os 12 critérios CA-01.1 a CA-03.4 fornecidos em docs/testes/requisitos-v1.md. Use os módulos FastAPI/SQLAlchemy listados nesse arquivo e o contrato efetivamente existente. Aplique partições de equivalência, valores-limite e cobertura de critérios. Cada teste deve identificar em comentário requisito e técnica. Use SQLite em memória, cliente FastAPI e MockTransport para Gutendex; não acesse serviços ou banco reais. Não consulte a matriz, seus casos planejados ou a análise posterior. Entregue código, sem inventar APIs e sem alterar produção.

Contexto fornecido: histórias/12 critérios em requisitos-v1.md; código de backend/app/api/routes/{books,news}.py, backend/app/schemas/{books,news}.py, backend/app/api/dependencies.py e backend/app/services/gutendex.py; pytest/FastAPI/SQLAlchemy disponíveis no projeto. Também foram lidos os testes backend preexistentes como contexto de infraestrutura; isso limita a independência absoluta em relação à suíte anterior, mas não houve consulta aos casos da matriz.

Resposta integral de código: tests/v1-llm/test_stories.py e tests/conftest.py (preservados no commit da geração). O arquivo resposta-v1.md reproduz os dois arquivos integralmente.
Ajustes na v1: nenhum. Uma rodada usada, limite máximo três. A infraestrutura de execução/cobertura não altera os testes.
Resultados e diagnóstico: preenchidos após execução; nenhuma alegação de cobertura feita antes de medir.

## Resultado rodada 1
25/25 passaram; zero falhas ou erros de coleta. Nenhum ajuste de executabilidade: 1/3 rodadas. A matriz completa foi consultada somente apos preservar a v1 no Git.

## Rodada 2 - v2
Prompt integral:
> Feche as lacunas da matriz: limit 0/100, ordem 0 explicita, combinacoes completas de flags, consulta sem busca e detalhe publicado com oraculos completos. Acrescente formatos, payloads invalidos, falhas de rede e tokens invalidos/expirados para melhorar branches. Preserve v1 e escopo dos seis modulos. Comente requisito/tecnica. Caracterize formatos, mensagens e paginacao publica/admin antes das refatoracoes.
Resposta integral: tests/v2/test_stories_v2.py. 78/78 passaram; nenhum ajuste posterior.
SHA256 v1: 280ea5e288370024c9eceb10f2ef9e91839ba581992c18549c16ad54238b29c5
Modelo exato/snapshot nao exposto. Toda revisao desta execucao e assistida por IA; nao se declara revisao humana independente.
