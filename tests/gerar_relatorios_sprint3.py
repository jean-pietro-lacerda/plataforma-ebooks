import ast,hashlib,json,pathlib,re
from html import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
D=pathlib.Path("docs/testes")
v1=json.loads((D/"relatorios/v1/metricas.json").read_text());v2=json.loads((D/"relatorios/v2/metricas.json").read_text())
def quality(folder):
 fs=[f for p in pathlib.Path(folder).glob("test*.py") for f in ast.walk(ast.parse(p.read_text(encoding="utf-8-sig"))) if isinstance(f,ast.FunctionDef) and f.name.startswith("test")]
 return {"functions":len(fs),"without_assert":sum(not any(isinstance(a,ast.Assert) for a in ast.walk(f)) for f in fs),"trivial":sum(any(isinstance(a,ast.Assert) and isinstance(a.test,ast.Constant) and a.test.value is True for a in ast.walk(f)) for f in fs),"status_only":sum(all("status_code" in ast.unparse(a.test) for a in ast.walk(f) if isinstance(a,ast.Assert)) for f in fs)}
q1,q2=quality("tests/v1-llm"),quality("tests/v2")
rows=[
["Testes gerados/passam/falham/nao compilam","25/25/0/0","78/78/0/0"],
["Linhas",f"{v1['line_percent']}% (178/224)",f"{v2['line_percent']}% (204/224)"],
["Branches",f"{v1['branch_percent']}% (24/44)",f"{v2['branch_percent']}% (39/44)"],
["Criterios com ao menos um teste","100% (12/12)","100% (12/12)"],
["Particoes exercitadas","91,67% (33/36)","100% (36/36)"],
["Limites explicitamente enviados","81,25% (13/16)","100% (16/16)"],
["Sem assert / assert trivial",f"{q1['without_assert']}/{q1['trivial']}",f"{q2['without_assert']}/{q2['trivial']}"],
["Defeitos reais confirmados","0","0"],
["CTs completos/parciais/ausentes","24/5/1","30/0/0"],
["Funcoes apenas com oraculo HTTP",str(q1["status_only"]),str(q2["status_only"])],
]
metrics={"v1":v1,"v2":v2,"assertions_v1":q1,"assertions_v2":q2,"criteria":[12,12,12],"partitions":[33,36,36],"limits":[13,16,16],"real_defects":[0,0]}
(D/"comparacao.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
md="# Comparacao v1 x v2\n\n| Indicador | v1 | v2 |\n|---|---|---|\n"+"\n".join("| "+" | ".join(r)+" |" for r in rows)
md+="\n\n## Regra de contagem\n36 classes separando variaveis/estados do plano: US-01=9, US-02=13, US-03=14. Limites=16: page 0/1; ID 0/1; offset -1/0; limit 0/1/100/101; titulo 0/1/255/256; ordem -1/0. Default de ordem nao conta como zero explicitamente enviado. Particoes medem exercicio; requisitos seguem ao menos um teste por CA, nao exaustividade. Contagem dos CTs exige oraculo completo, por isso difere da cobertura de criterios.\n\nv1: faltavam flags false/false e true/false nos destaques e limit<1 (3 classes); limites 0 e 100 de limit e ordem=0 explicita. CT-01-02, CT-02-02, CT-02-04, CT-02-08 e CT-03-07 parciais; CT-02-07 ausente. Demais 24 CTs verificados por representantes equivalentes. v2 cobre os 30 CTs, 36 classes e 16 limites. As particoes adicionais de JSON/transporte/token caracterizam riscos existentes, nao criam requisitos.\n\nStatus HTTP e oraculo significativo, nao assert trivial. Um oraculo v1 deriva de detalhe implementado (URL oficial exata em test_digital_links), nao literalmente do CA. Nao ha defeito real confirmado nem teste comprovadamente validando defeito. A revisao humana independente nao foi realizada pelo assistente.\n"
(D/"comparacao-v1-v2.md").write_text(md+"\n",encoding="utf-8")
p=D/"matriz-rastreabilidade.md";lines=p.read_text(encoding="utf-8-sig").splitlines();out=[]
partial={"CT-01-02","CT-02-02","CT-02-04","CT-02-08","CT-03-07"}
for line in lines:
 if re.match(r"\| CT-\d\d-\d\d ",line):
  parts=line.split("|");identifier=parts[1].strip();parts[-3]=" Nao " if identifier=="CT-02-07" else " Parcial " if identifier in partial else " Sim ";parts[-2]=" Sim ";line="|".join(parts)
 out.append(line)
p.write_text("\n".join(out)+"\n\n## Resultados executados (substituem o estado pendente do plano inicial)\n\n"+md+"\n\nMatriz original no commit 8b72f31, v1 congelada em a7f259a. Resultados: relatorios/v1/index.html e relatorios/v2/index.html.\n",encoding="utf-8")
with (D/"llm-log.md").open("a",encoding="utf-8") as f:
 f.write("\n## Resultado rodada 1\n25/25 passaram; zero falhas ou erros de coleta. Nenhum ajuste de executabilidade: 1/3 rodadas. A matriz completa foi consultada somente apos preservar a v1 no Git.\n\n## Rodada 2 - v2\nPrompt integral:\n> Feche as lacunas da matriz: limit 0/100, ordem 0 explicita, combinacoes completas de flags, consulta sem busca e detalhe publicado com oraculos completos. Acrescente formatos, payloads invalidos, falhas de rede e tokens invalidos/expirados para melhorar branches. Preserve v1 e escopo dos seis modulos. Comente requisito/tecnica. Caracterize formatos, mensagens e paginacao publica/admin antes das refatoracoes.\nResposta integral: tests/v2/test_stories_v2.py. 78/78 passaram; nenhum ajuste posterior.\nSHA256 v1: "+hashlib.sha256(pathlib.Path("tests/v1-llm/test_stories.py").read_bytes()).hexdigest()+"\nModelo exato/snapshot nao exposto. Toda revisao desta execucao e assistida por IA; nao se declara revisao humana independente.\n")
cov=json.loads((D/"relatorios/v1/coverage.json").read_text());examples=[]
for file,data in cov["files"].items():
 for a,b in data.get("missing_branches",[]):
  if a in data["executed_lines"]:examples.append((file,a,b))
ex=next(x for x in examples if "gutendex" in x[0]);snippet=pathlib.Path(ex[0]).read_text(encoding="utf-8-sig").splitlines()[ex[1]-1].strip()
styles=getSampleStyleSheet();styles["BodyText"].fontSize=9;styles["BodyText"].leading=12
def pdf(path,pages):
 story=[]
 for title,paragraphs in pages:
  if story:story.append(PageBreak())
  story.append(Paragraph(escape(title),styles["Heading1"]));story.append(Spacer(1,10))
  for item in paragraphs:
   if isinstance(item,list):
    table=Table([[Paragraph(escape(str(c)),styles["BodyText"]) for c in row] for row in item],colWidths=[245,115,115],repeatRows=1)
    table.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.3,colors.grey),("BACKGROUND",(0,0),(-1,0),colors.lightgrey),("VALIGN",(0,0),(-1,-1),"TOP")]))
    story.append(table)
   else:story.append(Paragraph(escape(item),styles["BodyText"]))
   story.append(Spacer(1,9))
 SimpleDocTemplate(str(path),pagesize=A4,leftMargin=35,rightMargin=35,topMargin=30,bottomMargin=30).build(story)
