import sys
import time
import platform
import psutil

# --- Algoritmos de Ordenação ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def efficient_sort(arr):
    # O Timsort é o algoritmo de ordenação padrão do Python, altamente eficiente.
    arr.sort()
    return arr

# --- Função Principal ---
def main(algorithm):
    # Medição de Memória Inicial
    process = psutil.Process()
    mem_before = process.memory_info().rss

    # Ler os números do arquivo
    try:
        with open('arq.txt', 'r') as f:
            numbers = [int(line.strip()) for line in f]
    except FileNotFoundError:
        print("Erro: Arquivo 'arq.txt' não encontrado. Execute o 'gerar_numeros.py' primeiro.")
        return

    # Medição de Tempo - Início
    start_time = time.perf_counter()

    # Executar o algoritmo de ordenação escolhido
    if algorithm == 'bubble':
        sorted_numbers = bubble_sort(numbers)
    elif algorithm == 'efficient':
        sorted_numbers = efficient_sort(numbers)
    else:
        print(f"Erro: Algoritmo '{algorithm}' desconhecido.")
        return

    # Medição de Tempo - Fim
    end_time = time.perf_counter()
    
    # Medição de Memória Final
    mem_after = process.memory_info().rss
    
    # Escrever os números ordenados no arquivo de saída
    with open('arq-saida.txt', 'w') as f:
        for number in sorted_numbers:
            f.write(str(number) + '\n')

    # --- Saída das Informações ---
    # Informações da linguagem e sistema
    print("--- System Info ---")
    print(f"Language: Python")
    print(f"Version: {sys.version}")
    print(f"System: {platform.system()} {platform.release()}")
    cpu_info = f"{psutil.cpu_count(logical=True)} Cores, {psutil.cpu_freq().max:.2f} Mhz" if psutil.cpu_freq() else f"{psutil.cpu_count(logical=True)} Cores"
    print(f"CPU: {cpu_info}")
    print(f"Total RAM: {psutil.virtual_memory().total / (1024**3):.2f} GB")
    
    # Informações de performance
    execution_time_ms = (end_time - start_time) * 1000
    memory_used_kb = (mem_after - mem_before) / 1024

    print("\n--- Performance ---")
    print(f"Time: {execution_time_ms:.4f}")
    print(f"Memory: {memory_used_kb:.4f}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python sorter_py.py <bubble|efficient>")
    else:
        main(sys.argv[1])