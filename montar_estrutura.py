import os

# Nome do projeto
project_name = "qualidade_ar_projeto"

# Lista de pastas a serem criadas
folders = [
    "01_dados_brutos",
    "02_dados_processados",
    "03_notebooks",
    "04_scripts",
    "05_modelos",
    "06_relatorios"
]

# Lista de arquivos a serem criados
files = {
    "03_notebooks/exploracao_inicial.ipynb": "",
    "04_scripts/__init__.py": "",
    "04_scripts/coleta_dados.py": "# Script para coletar dados das fontes (CETESB, IQAir, etc.)",
    "04_scripts/limpeza_dados.py": "# Script para limpar e processar os dados brutos",
    "README.md": f"# Projeto de Análise de Qualidade do Ar: {project_name}\n\nDescrição do projeto...",
    "requirements.txt": "pandas\nmatplotlib\nopenpyxl\n# Adicione outras bibliotecas aqui",
    ".gitignore": "*.pyc\n__pycache__/\n.venv/\n.vscode/\n01_dados_brutos/\n02_dados_processados/\n"
}

# Cria as pastas
for folder in folders:
    try:
        os.makedirs(folder)
        # Cria um arquivo .gitkeep para que o Git reconheça pastas vazias
        with open(os.path.join(folder, ".gitkeep"), "w") as f:
            pass
        print(f"Pasta criada: {folder}/")
    except FileExistsError:
        print(f"Pasta já existe: {folder}/")

# Cria os arquivos
for filepath, content in files.items():
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Arquivo criado: {filepath}")
    except FileExistsError:
        print(f"Arquivo já existe: {filepath}")

print("\nEstrutura de pastas e arquivos criada com sucesso!")