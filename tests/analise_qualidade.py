import ast,json,pathlib
files=["backend/app/services/gutendex.py","backend/app/api/routes/news.py","backend/app/schemas/news.py","backend/app/services/news.py"]
out={}
for name in files:
    text=pathlib.Path(name).read_text(encoding="utf-8-sig")
    tree=ast.parse(text)
    funcs=[]
    for n in ast.walk(tree):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
            funcs.append({"name":n.name,"line":n.lineno,"lines":n.end_lineno-n.lineno+1,"decisions_ast":sum(isinstance(x,(ast.If,ast.For,ast.While,ast.ExceptHandler,ast.IfExp)) for x in ast.walk(n))})
    out[name]={"functions":funcs,"imports":[ast.unparse(x) for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom))],"invalid_message_literals":text.count("retornou uma resposta")}
pathlib.Path("docs/qualidade").mkdir(parents=True,exist_ok=True)
pathlib.Path("docs/qualidade/evidencias-ast.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out))
