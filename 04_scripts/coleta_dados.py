import requests
import pandas as pd
import os
from datetime import datetime, timedelta

def coletar_dados_cetesb_api(datas: list, id_estacao: int, nome_estacao: str, pasta_saida: str):
    """
    Coleta dados diretamente da API interna do site da CETESB.
    """
    url_api = "https://arcgis.cetesb.sp.gov.br/server/rest/services/QUALAR/CETESB_QUALAR/MapServer/1/query"
    
    for data_str in datas:
        print(f"Coletando dados para a data: {data_str} na estação: {nome_estacao}...")
        try:
            data_obj = datetime.strptime(data_str, '%d/%m/%Y')
            data_inicio_api = data_obj.strftime('%Y-%m-%d')
            data_fim_obj = data_obj + timedelta(days=1)
            data_fim_api = data_fim_obj.strftime('%Y-%m-%d')

            where_clause = f"EstacaoID = {id_estacao} AND data >= DATE '{data_inicio_api}' AND data < DATE '{data_fim_api}'"

            params = { 'where': where_clause, 'outFields': '*', 'returnGeometry': 'false', 'f': 'json' }
            
            response = requests.get(url_api, params=params)
            response.raise_for_status()
            
            dados_json = response.json()
            
            if 'features' in dados_json and dados_json['features']:
                dados_dia = dados_json['features'][0]['attributes']
                registros = []
                for hora in range(24):
                    hora_str = str(hora).zfill(2)
                    registro = {'Data': data_str, 'Hora': f"{hora_str}:00:00"}
                    
                    for poluente, nome_coluna in [
                        ('MP25', 'MP2,5'), ('MP10', 'MP10'), ('O3', 'O3'), 
                        ('NO2', 'NO2'), ('CO', 'CO'), ('SO2', 'SO2')
                    ]:
                        chave = f"h{hora_str}_{poluente}".upper()
                        if chave in dados_dia and dados_dia[chave] is not None:
                            registro[nome_coluna] = dados_dia[chave]
                    
                    registros.append(registro)
                
                df = pd.DataFrame(registros)
                
                nome_arquivo = f"dados_{nome_estacao.lower()}_{data_str.replace('/', '-')}.csv"
                caminho_completo = os.path.join(pasta_saida, nome_arquivo)
                df.to_csv(caminho_completo, index=False, sep=';', encoding='utf-8-sig')
                print(f"  -> Sucesso! Arquivo salvo em: {caminho_completo}")

            else:
                print(f"  -> Aviso: Nenhum dado retornado pela API para a data {data_str}.")

        except Exception as e:
            print(f"  -> ERRO ao processar a data {data_str}: {e}")
            
    print("\nColeta de dados finalizada.")


# --- CONFIGURAÇÃO E EXECUÇÃO ---
if __name__ == "__main__":
    # Vamos testar com datas de alguns meses atrás para garantir que os dados existem
    datas_para_coletar = [
        "15/05/2025",
        "16/05/2025",
    ]
    
    # --- ID CORRETO DA ESTAÇÃO ---
    id_estacao_alvo = 83
    nome_estacao_alvo = "Pinheiros"
    
    pasta_de_saida = os.path.join(os.path.dirname(__file__), '..', '01_dados_brutos')
    
    coletar_dados_cetesb_api(
        datas=datas_para_coletar, 
        id_estacao=id_estacao_alvo, 
        nome_estacao=nome_estacao_alvo, 
        pasta_saida=pasta_de_saida
    )