# Análise e Previsão da Qualidade do Ar com Machine Learning

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML-brightgreen.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-Boosting-blueviolet.svg)

## 📖 Descrição do Projeto

Este projeto acadêmico tem como objetivo desenvolver um pipeline completo de Data Science para coletar, organizar, analisar e prever a qualidade do ar em cidades brasileiras. A solução utiliza dados de fontes públicas (IEMA), aplica técnicas de análise exploratória de dados (EDA) e treina um modelo de Machine Learning para prever a concentração de poluentes, simulando uma aplicação de IoT.

O projeto documenta a jornada realista de um analista de dados, desde os desafios na coleta de dados brutos e inconsistentes, passando pela limpeza e transformação (ETL), até a criação e avaliação de um modelo preditivo com **XGBoost**.

## ✨ Funcionalidades e Etapas

O projeto é dividido em um fluxo de trabalho claro, refletido na estrutura de pastas:

1.  **Coleta de Dados:**
    - Coleta de dados históricos anuais a partir da base de dados consolidada do **IEMA (Instituto de Energia e Meio Ambiente)**.
    - Scripts legados para automação via **Selenium** e consumo de APIs (`CETESB`, `IQAir`), documentando os desafios de cada abordagem.

2.  **Limpeza e Pré-processamento (ETL):**
    - Notebook Jupyter (`03_notebooks/exploracao_inicial.ipynb`) que carrega os dados brutos.
    - Tratamento de erros de codificação de caracteres (`latin1`).
    - Transformação dos dados de formato "longo" para "largo" usando **pivotagem**, criando uma série temporal onde cada linha é uma hora e cada coluna um poluente.
    - Interpolação e preenchimento de dados ausentes.

3.  **Análise Exploratória de Dados (EDA):**
    - Geração de gráficos de série temporal para visualizar a variação dos poluentes (ex: MP2.5) ao longo do tempo.
    - Cálculo e plotagem de **médias móveis** e **médias diárias/mensais** (`resample`) para identificar tendências.
    - Análise de **correlação** entre diferentes poluentes através de um mapa de calor (heatmap).
    - Estudo de padrões sazonais e semanais com gráficos de `boxplot` para analisar a distribuição dos poluentes por dia da semana.

4.  **Engenharia de Features e Modelagem Preditiva:**
    - Criação de *features* (pistas) para o modelo a partir dos dados existentes:
        - **Features de Tempo:** Hora do dia, dia da semana, mês, dia do ano.
        - **Features de Lag:** Valores da poluição em horas anteriores (ex: 1h, 2h e 3h atrás).
        - **Média Móvel:** A média das últimas 3 horas como uma feature.
    - Treinamento de um modelo de regressão **XGBoost** para prever a concentração futura de um poluente alvo.
    - Divisão cronológica dos dados em conjuntos de **treino** (dados mais antigos) e **teste** (dados mais recentes), uma prática essencial para séries temporais.
    - Avaliação do modelo com métricas como **MAE (Erro Médio Absoluto)** e **RMSE (Erro Quadrático Médio)**.
    - Visualização da performance do modelo comparando os valores reais com as previsões.

5.  **Simulação de Aplicação IoT (`prever.py`):**
    - Criação de um script que **carrega o modelo treinado** e salvo (`.pkl`).
    - Busca o dado de qualidade do ar mais recente em tempo real usando a API da **IQAir**.
    - Executa a mesma engenharia de features no novo dado.
    - Utiliza o modelo para **fazer uma previsão** da qualidade do ar para a próxima hora.
    - Exibe o resultado no terminal, demonstrando o uso prático do modelo.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Ambiente de Análise:** Jupyter Notebook
- **Bibliotecas Principais:**
  - **Análise de Dados:** `pandas`, `openpyxl`
  - **Visualização:** `matplotlib`, `seaborn`
  - **Machine Learning:** `scikit-learn`, `xgboost`
  - **Persistência do Modelo:** `joblib`
  - **Coleta de Dados:** `requests`, `selenium` (para scripts de exemplo)

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar a análise em seu ambiente local.

### Pré-requisitos

- Python 3.10 ou superior
- Git

### Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_AQUI>
    cd <NOME_DA_SUA_PASTA_AQUI>
    ```

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    ```bash
    # Cria o ambiente
    python -m venv .venv

    # Ativa o ambiente (Windows)
    .\.venv\Scripts\activate
    ```

3.  **Instale as Dependências:**
    Todas as bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Obtenha os Dados:**
    - Baixe a base de dados anual do [IEMA](https://www.energiaeambiente.org.br/plataforma-qualidade-do-ar) e salve o arquivo na pasta `01_dados_brutos/`.

### Executando a Análise e o Treinamento

1.  **Inicie o Jupyter Notebook:**
    No terminal, a partir da pasta raiz do projeto, execute:
    ```bash
    jupyter notebook
    ```

2.  **Abra o Notebook:**
    No seu navegador, navegue até a pasta `03_notebooks/` e abra o arquivo `exploracao_inicial.ipynb`.

3.  **Execute as Células:**
    Execute as células em sequência. A maneira mais fácil é ir ao menu e clicar em **`Kernel > Restart & Run All`**. O notebook irá carregar os dados, limpá-los, gerar as análises e treinar o modelo de Machine Learning, salvando o resultado em `05_modelos/`.

### Executando uma Previsão

1.  **Configure a Chave de API:**
    - Obtenha uma chave de API gratuita no site da [IQAir](https://www.iqair.com/developer-hub).
    - Abra o arquivo `04_scripts/prever.py` e cole sua chave na variável `API_KEY`.

2.  **Execute o Script:**
    No terminal, a partir da pasta raiz do projeto, execute:
    ```bash
    python 04_scripts/prever.py
    ```
    O script irá carregar o modelo, buscar o dado mais recente e imprimir a previsão no terminal.