pages=[
("Sprint 3 - Contexto e protocolo (1/4)",[
"US-01: pesquisar/acessar livros. US-02: consultar noticias/destaques. US-03: administrar noticias. Planejamento aprovado com apoio de IA; 12 criterios, 30 CTs, 36 classes e 16 limites numericos explicitos.",
"Matriz commitada em 8b72f31 antes da geracao; v1 preservada em a7f259a antes de ler os casos planejados. Uma rodada, nenhum ajuste manual na v1. O contexto incluiu requisitos, modulos e infraestrutura de testes preexistente; essa memoria limita independencia absoluta em relacao a testes antigos.",
"LLM: OpenAI Codex baseado em GPT-6, snapshot exato nao exposto. Data 15/11/2026, America/Sao_Paulo. Prompts em llm-log.md; resposta integral em resposta-v1.md e arquivos versionados.",
"Ferramentas: pytest, coverage.py branch=True, AST para assercoes e ReportLab. Mesmo escopo de seis modulos Python de livros, noticias, validacao e dependencias; nao inclui React, bibliotecas ou projeto inteiro. SQLite em memoria e HTTP simulado, sem servicos externos.",
"Requisitos usam a regra de ao menos um teste por criterio. Classes contam exercicio, CTs completos exigem oraculos completos e limites exigem envio explicito. Nao confundir 100% de criterios com exaustividade."]),
("Indicadores e evidencias (2/4)",[rows,
"Relatorios HTML: docs/testes/relatorios/v1/index.html e v2/index.html. JUnit XML, coverage.json, metricas.json, coverage.txt e execucao.log preservam as medicoes. Nao houve falha omitida; zero defeitos novos confirmados. A cobertura v2 foi medida antes de qualquer refatoracao."]),
("Respostas as quatro perguntas (3/4)",[
"1. Tecnicas funcionais: v1 acertou 33/36 classes e 13/16 limites. Perdeu duas combinacoes de flags e limit<1, alem de limit=0/100 e ordem=0 explicita. v2 fecha 36/36 e 16/16. Descobriu ainda formatos HTML alternativos, JSON invalido, timeout e tokens invalidos fora do plano inicial, mas dentro dos contratos existentes.",
"2. Requisitos: nenhum dos 12 criterios ficou sem teste, pela definicao de cobertura do enunciado. Apesar disso, v1 tinha 5 CTs parciais e 1 ausente; v2 tem 30/30 completos. Testes de caracterizacao adicionais protegem as refatoracoes, sem serem contados como novos requisitos.",
f"3. Linhas versus branches: v1 79,46% contra 54,55%; v2 91,07% contra 88,64%. Exemplo real: {ex[0]}:{ex[1]} '{snippet}', linha executada mas aresta para {ex[2]} nao percorrida na v1, conforme coverage.json. Executar o if nao cobre ambos os resultados; v2 inclui formatos alternativos/invalidos.",
f"4. Oraculos: {q1['status_only']} funcoes v1 tinham somente verificacao de status. A paginacao podia passar sem provar quantidade ou selecao; v2 verifica min(3,limit), IDs e encaminhamento. Zero sem assert/triviais em ambas. Uma escolha de implementacao virou oraculo v1 (URL oficial exata), sem estar literalmente no CA. Nao foi confirmado caso aprovando defeito real: zero defeitos encontrados."]),
("Melhoria e conclusao (4/4)",[
"v2 acrescenta 53 execucoes de teste e reforca estados, cardinalidade, dados, encaminhamento, ausencia de mutacao apos null e mensagens de erro. Ganho estrutural: 26 linhas e 15 arestas de branch, sem mudar producao.",
"Usariamos LLM para a primeira versao, acompanhada de requisitos, registro integral, suite imutavel e revisao de oraculos. Nunca aceitar percentuais altos como prova isolada: 100% dos criterios na v1 coexistia com somente 54,55% dos branches.",
"Limitacoes: identificador exato do modelo nao exposto; geracao e leitura dirigida pelo assistente, sem revisao humana independente. Frontend, PostgreSQL real e todos os fluxos de imagem nao foram medidos. O planejamento original tinha suporte de IA, declarado; a equipe deve validar a entrega.",
"Apendices externos: matriz-rastreabilidade.md, llm-log.md, resposta-v1.md, comparacao-v1-v2.md, comparacao.json e ambas as suites. Advertencia de deprecacao Starlette/httpx nao causou falhas."])
]
pdf(D/"relatorio-critico.pdf",pages)
print("PARTE1_COMPLETA_PDF_4_PAGINAS")
