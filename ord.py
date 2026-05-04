# metodo de ordenação com big-o - nathan, gustavo, helen e lennon

import time
import random


# rodar o algoritmo e medir o tempo
def executar(func, listaOriginal, usaGlobal=False):
    global comparacoesMerge, trocasMerge
    lista = listaOriginal.copy()

    inicio = time.perf_counter()

    if usaGlobal:
        comparacoesMerge = 0
        trocasMerge = 0
        lista = func(lista)
        comparacoes = comparacoesMerge
        trocas = trocasMerge
    else:
        lista, comparacoes, trocas = func(lista)

    fim = time.perf_counter()
    tempo = (fim - inicio) * 1000  # em milissegundos

    return lista, comparacoes, trocas, tempo


# metodo por inserção
def inserção(lista):
    comparacoes = 0
    trocas = 0
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]  
            j -= 1
            comparacoes += 1
            trocas += 1            
        lista[j + 1] = chave
        comparacoes += 1
    return lista, comparacoes, trocas


# método por seleção
def seleção(lista):
    comparacoes = 0
    trocas = 0
    n = len(lista)
    for i in range(n):
        minIdx = i
        for j in range(i + 1, n):
            comparacoes += 1
            if lista[j] < lista[minIdx]:
                minIdx = j
        if minIdx != i:
            lista[i], lista[minIdx] = lista[minIdx], lista[i]  
            trocas += 1                                         
    return lista, comparacoes, trocas


# metodo híbrido
def híbrido(lista):
    comparacoes = 0
    trocas = 0
    n = len(lista)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = lista[i]
            j = i
            while j >= gap and lista[j - gap] > temp:
                lista[j] = lista[j - gap] 
                j -= gap
                comparacoes += 1
                trocas += 1              
            lista[j] = temp
            comparacoes += 1
        gap //= 2
    return lista, comparacoes, trocas


# metodo por partição
comparacoesMerge = 0
trocasMerge = 0

def partiçãosort(lista):
    global comparacoesMerge
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esq = partiçãosort(lista[:meio])
    dir = partiçãosort(lista[meio:])
    return partição(esq, dir)

def partição(esq, dir):
    global comparacoesMerge, trocasMerge
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        comparacoesMerge += 1
        if esq[i] <= dir[j]:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
        trocasMerge += 1          
    for x in esq[i:]:
        resultado.append(x)
        trocasMerge += 1
    for x in dir[j:]:
        resultado.append(x)
        trocasMerge += 1
    return resultado


# resultados
def exibirRelatorio(resultados, n):
    print("\n" + "=" * 20)
    print(f"  relatorio — {n} elementos")
    print("=" * 20)
    print(f"  {'Algoritmo':<18} {'Big-O':<14} {'Comparações':>12} {'Trocas':>10} {'Tempo':>8}")
    print("-" * 20)
    for r in resultados:
        print(
            f"  {r['nome']:<18} {r['bigO']:<14} "
            f"{r['comparacoes']:>12,} {r['trocas']:>10,} {r['tempo']:>6.3f}ms"
        )

# add vetor manualmente
def entradaManual():
    print("\ndigite os números para o vetor")
    print("exemplo: 42, 7, 19, 3")

    while True:
        entrada = input(">> ").strip()
        if not entrada:
            print("Vazio")
            continue
        try:
            entrada = entrada.replace(",", " ")
            lista = [int(x) for x in entrada.split() if x]
            if len(lista) < 2:
                print("digite pelo menos 2 números.")
                continue
            print(f"Vetor recebido: {lista}")
            return lista
        except ValueError:
            print("apenas numeros inteiros")

# roda os algoritmos da lista
def rodarAlgoritmos(listaOriginal):
    algoritmos = [
        {"nome": "inserção",  "bigO": "O(n²)",       "func": inserção,    "global": False},
        {"nome": "seleção",   "bigO": "O(n²)",       "func": seleção,     "global": False},
        {"nome": "híbrido",   "bigO": "O(n log² n)", "func": híbrido,     "global": False},
        {"nome": "partição",  "bigO": "O(n log n)",  "func": partiçãosort, "global": True},
    ]

    resultados = []
    listaFinal = None

    for alg in algoritmos:
        listaOrd, comp, trocas, tempo = executar(alg["func"], listaOriginal, alg["global"])
        if listaFinal is None:
            listaFinal = listaOrd
        resultados.append({
            "nome":        alg["nome"],
            "bigO":        alg["bigO"],
            "comparacoes": comp,
            "trocas":      trocas,
            "tempo":       tempo,
        })

    return resultados, listaFinal

# menu principal
def menu():
    print("  MÉTODOS DE ORDENAÇÃO COM BIG-O")
    print("/" * 20)
    print("  [1] Add vetor manualmente")
    print("  [2] Testes de vetores pequenos, médios e grandes")
    print("  [0] sair")
    print("/" * 20)
    return input("  escolha uma opção: ").strip()

# programa principal
if __name__ == "__main__":

    while True:
        opcao = menu()

        if opcao == "1":
            listaOriginal = entradaManual()
            n = len(listaOriginal)
            resultados, listaOrd = rodarAlgoritmos(listaOriginal)
            exibirRelatorio(resultados, n)
            print(f"\nresultado de forma ordenada: {listaOrd}")

        elif opcao == "2":
            for n in [1000, 10000, 50000]:
                listaOriginal = random.sample(range(1, n * 10), n)
                resultados, listaFinal = rodarAlgoritmos(listaOriginal)
                exibirRelatorio(resultados, n)

        elif opcao == "0":
            print("\nprograma fechado\n")
            break

        else:
            print("opção incorreta")
