from flask import Flask, render_template, request
import itertools
from sympy import symbols, And, Or, Not, Implies, Equivalent, Xor
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Função para criar os símbolos lógicos a partir das variáveis da expressão
def criar_simbolos(proposicoes):
    return {p: symbols(p) for p in proposicoes}

# Função para substituir os operadores textuais pelos operadores simbólicos
def substituir_operadores(expressao):
    expressao = expressao.replace("and", "&")      # Substitui 'and' por &
    expressao = expressao.replace("or", "|")       # Substitui 'or' por |
    expressao = expressao.replace("not", "~")      # Substitui 'not' por ~
    expressao = expressao.replace("xor", "Xor")    # Substitui 'xor' por Xor
    expressao = expressao.replace("∧", "&")        # Substitui '∧' por &
    expressao = expressao.replace("∨", "|")        # Substitui '∨' por |
    expressao = expressao.replace("¬", "~")        # Substitui '¬' por ~
    expressao = expressao.replace("<>", "==")      # Substitui '<>' por Bicondicional
    expressao = expressao.replace("<", ">>")       # Substitui '<' por Implies
    expressao = expressao.replace(".", "&")        # Substitui '.' por AND
    expressao = expressao.replace("+", "|")        # Substitui '+' por OR
    return expressao

# Função para gerar a tabela-verdade
def gerar_tabela_verdade(expressao):
    expressao = substituir_operadores(expressao)

    # Identificar proposições (variáveis) na expressão
    proposicoes = sorted(set(filter(str.isalpha, expressao)))  # Identifica 'p', 'q', etc.
    simbolos = criar_simbolos(proposicoes)  # Cria símbolos para cada variável proposicional

    # Avaliar expressão usando SymPy
    try:
        # Gerar todas as combinações possíveis de verdade e falsidade
        combinacoes = list(itertools.product([True, False], repeat=len(proposicoes)))

        # Avaliar expressão para cada combinação de valores de verdade
        tabela = []
        for combinacao in combinacoes:
            valores = dict(zip(proposicoes, combinacao))  # Associa 'p', 'q' a 'True' ou 'False'
            # Substituir as variáveis na expressão por seus valores de verdade
            expr = eval(expressao, {'Xor': Xor, 'And': And, 'Or': Or, 'Not': Not, 'Implies': Implies, 'Equivalent': Equivalent}, simbolos)
            resultado = expr.subs(valores)
            linha = {'valores': combinacao, 'resultado': resultado}
            tabela.append(linha)

        return proposicoes, tabela
    except Exception as e:
        print(f"Erro: {e}")  # Adiciona log de erro para facilitar a depuração
        return None  # Retorna None se houver erro na avaliação

@app.route("/", methods=["GET", "POST"])
def index():
    erro = None
    tabela = None
    proposicoes = []
    expressao = ""
    
    if request.method == "POST":
        expressao = request.form.get("expressao")
        try:
            # Tentar gerar a tabela-verdade
            proposicoes, tabela = gerar_tabela_verdade(expressao)
            if tabela is None:
                erro = "A expressão inserida é inválida. Por favor, insira uma expressão válida."
            else:
                # Substituir operadores textuais pelos símbolos reais antes de exibir
                expressao_formatada = expressao.replace("&", "∧").replace("|", "∨").replace("~", "¬").replace("Xor", "⊕").replace(">>", "→").replace("==", "↔")
        except Exception as e:
            erro = "Erro ao processar a expressão. Tente novamente."
    
    # Passa 'expressao_formatada' em vez de 'expressao'
    return render_template("index.html", proposicoes=proposicoes, tabela=tabela, expressao=expressao_formatada if tabela else expressao, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)
