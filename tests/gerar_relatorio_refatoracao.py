import hashlib,json,pathlib,re,subprocess
from html import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
Q=pathlib.Path("docs/qualidade");D=pathlib.Path("docs/testes")
commits={}
for line in subprocess.check_output(["git","log","--format=%h %s","e6abd9a..HEAD"],text=True,encoding="utf-8").splitlines():
 for key in ("DT-01","DT-02","DT-03"):
  if line.split(" ",1)[1].startswith(key+":"):commits[key]=line.split(" ",1)[0]
runs={}
for phase in ("antes","DT-01","DT-02","DT-03"):
 runs[phase]=json.loads((D/"relatorios"/("refatoracao-"+phase)/"metricas.json").read_text())
 assert runs[phase]["passed"]==78 and runs[phase]["failed"]==runs[phase]["errors"]==0
p=Q/"divida-tecnica.md";text=p.read_text(encoding="utf-8")
for key in commits:
 lines=text.splitlines()
 text="\n".join(line.replace("| Aberto |",f"| Refatorado ({commits[key]}) |") if line.startswith("| "+key+" ") else line for line in lines)+"\n"
text+="\n## Evidencias dos testes e commits\n\n| Etapa | Passam/falham/erros | Linhas | Branches | Commit |\n|---|---|---|---|---|\n"
for phase,m in runs.items():
 text+=f"| {phase} | {m['passed']}/{m['failed']}/{m['errors']} | {m['line_percent']}% | {m['branch_percent']}% | {commits.get(phase,'baseline v2')} |\n"
text+="\nDT-01 usa Extract Function; DT-02 Extract Constant para mensagem duplicada; DT-03 Replace Magic Literal para politica compartilhada. Cinco itens permanecem abertos. Todos os oraculos HTTP e dados passaram antes/depois. Nenhum teste precisou ser enfraquecido. Evidencias completas em docs/testes/relatorios/refatoracao-*/.\n"
p.write_text(text,encoding="utf-8")
(Q/"resultados-refatoracoes.json").write_text(json.dumps({"commits":commits,"runs":runs},indent=2),encoding="utf-8")
with (Q/"log-analise.md").open("a",encoding="utf-8") as f:
 f.write("\n## Resultado final\nDT-01="+commits["DT-01"]+"; DT-02="+commits["DT-02"]+"; DT-03="+commits["DT-03"]+". V2: 78/78 antes e apos cada alteracao. Sem falhas, sem alteracao de oraculos, cinco dividas abertas. Aumento pequeno de linhas decorre de helpers/constantes, nao de novos requisitos.\n")
styles=getSampleStyleSheet();styles["BodyText"].fontSize=9;styles["BodyText"].leading=12
story=[]
def addpage(title,items):
 if story:story.append(PageBreak())
 story.append(Paragraph(escape(title),styles["Heading1"]));story.append(Spacer(1,12))
 for item in items:
  if isinstance(item,list):
   table=Table([[Paragraph(escape(str(c)),styles["BodyText"]) for c in row] for row in item],colWidths=[75,155,245])
   table.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.3,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,0),colors.lightgrey)]));story.append(table)
  else:story.append(Paragraph(escape(item),styles["BodyText"]))
  story.append(Spacer(1,10))
