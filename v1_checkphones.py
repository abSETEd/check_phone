import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search
import tkinter as tk
from tkinter import filedialog

def carregar_planilhas(arquivo):
    if arquivo.endswith('.csv'):
        return pd.read_csv(arquivo)
    elif arquivo.endswith('.xlsx'):
        return pd.read_excel(arquivo, engine='openpyxl')
    elif arquivo.endswith('.ods'):
        return pd.read_excel(arquivo, engine='odf')
    else: raise ValueError("Formato de arquivo não suportado.")
#parte do codigo que carrega a planilha

def verificar_site(url): #essa parte verifica se o site esta online
    try:
        resoponse = requests.get(url)
        return resoponse.status_code == 200
    except requests.exceptions.RequestException:
        return False
    
def extrair_telefones(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        texto = soup.get_text()
        telefones = re.findall(r'\(?\d{2}\)?\s?\d{4,5}-\d{4}', texto)
        return",".join(set(telefones)) if telefones else "Não encontrado"
    except:
        return "Erro ao acessar o site"
    
def buscar_site(razao_social): #busca um site relacionado a razao social no google
    query = f"{razao_social} site oficial"
    try:
        for resultado in search(query, num=1, stop=1, pause=2):
            return resultado
    except:
        return "Não encontrado"
def processar_planilha(arquivo_entrada, arquivo_saida): #processa a planilha verificando sites e extraindo telefones.
    df = carregar_planilhas(arquivo_entrada)
    if not any('site' in str(cell).lower() for cell in df.iloc[0]):
        # Verifica se 'razão social' está presente na primeira linha
        if not any('razão social' in str(cell).lower() for cell in df.iloc[0]):
            raise ValueError("Planilha não possui as colunas 'site' e 'razão social'.")
        else:
            coluna_razão_social = True
    else:
        coluna_razão_social = False
    
    telefones = []
    for index, row in df.iterrows():
        site = str(row['site']).strip() if 'site' in row else ''
    
        if coluna_razão_social and 'razão social' in row:  # Se for necessário buscar pela razão social
            site = buscar_site(row['razão social'])

        if verificar_site(site):
            telefone = extrair_telefones(site)
        else:
            telefone = "não encontrado"

        telefones.append(telefone)

    df['telefone extraído'] = telefones
    df.to_excel(arquivo_saida, index=False)
    print(f"Processo concluído. Planilha salva em {arquivo_saida}")
    df = carregar_planilhas(arquivo_entrada)

    if 'site' not in df.columns or 'razão social' not in df.columns:
        raise ValueError(" Planilha não possui as colunas 'site' e 'razão social'.")
    
    telefones = []
    for index, row in df.iterrows():
        site = str(row['site']).strip()
        if verificar_site(site):
            telefone = extrair_telefones(site)
        else:
            novo_site = buscar_site(row['razão social'])
            telefone = extrair_telefones(novo_site) if verificar_site (novo_site) else "Não encontrado"
            telefones.append(telefones)

    df['telefone extraído'] = telefones
    df.to_excel(arquivo_saida, index=False)
    print(f"Processo concluido. Planilha salva em {arquivo_saida}")

def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()

    arquivo_entrada = filedialog.askopenfilename(title="Selecione a planilha", filetypes=[("Planilhas", "*.csv;*.xlsx;*.ods")])
    if not arquivo_entrada: 
        print("Nenhum arquivo selecionadoç. Processo cancelado.")
        return
    
    arquivo_saida = filedialog.asksaveasfilename(title="Salvar planilha como", defaultextension=".xlsx",filetypes=[("Arquivo Excel", "*.xlsx")])
    if not arquivo_saida:
        print("nenhum local de salvamento definido.")
        return

    processar_planilha(arquivo_entrada, arquivo_saida)

selecionar_arquivo()

 




    