# Plataforma eBooks

Frontend React/Vite e backend FastAPI para consulta de livros do Project Gutenberg/Gutendex e publicação de notícias por administradores.

## Estado funcional

| Funcionalidade | Implementação |
| --- | --- |
| Catálogo | Consulta real de /books, busca por título/autor, filtro por assunto e paginação |
| Detalhes dos livros | Consulta de /books/{id}, autores, links oficiais e tratamento de falhas |
| FAQ | Perguntas expansíveis por clique e teclado |
| Login | Usuário e senha enviados a /auth/login; identidade confirmada por /auth/me |
| Área administrativa | Perfil e gerenciamento de notícias protegidos por autenticação |
| Notícias | Lista pública, leitura, criação, edição, exclusão confirmada, publicação, destaques, ordenação e imagens |
| Página inicial | Destaques publicados da API, com acesso ao conteúdo completo |
| Recuperação de senha | Pendente de requisitos e infraestrutura; ações explicitamente indisponíveis |
| Publicação de e-books próprios | Não implementada; o backend de livros consulta um catálogo externo |

Não há cadastro público de usuários ou endpoint de edição de livros. Os arquivos vazios PainelLivros e CarrosselNoticias são remanescentes da estrutura inicial e não representam funcionalidades disponíveis.

## Arquitetura e contratos

- Frontend: frontend/src/App.jsx registra rotas públicas e a área /admin.
- frontend/src/services/api.js centraliza URL, JSON, multipart e erros de conexão.
- frontend/src/auth mantém o estado administrativo; a autorização efetiva continua no backend.
- Backend: /books e /books/{id} consultam Gutendex.
- /auth/login recebe usuario e senha; /auth/me exige Authorization: Bearer.
- /news e /news/{id} expõem somente notícias publicadas.
- /news/highlights retorna destaques publicados ordenados.
- /news/admin e operações POST/PATCH/DELETE exigem administrador.
- /news/{id}/image recebe ou entrega imagens conforme o contrato B3.

Os rótulos de temas do catálogo são apresentados em português e usam expressões de assunto em inglês no parâmetro topic do Gutendex. O frontend mantém busca, tema e página na URL; não segue URLs externas de paginação fornecidas pelo serviço.

## Autenticação

O identificador atual é usuario, conforme o modelo Admin, os schemas e o script de criação inicial. Não há requisito documentado nem modelo de email para alterar esse contrato.

O token Bearer fica somente na memória da aba, sem localStorage, sessionStorage ou cookies de autenticação. Recarregar ou fechar a página exige novo login. A expiração exibida pelo cliente não substitui a validação de assinatura, expiração e existência do administrador no servidor.

Sair descarta a sessão da aba. O backend atual não tem revogação global de JWT ou refresh token; um JWT emitido mantém sua validade no servidor até expirar. Alterar esse modelo exige decisão de segurança e, possivelmente, migração.

## Configuração

Nenhuma credencial real faz parte do repositório. .env.example contém apenas placeholders. Nunca inclua senhas ou tokens nas variáveis VITE_, que são públicas no bundle.

Backend:

- DATABASE_URL: conexão da aplicação ao PostgreSQL.
- MIGRATIONS_DATABASE_URL: conexão administrativa usada somente para migrações.
- JWT_SECRET_KEY: chave secreta forte do ambiente.
- ACCESS_TOKEN_EXPIRE_MINUTES: validade do acesso, padrão de 30 minutos.
- NEWS_UPLOAD_DIR: diretório gravável para imagens; configure um caminho absoluto no ambiente de execução. O padrão /workspace/storage/uploads pertence ao ambiente original do projeto e deve ser ajustado em uma execução local sem esse diretório.
- As configurações podem ser recebidas por variáveis de ambiente ou pelo arquivo .env já suportado pelo backend.

Frontend:

- frontend/.env.example exemplifica VITE_API_URL.
- Sem configuração, a API é http://localhost:8000.
- As origens locais permitidas pelo backend são http://localhost:5173 e http://127.0.0.1:5173. A publicação em outro domínio precisa de configuração de CORS correspondente.
- Em produção, frontend e API precisam usar HTTPS.

O script backend/create_initial_admin.py cria o primeiro administrador no banco configurado. Ele não é executado pelos testes e não contém uma conta padrão de produção.

Cloudinary aparece no template original, mas o upload B3 implementado usa armazenamento local configurável, não esse serviço. SMTP e recuperação por email ainda não foram definidos.

## Testes

A etapa funcional foi validada com Node.js 24.22.3, npm 11.19.1, Python 3.14.7 e Chrome instalado no Windows, usando cópias e dependências no TEMP, sem instalações globais ou banco de produção.

- npm ci, npm run build e npm run lint no frontend.
- python -m pytest no backend, com fixtures SQLite em memória e mocks do Gutendex.
- Testes adicionais de autenticação e B3 estão em backend/tests.
- Os testes de navegador desta etapa usam um lançador temporário com Chrome DevTools; não foi adicionado framework de testes de frontend nem dependência de navegador ao projeto.
- O serviço HTTP de teste usa as rotas reais, contas fictícias e SQLite em memória. A emissão de JWT de curta duração é configurada apenas no lançador temporário para exercitar expiração; não existe bypass de autenticação no código da aplicação.

As limitações e decisões de recuperação estão em docs/RECUPERACAO_SENHA.md. A validação local não comprova migrações, permissões ou disponibilidade do banco de produção.
