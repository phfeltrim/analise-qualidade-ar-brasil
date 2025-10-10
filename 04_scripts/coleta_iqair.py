import requests
import pandas as pd
import os
from datetime import datetime
import time

# --- CONFIGURAÇÕES ---

# !! IMPORTANTE !! Cole aqui a sua chave da API que você obteve no site da IQAir
API_KEY = "df4e1aa3-4c2d-4d68-bc2e-923c29c1960e" # Mantenha sua chave correta aqui

# Cidade e estado que queremos pesquisar
CIDADE = "Sao Paulo"
ESTADO = "Sao Paulo"
PAIS = "Brazil"

# Pasta de saída para os dados
PASTA_SAIDA = os.path.join(os.path.dirname(__file__), '..', '01_dados_brutos')
NOME_ARQUIVO_SAIDA = f"dados_iqair_{CIDADE.lower()}_tempo_real.csv"
CAMINHO_COMPLETO = os.path.join(PASTA_SAIDA, NOME_ARQUIVO_SAIDA)

# --- FUNÇÃO DE COLETA ---

def coletar_dados_iqair_tempo_real(api_key, cidade, estado, pais):
    """
    Coleta os dados de qualidade do ar EM TEMPO REAL da API da IQAir.
    """
    print(f"Iniciando coleta de dados da IQAir para a cidade de {cidade}...")
    
    # --- CORREÇÃO: Usando o endpoint correto para o plano gratuito ---
    url = "http://api.airvisual.com/v2/city"
    
    params = {
        'city': cidade,
        'state': estado,
        'country': pais,
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        dados = response.json()
        
        if dados.get("status") == "success":
            print("  -> Sucesso! Dados em tempo real coletados.")
            current_data = dados["data"]["current"]
            
            # Extrai os dados de interesse
            nova_medicao = {
                'datetime': current_data['pollution']['ts'],
                'aqi_us': current_data['pollution']['aqius'],
                'poluente_principal_us': current_data['pollution']['mainus'],
                'temperatura': current_data['weather']['tp'],
                'umidade': current_data['weather']['hu'],
                'pressao': current_data['weather']['pr'],
                'vento_velocidade': current_data['weather']['ws'],
            }
            
            # Converte para DataFrame
            df_novo = pd.DataFrame([nova_medicao])
            df_novo['datetime'] = pd.to_datetime(df_novo['datetime'])

            # --- Lógica para adicionar ao arquivo existente ---
            # Se o arquivo já existe, lê os dados antigos e adiciona a nova linha
            if os.path.exists(CAMINHO_COMPLETO):
                print("  -> Arquivo existente encontrado. Adicionando nova medição...")
                df_antigo = pd.read_csv(CAMINHO_COMPLETO, sep=';')
                df_completo = pd.concat([df_antigo, df_novo], ignore_index=True)
            else:
                print("  -> Criando novo arquivo de dados...")
                df_completo = df_novo

            # Remove duplicatas e ordena pela data
            df_completo['datetime'] = pd.to_datetime(df_completo['datetime'])
            df_completo = df_completo.drop_duplicates(subset=['datetime'], keep='last')
            df_completo = df_completo.sort_values(by='datetime')
            
            # Salva o arquivo CSV completo
            df_completo.to_csv(CAMINHO_COMPLETO, index=False, sep=';', encoding='utf-8-sig')
            
            print(f"\nDados salvos/atualizados em: {CAMINHO_COMPLETO}")
            print("Última medição adicionada:")
            print(df_novo.to_string())

        else:
            print(f"  -> ERRO: A API retornou um status de falha: {dados.get('data', {}).get('message')}")

    except requests.exceptions.RequestException as e:
        print(f"  -> ERRO na requisição: {e}")
        print(f"   Resposta do servidor: {e.response.text if e.response else 'N/A'}")


# --- EXECUÇÃO DO SCRIPT ---
if __name__ == "__main__":
    if API_KEY == "SUA_CHAVE_DE_API_AQUI" or not API_KEY:
        print("ERRO: Por favor, insira sua chave de API da IQAir na variável API_KEY antes de executar.")
    else:
        coletar_dados_iqair_tempo_real(API_KEY, CIDADE, ESTADO, PAIS)