addpage("Sprint 3 - Divida tecnica (1/3)",[
"Escopo: modulos de livros, noticias, schemas e componente administrativo das historias selecionadas. Oito itens concretos, relacionados a coesao, integridade conceitual, acoplamento, SRP/DIP, duplicacao e Magic Literals. Nenhum requisito novo implementado.",
[["ID/status","Local","Consequencia"],["DT-01/refatorado","normalize_book","Validacao de formatos misturada a normalizacao; 29 linhas e cinco decisoes AST."],["DT-02/refatorado","gutendex.py","Mensagem identica repetida tres vezes; manutencao pode divergir."],["DT-03/refatorado","list_news/list_admin_news","Politica 100 repetida em defaults e validacao."],["DT-04/aberto","_get_json","Acoplamento a AsyncClient concreto exige monkeypatch global."],["DT-05/aberto","upload_image","HTTP, arquivo e transacao compartilham procedimento."],["DT-06/aberto","create/update_news","Commit/refresh repetidos nas rotas."],["DT-07/aberto","NewsCreate/NewsUpdate","Restricoes repetidas podem divergir."],["DT-08/aberto","PainelNoticias","Estado de consulta, pagina e formulario concentrados."]],
"Escolha: DT-01 ja possuia caracterizacao de None/formatos invalidos; DT-02 tinha mensagens verificadas; DT-03 ganhou testes das duas rotas ANTES de mudar. Sao riscos de manutencao, nao alegacoes de defeitos funcionais."])
addpage("Tres alteracoes e evidencias (2/3)",[
"DT-01 - Extract Function: antes normalize_book validava formatos inline; depois chama _normalize_formats(raw.get('formats')). Preserva None->dict vazio, rejeicao de tipos/valores invalidos e retorno dos mesmos campos. Melhora coesao/SRP. Commit "+commits["DT-01"]+".",
"DT-02 - Extract Constant: antes tres copias da mesma mensagem HTTP 503; depois INVALID_PAYLOAD_MESSAGE e reutilizada por JSON, lista e detalhe invalidos. Elimina duplicacao e risco de inconsistencias. Commit "+commits["DT-02"]+".",
"DT-03 - Replace Magic Literal: antes Query(100,ge=1,le=100) em duas rotas; depois MAX_NEWS_PAGE_SIZE expressa uma unica politica, mantendo os mesmos limites. Melhora integridade conceitual. Commit "+commits["DT-03"]+".",
"Resultado: 78/78 testes passaram antes e depois de cada uma das tres refatoracoes; zero falhas e zero erros de coleta. Caracterizacao previa inclui limites publico/admin 0/1/100/101 e oraculo de cardinalidade. Nenhum teste foi retirado nem alterado para passar.",
"Diffs: git show "+commits["DT-01"]+"; git show "+commits["DT-02"]+"; git show "+commits["DT-03"]+". Logs, JUnit e cobertura de cada etapa estao em docs/testes/relatorios/refatoracao-*/."])
addpage("Comparacao das analises e conclusao (3/3)",[
"Leitura dirigida identificou o contexto que o AST nao decide: o limite 100 e politica compartilhada, mas 404/422 sao linguagem do protocolo. A LLM relacionou validacao/normalizacao a coesao e o transporte concreto a DIP; essas classificacoes foram confrontadas com trechos reais.",
"AST forneceu evidencias reproduziveis: normalize_book tinha 29 linhas/cinco decisoes; _get_json tinha 49 linhas/oito decisoes; a mensagem era repetida tres vezes. Contagens apontam sinais, nao certificam violacao SOLID nem medem qualidade sozinhas. Evidencias: evidencias-ast.json e tests/analise_qualidade.py.",
"Falsos positivos relevantes: nao ha LSP entre schemas sem heranca; duplicacao de restricoes nao justifica herdar indiscriminadamente. PATCH vazio e permitido; titulo com espacos nao viola o criterio de comprimento. Nenhum desses comportamentos foi alterado para criar uma suposta correcao.",
"Vantagem da combinacao: ferramenta mede, leitura confere contrato e impacto, LLM sugere classificacao/refatoracao. Limite: geracao e leitura foram feitas pelo assistente de IA; nao ha revisao humana independente comprovada. A equipe deve validar as conclusoes, sem atribuir autoria humana ficticia.",
"Somente tres itens foram pagos e cinco seguem abertos. A suite protege os comportamentos selecionados, nao prova ausencia de qualquer regressao fora do escopo. Nenhum teste anterior de integracao funcional foi repetido. Modelo Codex baseado em GPT-6; snapshot exato nao exposto. Nao houve push, nova branch ou alteracao da main."])
SimpleDocTemplate(str(Q/"relatorio-refatoracao.pdf"),pagesize=A4,leftMargin=35,rightMargin=35,topMargin=30,bottomMargin=30).build(story)
# Complete the initial metric table in the matrix, retaining original planning in Git.
p=D/"matriz-rastreabilidade.md";lines=p.read_text(encoding="utf-8").splitlines();out=[]
vals=[("Testes gerados","25/25/0/0","78/78/0/0"),("Cobertura de linhas","79,46%","91,07%"),("Cobertura de branches","54,55%","88,64%"),("Cobertura de crit","100% (12/12)","100% (12/12)"),("Parti","91,67% (33/36)","100% (36/36)"),("Valores-limite","81,25% (13/16)","100% (16/16)"),("Testes sem","0/0","0/0"),("Defeitos reais","0","0")]
for line in lines:
 if line.startswith("|") and "—" in line:
  for prefix,a,b in vals:
   if line.startswith("| "+prefix):
    fields=line.split("|");fields[2]=" "+a+" ";fields[3]=" "+b+" ";line="|".join(fields);break
 out.append(line)
p.write_text("\n".join(out)+"\n",encoding="utf-8")
req=D/"requisitos-v1.md"
if not req.exists():
 lines=p.read_text(encoding="utf-8").splitlines()
 req.write_text("# Requisitos fornecidos antes da geracao\n\n"+"\n".join(lines[27:70])+"\n",encoding="utf-8")
pathlib.Path(".gitattributes").write_text("*.pdf -text\n",encoding="utf-8")
pdfs={}
for file,limit in [(D/"relatorio-critico.pdf",5),(Q/"relatorio-refatoracao.pdf",3)]:
 count=len(re.findall(rb"/Type\s*/Page\b",file.read_bytes()))
 assert 0<count<=limit,(file,count)
 pdfs[str(file)]={"pages":count,"bytes":file.stat().st_size}
pathlib.Path("docs/qualidade/entrega-verificada.json").write_text(json.dumps({"pdfs":pdfs,"refactor_commits":commits},indent=2),encoding="utf-8")
print(json.dumps({"pdfs":pdfs,"refactor_commits":commits}))
