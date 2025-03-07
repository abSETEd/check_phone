import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import openpyxl  # Para XLSX
import odf  # Para ODS com odfpy
import re  # Para expressões regulares
import os  # Pra manipular nomes de arquivo
import tkinter as tk  # Para a interface gráfica
from tkinter import filedialog  # Para selecionar arquivos

# Função para carregar a planilha em diferentes formatos
def carregador_planilha(caminho_arquivo):
    try:
        if caminho_arquivo.endswith('.csv'):
            df = pd.read_csv(caminho_arquivo)
        elif caminho_arquivo.endswith('.xlsx'):
            df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        elif caminho_arquivo.endswith('.ods'):
            df = pd.read_excel(caminho_arquivo, engine='odf')
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV, XLSX ou ODS.")
        
        colunas_esperadas = ["Site", "qtd CNPJs", "qtd UF MVX", "CNPJ", "CNPJRaiz", "RazaoSocial", "Logradouro",
                            "Numero", "Complemento", "Bairro", "Cidade", "Uf", "Cep", "CapitalSocial",
                            "Cnae", "CodigoPredio", "NaturezaJuridica", "DescNaturezaJuridica",
                            "Mailing", "SDR", "Data"]
        colunas_faltantes = [col for col in colunas_esperadas if col not in df.columns]
        if colunas_faltantes:
            raise ValueError(f"As colunas {colunas_faltantes} não foram encontradas na planilha.")
        
        # Formata a coluna 'Site' adicionando 'https://' se necessário
        df['Site'] = df['Site'].apply(lambda x: f"https://{x}" if not str(x).startswith(('http://', 'https://')) else x)

        return df
    except Exception as e:
        print(f"Erro ao carregar a planilha: {e}")
        return None

# Função para consultar o site e extrair telefones
def consultar_site(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, 'html.parser')
        texto = soup.get_text()

        padrao_telefone = r'(?:(?:\+?55\s?)?(?:\(?0?\d{2}\)?\s?)?\d{4,5}[-.\s]?\d{4})'
        telefones = re.findall(padrao_telefone, texto)
        telefones_unicos = list(set(telefones))
        if telefones_unicos:
            return ', '.join(telefones_unicos)
        else:
            return "Nenhum telefone encontrado."
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return "Erro na consulta"

# Função principal
def main():
    root = tk.Tk()
    root.withdraw()

    print("Por favor, selecione uma planilha (CSV, XLSX ou ODS): ")

    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione a planilha",
        filetypes=[("Arquivos suportados", "*.csv *.xlsx *.ods"), ("Todos os arquivos", "*.*")]
    )

    if not caminho_arquivo:
        print("Nenhum arquivo selecionado. Encerrando...")
        return
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo '{caminho_arquivo}' não encontrado. Encerrando...")
        return
    
    df_urls = carregador_planilha(caminho_arquivo)
    if df_urls is None:
        return
    
    print(f"Carreguei {len(df_urls)} linhas da planilha: {caminho_arquivo}")

    telefones = []
    for index, row in df_urls.iterrows():
        url = row['Site']
        print(f"\nConsultando: {url}")
        
        telefone = consultar_site(url)
        telefones.append(telefone)
        print(f"Telefones para {url}: {telefone}")

        time.sleep(2)

    # Primeiro, adiciona a coluna 'Telefone' ao DataFrame original
    df_urls['Telefone'] = telefones

    # Depois, reorganiza as colunas para inserir 'Telefone' entre 'RazaoSocial' e 'Logradouro'
    colunas_antes = df_urls.columns[:df_urls.columns.get_loc('RazaoSocial') + 1].tolist()
    colunas_depois = df_urls.columns[df_urls.columns.get_loc('Logradouro'):].tolist()
    novas_colunas = colunas_antes + ['Telefone'] + colunas_depois
    
    # Reorganiza o DataFrame com as novas colunas
    df_urls = df_urls[novas_colunas]

    # Solicita o nome do arquivo de saída apenas no final
    nome_saida = input(f"Digite o nome do arquivo de saída (ex.: novos_dados.csv) ou pressione Enter para '{os.path.splitext(caminho_arquivo)[0]}_com_telefones.csv': ") or f"{os.path.splitext(caminho_arquivo)[0]}_com_telefones.csv"
    df_urls.to_csv(nome_saida, index=False)
    
    print(f"Nova planilha salva em '{nome_saida}'.")

    # Fecha a janela do tkinter
    root.destroy()

if __name__ == "__main__":
    main()