import subprocess
import re
import statistics
import matplotlib.pyplot as plt
import numpy as np
import platform
import psutil  # Importado aqui para monitorar
import time    # Importado para o polling

# --- Configurações ---
NUM_RUNS = 10
# Define o nome do executável C++ baseado no sistema operacional
cpp_executable = './sorter_cpp.exe' if platform.system() == "Windows" else './sorter_cpp'

COMMANDS = {
    'Python_Bubble': ['python', 'sorter_py.py', 'bubble'],
    'Python_Efficient': ['python', 'sorter_py.py', 'efficient'],
    'Cpp_Bubble': [cpp_executable, 'bubble'],
    'Cpp_Efficient': [cpp_executable, 'efficient']
}

# Dicionário para armazenar todos os resultados
results = {key: {'time': [], 'memory': []} for key in COMMANDS}

def parse_output_time(output):
    """Extrai APENAS o tempo da saída do console."""
    time_match = re.search(r'Time: (\d+\.?\d*)', output)
    time_val = float(time_match.group(1)) if time_match else None
    return time_val

# --- Execução e Coleta de Dados ---
for name, command in COMMANDS.items():
    print(f"--- Executando {name} {NUM_RUNS} vezes ---")
    for i in range(NUM_RUNS):
        print(f"  Rodada {i + 1}/{NUM_RUNS}...")
        try:
            # Inicia o processo para podermos monitorá-lo
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            ps_process = psutil.Process(process.pid)
            
            peak_mem_kb = 0
            # Monitora o uso de memória enquanto o processo está rodando
            while process.poll() is None:
                try:
                    mem_info = ps_process.memory_info()
                    # rss = Resident Set Size (memória física)
                    current_mem_kb = mem_info.rss / 1024 
                    if current_mem_kb > peak_mem_kb:
                        peak_mem_kb = current_mem_kb
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # Processo pode ter terminado entre o poll() e a medição
                    break 
                time.sleep(0.01) # Verifica a cada 10ms
            
            # Pega a saída final (stdout) e erros (stderr)
            stdout, stderr = process.communicate() 
            
            # Verifica se o processo terminou com erro
            if process.returncode != 0:
                print(f"ERRO ao executar {name}: {stderr}")
                continue # Pula para a próxima rodada

            # Extrai o tempo da saída do console
            time_val = parse_output_time(stdout)
            
            if time_val is not None:
                results[name]['time'].append(time_val)
                # Adiciona o pico de memória medido externamente
                results[name]['memory'].append(peak_mem_kb)

        except FileNotFoundError:
            print(f"ERRO: O executável '{command[0]}' não foi encontrado.")
            print("Certifique-se de que você compilou o C++ com 'g++'.")
            exit()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
             # Processo pode ter terminado super rápido, antes do psutil pegar
             # Isso é comum em Cpp_Efficient
            stdout, stderr = process.communicate() # Pega a saída de qualquer forma
            time_val = parse_output_time(stdout)
            if time_val is not None:
                print("  Processo foi rápido. Medição de memória pode ser 0.")
                results[name]['time'].append(time_val)
                results[name]['memory'].append(0) # Não conseguiu medir
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            exit()

# --- Cálculo das Estatísticas ---
summary = {}
for name, data in results.items():
    if not data['time']: # Pula se não houver dados (devido a um erro)
        continue
    summary[name] = {
        'time_mean': statistics.mean(data['time']),
        'time_median': statistics.median(data['time']),
        'mem_mean': statistics.mean(data['memory']),
        'mem_median': statistics.median(data['memory']),
    }

# --- Apresentação dos Resultados em Tabela ---
print("\n\n--- Resultados da Análise ---")
print(f"{'Algoritmo':<20} | {'Média Tempo (ms)':<20} | {'Mediana Tempo (ms)':<20} | {'Média Memória (KB)':<22} | {'Mediana Memória (KB)':<22}")
print("-" * 110)
for name, stats in summary.items():
    print(f"{name:<20} | {stats['time_mean']:<20.4f} | {stats['time_median']:<20.4f} | {stats['mem_mean']:<22.4f} | {stats['mem_median']:<22.4f}")

# --- Geração dos Gráficos ---
if not summary:
    print("\nNenhuma análise foi concluída. Não foi possível gerar gráficos.")
else:
    labels = list(summary.keys())
    time_means = [s['time_mean'] for s in summary.values()]
    time_medians = [s['time_median'] for s in summary.values()]
    mem_means = [s['mem_mean'] for s in summary.values()]
    mem_medians = [s['mem_median'] for s in summary.values()]

    # Gráfico 1: Média de Tempo
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(labels, time_means, color='skyblue')
    ax1.set_ylabel('Tempo (ms)')
    ax1.set_title('Média de Tempo de Execução por Algoritmo')
    ax1.set_yscale('log') # Escala log é boa para grandes variações
    plt.xticks(rotation=15, ha="right")
    fig1.tight_layout()
    plt.savefig('grafico_media_tempo.png')
    print("\nGráfico 'grafico_media_tempo.png' salvo.")

    # Gráfico 2: Mediana de Tempo
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(labels, time_medians, color='lightgreen')
    ax2.set_ylabel('Tempo (ms)')
    ax2.set_title('Mediana de Tempo de Execução por Algoritmo')
    ax2.set_yscale('log')
    plt.xticks(rotation=15, ha="right")
    fig2.tight_layout()
    plt.savefig('grafico_mediana_tempo.png')
    print("Gráfico 'grafico_mediana_tempo.png' salvo.")

    # Gráfico 3: Média de Memória
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.bar(labels, mem_means, color='salmon')
    ax3.set_ylabel('Pico de Memória Utilizada (KB)')
    ax3.set_title('Média de Pico de Memória Utilizada por Algoritmo')
    plt.xticks(rotation=15, ha="right")
    fig3.tight_layout()
    plt.savefig('grafico_media_memoria.png')
    print("Gráfico 'grafico_media_memoria.png' salvo.")

    # Gráfico 4: Mediana de Memória
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.bar(labels, mem_medians, color='plum')
    ax4.set_ylabel('Pico de Memória Utilizada (KB)')
    ax4.set_title('Mediana de Pico de Memória Utilizada por Algoritmo')
    plt.xticks(rotation=15, ha="right")
    fig4.tight_layout()
    plt.savefig('grafico_mediana_memoria.png')
    print("Gráfico 'grafico_mediana_memoria.png' salvo.")
    
    plt.show() # Mostra os gráficos