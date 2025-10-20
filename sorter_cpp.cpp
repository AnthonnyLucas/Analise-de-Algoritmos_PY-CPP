#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm> // Para std::sort

// --- Algoritmos de Ordenação ---
void bubble_sort(std::vector<int>& arr) {
    int n = arr.size();
    bool swapped;
    for (int i = 0; i < n - 1; ++i) {
        swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }
}

void efficient_sort(std::vector<int>& arr) {
    // std::sort usa Introsort, um híbrido de Quicksort, Heapsort e Insertion sort.
    // É extremamente eficiente.
    std::sort(arr.begin(), arr.end());
}


// --- Função Principal ---
int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Uso: ./sorter_cpp <bubble|efficient>" << std::endl;
        return 1;
    }
    std::string algorithm = argv[1];

    // Ler os números do arquivo
    std::ifstream inputFile("arq.txt");
    if (!inputFile) {
        std::cerr << "Erro: Arquivo 'arq.txt' não encontrado." << std::endl;
        return 1;
    }
    std::vector<int> numbers;
    int number;
    while (inputFile >> number) {
        numbers.push_back(number);
    }
    inputFile.close();

    // Medição de Tempo - Início
    auto start = std::chrono::high_resolution_clock::now();

    // Executar o algoritmo de ordenação escolhido
    if (algorithm == "bubble") {
        bubble_sort(numbers);
    } else if (algorithm == "efficient") {
        efficient_sort(numbers);
    } else {
        std::cerr << "Erro: Algoritmo '" << algorithm << "' desconhecido." << std::endl;
        return 1;
    }

    // Medição de Tempo - Fim
    auto end = std::chrono::high_resolution_clock::now();
    
    // Escrever os números ordenados no arquivo de saída
    std::ofstream outputFile("arq-saida.txt");
    for (const int& num : numbers) {
        outputFile << num << "\n";
    }
    outputFile.close();

    // --- Saída das Informações ---
    // Informações da linguagem e sistema
    std::cout << "--- System Info ---" << std::endl;
    std::cout << "Language: C++" << std::endl;
    #if defined(__GNUC__)
        std::cout << "Compiler: GCC " << __VERSION__ << std::endl;
    #elif defined(_MSC_VER)
        std::cout << "Compiler: MSVC " << _MSC_VER << std::endl;
    #else
        std::cout << "Compiler: Unknown" << std::endl;
    #endif
    
    // Informações de performance
    std::chrono::duration<double, std::milli> execution_time_ms = end - start;
    
    std::cout << "\n--- Performance ---" << std::endl;
    std::cout << "Time: " << execution_time_ms.count() << std::endl;
    // A medição de RAM precisa não é padrão, então não a incluímos para manter a portabilidade.
    std::cout << "Memory: N/A" << std::endl;


    return 0;
}