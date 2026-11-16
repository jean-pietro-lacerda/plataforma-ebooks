# Comparacao v1 x v2

| Indicador | v1 | v2 |
|---|---|---|
| Testes gerados/passam/falham/nao compilam | 25/25/0/0 | 78/78/0/0 |
| Linhas | 79.46% (178/224) | 91.07% (204/224) |
| Branches | 54.55% (24/44) | 88.64% (39/44) |
| Criterios com ao menos um teste | 100% (12/12) | 100% (12/12) |
| Particoes exercitadas | 91,67% (33/36) | 100% (36/36) |
| Limites explicitamente enviados | 81,25% (13/16) | 100% (16/16) |
| Sem assert / assert trivial | 0/0 | 0/0 |
| Defeitos reais confirmados | 0 | 0 |
| CTs completos/parciais/ausentes | 24/5/1 | 30/0/0 |
| Funcoes apenas com oraculo HTTP | 8 | 12 |

## Regra de contagem
36 classes separando variaveis/estados do plano: US-01=9, US-02=13, US-03=14. Limites=16: page 0/1; ID 0/1; offset -1/0; limit 0/1/100/101; titulo 0/1/255/256; ordem -1/0. Default de ordem nao conta como zero explicitamente enviado. Particoes medem exercicio; requisitos seguem ao menos um teste por CA, nao exaustividade. Contagem dos CTs exige oraculo completo, por isso difere da cobertura de criterios.

v1: faltavam flags false/false e true/false nos destaques e limit<1 (3 classes); limites 0 e 100 de limit e ordem=0 explicita. CT-01-02, CT-02-02, CT-02-04, CT-02-08 e CT-03-07 parciais; CT-02-07 ausente. Demais 24 CTs verificados por representantes equivalentes. v2 cobre os 30 CTs, 36 classes e 16 limites. As particoes adicionais de JSON/transporte/token caracterizam riscos existentes, nao criam requisitos.

Status HTTP e oraculo significativo, nao assert trivial. Um oraculo v1 deriva de detalhe implementado (URL oficial exata em test_digital_links), nao literalmente do CA. Nao ha defeito real confirmado nem teste comprovadamente validando defeito. A revisao humana independente nao foi realizada pelo assistente.

