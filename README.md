# Simulador Espacial de Arboviroses: Febre Amarela Urbana via Autômatos Celulares

## Sumário
Este projeto implementa um modelo matemático-computacional discreto para simular a propagação da Febre Amarela Urbana. Em vez de utilizar Equações Diferenciais Ordinárias (EDOs) clássicas que assumem uma população perfeitamente misturada (homogênea), o modelo utiliza a teoria dos Autômatos Celulares (CA), especificamente através de Malhas Acopladas (*Coupled Map Lattices*). 

Isso permite analisar espacialmente dois fenômenos críticos na transmissão de doenças vetoriais:
1. **O Efeito de Focos Localizados (Heterogeneidade Espacial):** Como a epidemia surge em um ponto específico de acúmulo hídrico e se espalha geograficamente criando uma "frente de onda".
2. **Mobilidade Humana vs. Mobilidade do Vetor:** O contraste entre o curto raio de voo do mosquito *Aedes aegypti* (difusão local lenta) e os saltos de longa distância humanos impulsionados pela malha de transporte urbano (espalhamento global estocástico de múltiplos focos).

## Algoritmos
O sistema matemático é governado pelas interações de dois compartimentos populacionais acoplados geograficamente:
- **Modelo Humano (SIR):** Populações de Suscetíveis, Infectados e Recuperados.
- **Modelo do Vetor (SI):** Populações de Suscetíveis e Infectados (assumindo que o mosquito não se recupera).

A dinâmica espacial do algoritmo é dividida em duas etapas de transição:
1. **Difusão do Mosquito:** A capacidade restrita de voo do vetor é calculada iterativamente aplicando uma matriz de convolução bidimensional (*Kernel* de Vizinhança de Moore) sobre o reticulado espacial.
2. **Saltos Humanos (Mobilidade):** Uma fração (ex: 5%) da população humana virêmica é realocada de forma randômica por toda a grade espacial a cada iteração, mimetizando deslocamentos pendulares pelo sistema de transporte.

## Linguagem e Bibliotecas
O simulador foi desenvolvido integralmente em **Python**. As bibliotecas científicas responsáveis pelo processamento e visualização são:
- **NumPy (`numpy`):** Estruturação e manipulação eficiente das matrizes de densidade populacional (grade do Autômato Celular).
- **SciPy (`scipy.signal`):** Utilização da função de processamento de sinais `convolve2d` para resolver de forma otimizada o espalhamento matemático espacial dos mosquitos para as células vizinhas.
- **Matplotlib (`matplotlib.pyplot`):** Renderização gráfica das matrizes em painéis visuais de *Heatmaps* (Mapas de Calor), contrastando os cenários temporais simulados.

## Como Rodar o Projeto

Siga os passos abaixo para configurar o ambiente e executar a simulação na sua máquina local.

### 1. Clonar o Repositório
Faça o clone do projeto para a sua máquina:
```bash
git clone [https://github.com/SeuUsuario/simulador-espacial-arboviroses.git](https://github.com/SeuUsuario/simulador-espacial-arboviroses.git)
cd simulador-espacial-arboviroses
```

### 2. Configurar o Ambiente Virtual (venv)
É recomendado criar um ambiente virtual para isolar as dependências matemáticas do projeto:
1. Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
2. Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar os Requisitos
Com o ambiente ativado, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 4. Executar a Simulação
Para iniciar o cálculo das malhas acopladas e gerar as visualizações espaciais, basta rodar o arquivo principal:
```bash
python main.py
```
