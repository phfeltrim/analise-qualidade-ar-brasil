import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
import requests
import traceback

# --- CONFIGURAÇÕES ---
CAMINHO_MODELO = os.path.join(os.path.dirname(__file__), '..', '05_modelos', 'modelo_xgboost_mp25.pkl')
CAMINHO_DADOS_HISTORICOS = os.path.join(os.path.dirname(__file__), '..', '02_dados_processados', 'dados_limpos_wide.csv')

API_KEY = "df4e1aa3-4c2d-4d68-bc2e-923c29c1960e"
CIDADE = "Sao Paulo"
ESTADO = "Sao Paulo"
PAIS = "Brazil"
POLUENTE_ALVO = 'MP2.5'

# --- FUNÇÕES AUXILIARES ---

def buscar_dado_mais_recente(api_key, cidade, estado, pais):
    print("Buscando o dado de qualidade do ar mais recente...")
    url = "http://api.airvisual.com/v2/city"
    params = {'city': cidade, 'state': estado, 'country': pais, 'key': api_key}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        dados = response.json()
        
        if dados.get("status") == "success":
            print("  -> Dado mais recente coletado com sucesso!")
            medicao = dados["data"]["current"]["pollution"]
            
            return {
                'datetime': pd.to_datetime(medicao['ts']),
                POLUENTE_ALVO: medicao['aqius'], # Usando o índice AQI como valor
            }
        else:
            print(f"  -> ERRO na API: {dados.get('data', {}).get('message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"  -> ERRO na requisição: {e}")
        return None

def preparar_features(dado_novo, dados_historicos, colunas_do_modelo):
    """
    Cria as features de tempo, lag e junta com os outros poluentes
    para corresponder ao formato de treinamento do modelo.
    """
    print("Preparando features para a previsão...")
    df_novo = pd.DataFrame([dado_novo]).set_index('datetime')
    
    # Junta o dado novo com os dados históricos
    df_combinado = pd.concat([dados_historicos, df_novo])
    df_combinado = df_combinado.sort_index()

    # Preenche para frente quaisquer valores ausentes dos outros poluentes
    df_combinado = df_combinado.fillna(method='ffill')

    # Cria as features de tempo
    df_combinado['hora'] = df_combinado.index.hour
    df_combinado['dia_da_semana'] = df_combinado.index.dayofweek
    df_combinado['mes'] = df_combinado.index.month
    df_combinado['dia_do_ano'] = df_combinado.index.dayofyear

    # Cria as features de lag para o poluente alvo
    for i in range(1, 4):
        df_combinado[f'lag_{i}h'] = df_combinado[POLUENTE_ALVO].shift(i)

    # Cria a feature de média móvel
    df_combinado['media_movel_3h'] = df_combinado[POLUENTE_ALVO].shift(1).rolling(window=3).mean()
    
    # Pega apenas a última linha, que contém nosso ponto de dado mais recente
    features_finais = df_combinado.iloc[-1:]
    
    # Garante que temos todas as colunas que o modelo espera, na ordem correta
    features_finais = features_finais[colunas_do_modelo]

    print("  -> Features preparadas com sucesso.")
    return features_finais

# --- SCRIPT PRINCIPAL ---
if __name__ == "__main__":
    if not os.path.exists(CAMINHO_DADOS_HISTORICOS):
        pass
    else:
        try:
            modelo = joblib.load(CAMINHO_MODELO)
            print("  -> Modelo carregado com sucesso.")

            # Pega os nomes das features que o modelo foi treinado para usar
            colunas_do_modelo = modelo.get_booster().feature_names

            df_historico = pd.read_csv(CAMINHO_DADOS_HISTORICOS, index_col='datetime', parse_dates=True)
            df_historico.index = df_historico.index.tz_localize('UTC')
            df_historico = df_historico.last('7D') 
            
            dado_atual = buscar_dado_mais_recente(API_KEY, CIDADE, ESTADO, PAIS)

            if dado_atual:
                # Passa a lista de colunas para a função
                features_para_prever = preparar_features(dado_atual, df_historico, colunas_do_modelo)
                print("\nRealizando a previsão...")
                previsao = modelo.predict(features_para_prever)
                valor_previsto = previsao[0]
                
                hora_atual = features_para_prever.index[0]
                hora_previsao = hora_atual + timedelta(hours=1)

                print("\n--- PREVISÃO DA QUALIDADE DO AR ---")
                print(f"Última medição (Índice AQI às {hora_atual.strftime('%H:%M')}): {dado_atual[POLUENTE_ALVO]:.2f}")
                print(f"Previsão do Índice AQI para a próxima hora ({hora_previsao.strftime('%H:%M')}): {valor_previsto:.2f}")
                print("-------------------------------------")
        except Exception as e:
            print("\n--- OCORREU UM ERRO DURANTE A EXECUÇÃO ---")
            traceback.print_exc()