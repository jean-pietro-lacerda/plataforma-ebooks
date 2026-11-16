# Validação da integração funcional

Base: main em 1a096b9, com o PR #9 incorporado por squash. O conteúdo inicial era idêntico a integracao-sprint3 em 36e23b5. A branch anterior foi preservada.

## Ambiente

- Node.js 24.22.3 portátil oficial, com SHA-256 conferido; npm 11.19.1.
- Python 3.14.7, com venv e dependências por wheels em pasta exclusiva no TEMP.
- Código testado em cópia separada, sem node_modules, venv ou arquivos de teste temporários no projeto original.
- Chrome já instalado, headless, com perfil temporário e serviços restritos a loopback.
- Banco SQLite em memória, contas fictícias, diretório de imagens temporário e Gutendex simulado para testes determinísticos.
- Nenhum acesso ao banco de produção, uso de Docker, instalação global ou alteração do PATH global.

## Resultados

| Verificação | Resultado |
| --- | --- |
| npm ci | Passou |
| npm run build, resultado final | Passou |
| npm run lint, resultado final | Passou, com dois avisos preexistentes |
| Pytest | 99 passaram, nenhuma falha |
| Navegador, conjunto final | 80 checagens passaram em oito grupos, nenhuma falha |
| JavaScript no navegador | Nenhuma exceção não tratada observada |
| Responsividade | Verificada a 1280, 390 e 320 px |
| Detalhe /books/84 com Gutendex real | Passou: HTTP 200 |
| Busca real por Frankenstein | Falhou por timeout externo: HTTP 503 tratado |
| Filtro real topic=biology | Falhou por timeout externo: HTTP 503 tratado |

O status do comando que fez as consultas ao vivo indica apenas que ele terminou; os resultados das duas consultas com timeout não foram classificados como aprovação.

## Cobertura

Os 47 testes de backend anteriores foram preservados. Foram acrescentados 11 cenários de autenticação e 41 da B3, agora presentes no repositório, totalizando 99. Os testes B3 que eram temporários na etapa anterior passaram a ter cobertura permanente nesta nova etapa.

Os oito grupos de navegador verificaram:

1. Campos obrigatórios, usuário em vez de email, credenciais inválidas, limpeza da senha após falha e erro de conexão.
2. Login real, confirmação do perfil, destino administrativo protegido, carregamento, ausência de token em storage/cookies, logout e exigência de novo login após reload.
3. Expiração automática e resposta 401 real do servidor, inclusive com relógio do cliente divergente. O JWT curto de teste existe somente no lançador temporário.
4. Catálogo real, pesquisa, tema, paginação, ausência de resultados, indisponibilidade, acesso ao detalhe e 404.
5. Destaques vazios, indisponíveis, nova tentativa, carrossel, lista pública de notícias sem destaque e proteção de rascunhos.
6. Criação administrativa, imagem, publicação, ordenação dos destaques, leitura pública, despublicação e exclusão com confirmação.
7. Rejeição local de arquivo inválido e repetição após falha parcial de upload sem duplicar a notícia. A falha parcial foi simulada na camada HTTP; a criação e o upload bem-sucedido chegaram ao backend real.
8. FAQ por clique e teclado, recuperação explicitamente indisponível e layout de páginas públicas e administrativas nos três tamanhos de tela.

Os textos de notícia com marcação HTML foram exibidos como texto, sem execução do script de teste. Essas verificações não equivalem a uma auditoria completa de segurança.

## Avisos e limitações

- Lint: react/purity em Footer.jsx e react/set-state-in-effect em LivroDetalhes.jsx, ambos anteriores a esta etapa.
- Pytest: avisos de depreciação de pytest-asyncio e Starlette/TestClient com httpx.
- PostgreSQL/Neon reais, migrações e permissões de produção não foram testados.
- A disponibilidade de busca e filtros do Gutendex não foi comprovada ao vivo: as duas consultas excederam o timeout existente. Os fluxos e o tratamento de indisponibilidade passaram com respostas controladas.
- Google Maps e recursos externos de imagem foram bloqueados nos testes de navegador; somente o Chrome instalado foi utilizado.
- Não há configuração real de banco, JWT ou SMTP neste ambiente. As contas e a chave do lançador são exclusivamente de teste.
- Recuperação por email, revogação global de JWT e publicação de livros próprios não foram implementadas. A recuperação foi adiada explicitamente; sua proposta está em RECUPERACAO_SENHA.md.
- Os testes de navegador foram executados com um lançador temporário, sem adicionar framework de frontend ao repositório.

Os contratos da API, models, migrações e dependências existentes foram preservados. O backend já fornecia os endpoints necessários; a integração funcional desta etapa foi realizada no frontend, acompanhada de testes de contrato e segurança.

Não houve push, novo Pull Request ou merge na main nesta etapa.
