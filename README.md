# Análise e Previsão da Qualidade do Ar com Machine Learning

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML-brightgreen.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-Boosting-blueviolet.svg)

## 📖 Descrição do Projeto

Este projeto acadêmico tem como objetivo desenvolver um pipeline completo de Data Science para coletar, organizar, analisar e prever a qualidade do ar em cidades brasileiras. A solução utiliza dados de fontes públicas, aplica técnicas de análise exploratória de dados (EDA) e treina um modelo de Machine Learning para prever a concentração de poluentes.

O projeto simula um cenário real, desde a coleta de dados brutos e inconsistentes, passando pela limpeza e transformação (ETL), até a criação de um modelo preditivo com **XGBoost**.

## ✨ Funcionalidades e Etapas

O projeto é dividido em um fluxo de trabalho claro, refletido na estrutura de pastas:

1.  **Coleta de Dados Automatizada:**
    - Script (`04_scripts/coleta_dados.py`) para coletar dados de fontes públicas como a API da CETESB (descontinuado por instabilidade) e o portal do IEMA.
    - Script (`04_scripts/coleta_iqair.py`) para consumir dados em tempo real da API da IQAir, simulando um sensor de IoT.

2.  **Limpeza e Pré-processamento:**
    - Notebook Jupyter (`03_notebooks/exploracao_inicial.ipynb`) que carrega os dados brutos.
    - Tratamento de cabeçalhos complexos, valores ausentes, tipos de dados inconsistentes e erros de codificação de caracteres (`latin1`).
    - Transformação dos dados de formato "longo" para "largo" (pivotagem), ideal para análise de séries temporais.

3.  **Análise Exploratória de Dados (EDA):**
    - Geração de gráficos de série temporal para visualizar a variação dos poluentes.
    - Cálculo e plotagem de médias móveis para identificar tendências.
    - Análise de correlação entre diferentes poluentes através de um mapa de calor (heatmap).
    - Estudo de padrões sazonais e semanais com gráficos de `boxplot`.

4.  **Engenharia de Features e Modelagem Preditiva:**
    - Criação de *features* baseadas no tempo (hora, dia da semana, mês) e *features* de lag (valores passados).
    - Treinamento de um modelo de regressão **XGBoost** para prever a concentração futura do poluente MP2.5.
    - Divisão cronológica dos dados em conjuntos de treino e teste, uma prática essencial para séries temporais.
    - Avaliação do modelo com métricas como MAE (Mean Absolute Error) e RMSE (Root Mean Squared Error).
    - Visualização da performance do modelo comparando os valores reais com as previsões.

5.  **Persistência do Modelo:**
    - O modelo treinado é salvo em um arquivo (`.pkl`) na pasta `05_modelos/` para uso futuro sem a necessidade de retreinamento.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Ambiente de Análise:** Jupyter Notebook
- **Bibliotecas Principais:**
  - **Análise de Dados:** `pandas`
  - **Visualização:** `matplotlib`, `seaborn`
  - **Machine Learning:** `scikit-learn`, `xgboost`
  - **Coleta de Dados:** `requests`, `selenium`
  - **Leitura de Arquivos:** `openpyxl`

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

    # Ativa o ambiente (macOS/Linux)
    # source .venv/bin/activate
    ```

3.  **Instale as Dependências:**
    Todas as bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Colete os Dados:**
    - **Opção A (Recomendado):** Baixe a base de dados anual do [IEMA](https://www.energiaeambiente.org.br/plataforma-qualidade-do-ar) e salve o arquivo `.csv` ou `.xlsx` na pasta `01_dados_brutos/`.
    - **Opção B (IoT):** Configure sua chave de API no arquivo `04_scripts/coleta_iqair.py` e execute-o (`python 04_scripts/coleta_iqair.py`) para coletar dados em tempo real.

### Executando a Análise

1.  **Inicie o Jupyter Notebook:**
    No terminal, a partir da pasta raiz do projeto, execute:
    ```bash
    jupyter notebook
    ```

2.  **Abra o Notebook:**
    No seu navegador, navegue até a pasta `03_notebooks/` e abra o arquivo `exploracao_inicial.ipynb`.

3.  **Execute as Células:**
    Execute as células em sequência. A maneira mais fácil é ir ao menu e clicar em **`Kernel > Restart & Run All`**. O notebook irá carregar os dados, limpá-los, gerar as análises e treinar o modelo de Machine Learning.

## 📁 Estrutura do Projeto

```
/qualidade_ar_projeto/
|
|-- 01_dados_brutos/          # Armazena os arquivos de dados originais (CSV, XLSX)
|-- 02_dados_processados/     # Armazena os dados após a limpeza e transformação
|-- 03_notebooks/             # Notebooks Jupyter para análise e experimentação
|-- 04_scripts/               # Scripts Python para tarefas automatizadas (coleta, etc.)
|-- 05_modelos/               # Arquivos dos modelos de ML treinados e salvos
|-- 06_relatorios/            # Gráficos, relatórios e saídas finais do projeto
|
|-- .gitignore                # Arquivos e pastas a serem ignorados pelo Git
|-- README.md                 # Este arquivo de documentação
|-- requirements.txt          # Lista de dependências Python do projeto
```
