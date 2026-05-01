"""
métodos de ordenação com o Big-O
"""

import time
import random

# metodo por inserção
def insertion_sort(lista):
    comparacoes = 0
    trocas = 0
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]  # desloca elemento uma posição
            j -= 1
            comparacoes += 1
            trocas += 1            # cada deslocamento conta como troca
        lista[j + 1] = chave
        comparacoes += 1
    return lista, comparacoes, trocas


# método por seleção
def selection_sort(lista):
    comparacoes = 0
    trocas = 0
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparacoes += 1
            if lista[j] < lista[min_idx]:
                min_idx = j
        if min_idx != i:
            lista[i], lista[min_idx] = lista[min_idx], lista[i]  # swap real
            trocas += 1                                           # 1 swap = 1 troca
    return lista, comparacoes, trocas


# metodo híbrido
def shell_sort(lista):
    comparacoes = 0
    trocas = 0
    n = len(lista)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = lista[i]
            j = i
            while j >= gap and lista[j - gap] > temp:
                lista[j] = lista[j - gap]  # desloca elemento pelo gap
                j -= gap
                comparacoes += 1
                trocas += 1               # cada deslocamento conta como troca
            lista[j] = temp
            comparacoes += 1
        gap //= 2
    return lista, comparacoes, trocas


# metodo por partição
comparacoes_merge = 0
trocas_merge = 0

def merge_sort(lista):
    global comparacoes_merge
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esq = merge_sort(lista[:meio])
    dir = merge_sort(lista[meio:])
    return merge(esq, dir)

def merge(esq, dir):
    global comparacoes_merge, trocas_merge
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        comparacoes_merge += 1
        if esq[i] <= dir[j]:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
        trocas_merge += 1          # cada elemento copiado para o resultado = 1 troca
    # copia os elementos restantes
    for x in esq[i:]:
        resultado.append(x)
        trocas_merge += 1
    for x in dir[j:]:
        resultado.append(x)
        trocas_merge += 1
    return resultado


# rodar o algoritmo e medir o tempo
def executar(func, lista_original, usa_global=False):
    global comparacoes_merge, trocas_merge
    lista = lista_original.copy()

    inicio = time.perf_counter()

    if usa_global:
        comparacoes_merge = 0
        trocas_merge = 0
        lista = func(lista)
        comparacoes = comparacoes_merge
        trocas = trocas_merge
    else:
        lista, comparacoes, trocas = func(lista)

    fim = time.perf_counter()
    tempo = (fim - inicio) * 1000  # em milissegundos

    return lista, comparacoes, trocas, tempo


# resultados
def exibir_relatorio(resultados, n):
    print("\n" + "=" * 20)
    print(f"  relatorio — {n} elementos")
    print("=" * 20)
    print(f"  {'Algoritmo':<18} {'Big-O':<14} {'Comparações':>12} {'Trocas':>10} {'Tempo':>8}")
    print("-" * 20)
    for r in resultados:
        print(
            f"  {r['nome']:<18} {r['big_o']:<14} "
            f"{r['comparacoes']:>12,} {r['trocas']:>10,} {r['tempo']:>6.3f}ms"
        )

# add vetor manualmente
def entrada_manual():
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
def rodar_algoritmos(lista_original):
    algoritmos = [
        {"nome": "Insertion Sort", "big_o": "O(n²)",       "func": insertion_sort, "global": False},
        {"nome": "Selection Sort", "big_o": "O(n²)",       "func": selection_sort, "global": False},
        {"nome": "Shell Sort",     "big_o": "O(n log² n)", "func": shell_sort,     "global": False},
        {"nome": "Merge Sort",     "big_o": "O(n log n)",  "func": merge_sort,     "global": True},
    ]

    resultados = []
    lista_final = None

    for alg in algoritmos:
        lista_ord, comp, trocas, tempo = executar(alg["func"], lista_original, alg["global"])
        if lista_final is None:
            lista_final = lista_ord
        resultados.append({
            "nome":        alg["nome"],
            "big_o":       alg["big_o"],
            "comparacoes": comp,
            "trocas":      trocas,
            "tempo":       tempo,
        })

    return resultados, lista_final

# menu principal
def menu():
    print("\n" + "=" * 20)
    print("  MÉTODOS DE ORDENAÇÃO COM BIG-O")
    print("=" * 20)
    print("  [1] Add vetor manualmente")
    print("  [2] Testes de vetores pequenos, médios e grandes")
    print("  [0] exit")
    print("-" * 20)
    return input("  escolha uma opção: ").strip()

# programa principal
if __name__ == "__main__":

    while True:
        opcao = menu()

        if opcao == "1":
            lista_original = entrada_manual()
            n = len(lista_original)
            resultados, lista_ord = rodar_algoritmos(lista_original)
            exibir_relatorio(resultados, n)
            print(f"\nresultado de forma ordenada: {lista_ord}")

        elif opcao == "2":
            for n in [1000, 10000, 50000]:
                lista_original = random.sample(range(1, n * 10), n)
                resultados, _ = rodar_algoritmos(lista_original)
                exibir_relatorio(resultados, n)

        elif opcao == "0":
            print("\nprograma fechado\n")
            break

        else:
            print("opção incorreta")
