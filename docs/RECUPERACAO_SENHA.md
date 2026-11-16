# Recuperação de senha — proposta pendente

Status: implementação adiada por decisão da responsável nesta etapa. Não foram alterados models, contratos de autenticação, migrações ou endpoints de redefinição.

## O que falta definir

1. Como um endereço de email será cadastrado por um operador confiável e vinculado a cada administrador, sem inferi-lo do nome de usuário.
2. Como a posse desse email será verificada antes de permitir seu uso na recuperação.
3. Provedor de envio/SMTP, remetente, domínio autorizado e URL HTTPS do frontend.
4. Aprovação das migrações e política de expiração, limites de solicitações e revogação de sessões.

O modelo Admin atual contém apenas id, usuario e senha_hash. As páginas de recuperação informam indisponibilidade e não coletam nem enviam credenciais enquanto esse fluxo não existe.

## Proposta para aprovação posterior

- Manter usuario como identificador de login; acrescentar email único e estado/data de verificação mediante migração aprovada. Endereços não verificados não poderão recuperar uma conta.
- Persistir somente o hash de tokens de recuperação aleatórios, criptograficamente fortes, com pelo menos 256 bits de entropia. Cada registro deve estar vinculado ao administrador e ter expiração e marca de consumo.
- Configurar o envio real por serviço substituível; usar mock desse serviço apenas nos testes. Definir mecanismo confiável de entrega e repetição sem expor existência de contas.
- Retornar mensagem genérica tanto para contas existentes quanto inexistentes, com comportamento temporal consistente; limitar solicitações por origem e por conta segundo política aprovada.
- Usar URL base HTTPS previamente configurada, sem confiar no Host enviado pelo solicitante. Evitar vazamento de tokens por logs, histórico ou Referer; a forma de transporte precisa ser definida com as proteções correspondentes.
- Validar token, expiração e uso antes de permitir a troca. Confirmar a senha e aplicar política compatível com a criação administrativa já existente, após aprovação.
- Atualizar o hash Argon2 e consumir o token atomicamente na mesma transação, prevenindo reutilização concorrente. Invalidar outras solicitações pendentes conforme política definida.
- Não efetuar login automático após a troca. Notificar a alteração por email, sem incluir senha ou token.
- Definir a invalidação de sessões existentes: o JWT atual não contém versão de sessão nem há lista de revogação. Essa parte exige decisão explícita sobre modelo/claims ou armazenamento adicional.
- Testar solicitação genérica, conta não verificada, limites de uso, token inválido/expirado/reutilizado, concorrência, falha de envio e rollback sem usar contas ou banco de produção.

Não há mecanismo alternativo que redefina senha apenas com usuario ou email informado.

Referência: [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).
