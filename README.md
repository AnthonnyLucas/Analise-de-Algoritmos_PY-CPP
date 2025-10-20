# Análise Comparativa de Algoritmos de Ordenação (Python vs. C++)

Este projeto realiza uma análise de desempenho detalhada, comparando o tempo de execução e o pico de uso de memória de algoritmos de ordenação. A análise é conduzida em dois cenários:

1.  **Algoritmo Ineficiente:** Uma implementação do **Bubble Sort** é testada em Python e C++.
2.  **Algoritmo Eficiente:** Os algoritmos de ordenação nativos e otimizados de cada linguagem são comparados (o **Timsort** do Python, acessado via `list.sort()`, e o **Introsort** do C++, acessado via `std::sort`).

O objetivo é quantificar as diferenças de performance não apenas entre os algoritmos ($O(n^2)$ vs. $O(n \log n)$), mas também entre as linguagens (Python interpretado vs. C++ compilado).

## O que este projeto faz?

O script principal (`analise.py`) orquestra todo o processo de análise. Ele automaticamente:

1.  Lê uma lista de números a serem ordenados a partir do arquivo `arq.txt`.
2.  Executa quatro cenários de teste distintos:
      * Bubble Sort em Python
      * Ordenação Eficiente em Python
      * Bubble Sort em C++
      * Ordenação Eficiente em C++
3.  Para cada cenário, ele inicia o processo e monitora externamente o **pico de uso de memória física (RSS)**.
4.  Mede o **tempo de execução** reportado pelo próprio script (em milissegundos).
5.  Repete cada um desses testes **10 vezes** para garantir consistência estatística.
6.  Calcula a **média** e a **mediana** tanto para o tempo de execução quanto para o pico de memória.
7.  Imprime uma tabela formatada com todos os resultados diretamente no terminal.
8.  Gera e salva **4 gráficos de barras** (`.png`) para visualização comparativa dos resultados.

## Como Utilizar (Passo a Passo)

Para executar este projeto em sua máquina local ou em um ambiente de nuvem (como Codespaces ou Replit), siga estes passos.

### Passo 1: Obter o Código

Primeiramente, obtenha os arquivos do projeto. Se estiver usando `git`, clone este repositório:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

### Passo 2: Preparar o Ambiente (Dependências)

Este projeto possui dependências tanto em Python quanto em C++.

**Dependências Python:**
O script de análise usa as bibliotecas `psutil` (para monitorar a memória) e `matplotlib` (para gerar os gráficos). É uma boa prática instalar isso em um ambiente virtual:

```bash
# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ative o ambiente virtual
# No Windows:
.\venv\Scripts\activate
# No Linux/macOS/Codespaces:
source venv/bin/activate

# Instale as bibliotecas necessárias
pip install psutil matplotlib
```

**Dependências C++ (Compilador):**
Você precisará de um compilador C++ (como o `g++`) instalado em seu sistema.

  * **No Linux (Ubuntu/Debian) ou GitHub Codespaces:**
    ```bash
    sudo apt-get update && sudo apt-get install build-essential g++
    ```
  * **No Windows:**
    Recomenda-se a instalação do [MinGW-w64](https://www.mingw-w64.org/) para obter o `g++`.

### Passo 3: Compilar o Código C++

O script `analise.py` não executa o código `.cpp` diretamente; ele executa um arquivo binário compilado. Você deve compilar o `sorter_cpp.cpp` uma vez antes de rodar a análise.

Use o comando de compilação apropriado para o seu sistema:

  * **No Linux, macOS ou GitHub Codespaces:**

    ```bash
    g++ -std=c++17 -O2 -o sorter_cpp sorter_cpp.cpp
    ```

    (A flag `-O2` é importante, pois otimiza o código para velocidade, tornando a comparação justa).

  * **No Windows (usando Powershell com MinGW/g++):**
    O Powershell pode ter problemas com os argumentos do linker. Use este comando específico para forçar a criação de um aplicativo de console:

    ```bash
    g++ -std=c++17 -O2 -o sorter_cpp sorter_cpp.cpp "-Wl,-subsystem,console"
    ```

Se o comando for bem-sucedido, um novo arquivo chamado `sorter_cpp` (ou `sorter_cpp.exe` no Windows) aparecerá na sua pasta.

### Passo 4: Preparar o Arquivo de Entrada

Certifique-se de que o arquivo `arq.txt` está presente na raiz do projeto. Este arquivo deve conter os números que você deseja ordenar, com **exatamente um número inteiro por linha**.

### Passo 5: Executar a Análise Completa

Com as dependências instaladas e o código C++ compilado, você está pronto para rodar o projeto. Basta executar o script `analise.py`:

```bash
python analise.py
```

Aguarde a conclusão. O processo pode demorar, especialmente durante as 10 rodadas do Bubble Sort em Python.

## Entendendo os Resultados (Saída)

Após a execução, você receberá dois tipos de saída:

1.  **Tabela no Terminal:** Uma tabela formatada aparecerá, mostrando a média e a mediana de tempo (ms) e memória (KB) para cada um dos quatro cenários.

    ```
    --- Resultados da Análise ---
    Algoritmo            | Média Tempo (ms)     | Mediana Tempo (ms)   | Média Memória (KB)       | Mediana Memória (KB)
    -------------------------------------------------------------------------------------------------------------
    Python_Bubble        | 36623.5795           | 36639.1796           | 1476.0000                | 1472.0000
    Python_Efficient     | 3.3447               | 3.2811               | 1459.2000                | 1392.0000
    Cpp_Bubble           | 1894.3270            | 1893.6050            | 980.0000                 | 978.0000
    Cpp_Efficient        | 1.3152               | 1.2986               | 972.0000                 | 970.0000
    ```

2.  **Gráficos (Arquivos .png):** Quatro arquivos de imagem serão salvos na raiz do projeto, permitindo uma fácil visualização e comparação dos dados:

      * `grafico_media_tempo.png`
      * `grafico_mediana_tempo.png`
      * `grafico_media_memoria.png`
      * `grafico_mediana_memoria.png`

## Estrutura dos Arquivos

  * `sorter_py.py`: Contém as implementações de ordenação em Python (Bubble Sort e `list.sort()`). É chamado pelo `analise.py` e reporta apenas seu próprio tempo de execução.
  * `sorter_cpp.cpp`: Contém as implementações de ordenação em C++ (Bubble Sort e `std::sort`). É compilado para um executável e reporta apenas seu próprio tempo de execução.
  * `analise.py`: O orquestrador principal. Este script executa os programas Python e C++, mede o pico de memória externamente (usando `psutil`) e coleta o tempo reportado. Ele também calcula as estatísticas e gera os gráficos (usando `matplotlib`).
  * `arq.txt`: O arquivo de dados de entrada.
