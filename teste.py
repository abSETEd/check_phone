import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search
import tkinter as tk
from tkinter import filedialog



def carregar_planilha(arquivo):
    if arquivo.endswith('.cvs'):
        return pd.read_cvs(arquivo, dtype=str, keep_default_na=False)
    elif arquivo.endswith('.xlsx'):
        return pd.read_excel(arquivo, engine='openpyxl', dtype=str, keep_default_na=False)
    elif arquivo.endswith('.ods'):
        return pd.read_excel(arquivo, engine='odf', dtype=str, keep_default_na=False)
    else:
        raise ValueError("Formato de arquivo não suportado.")

#teste para saber se o codigo esta rodando corretamente
'''
arquivo_teste = "minha planilha.xlsx" #substitui pelo caminho real do arquivo
df = carregar_planilha(arquivo_teste)
print(df.head()) # exibe as primeiras linhas para verificar se ocorreu algum erro 
'''
def formatar_url(url):
    if not url.starswith("http"):
        return f"https://{url}"
    return url

def verificar_site(url): #verifica se o site está online.
    try: 
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def extrair_telefones(url): # extrair numeros de site validados
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.txt, 'html.perser')
        texto = soup.get_text()
        telefones = re.findall(r'\(?\d{2}\)?\s?\d{4,5}-\d{4}', texto)
        return ", ".join(set(telefones)) if telefones else "Não encontrado"
    except:
        return "Erro ao acessar o site."
    
'''
def buscar_site(razao_social):
    query = f"{razao_social} site oficial"
    try:
        for resultado in search(query, num=1, stop=1, pause=2):
            return resultado
    except:
        return "não encontrado"
'''
def processar_planilha(arquivo_entrada, arquivo_saida):
    df = carregar_planilha(arquivo_entrada)

    #ajusta a colunas para renover espaços e garantir que estejam no formato correto 
    df.columns = df.columns.str.strip().str.lower()

    if 'site'not in df.columns:
        raise ValueError(f"Colunas encontradas: {df.columns}. A planilha deve conter 'site'.")
    
    telefones = []
    for index, row in df.interrows():
        site = str(row['site']).strip()
        if verificar_site(site):
            telefone = extrair_telefones(site)
    else:
        "Não encontrado"
        telefones.append(telefone)


'''
def selecionar_arquivos():
    #Abre janelas para selecionar arquivo de entrada e definir local de saída.
    root = tk.Tk()
    root.withdraw()
    
    arquivo_entrada = filedialog.askopenfilename(title="Selecione a planilha de entrada", filetypes=[("Planilhas", "*.csv;*.xlsx;*.ods")])
    if not arquivo_entrada:
        print("Nenhum arquivo selecionado.")
        return
    
    arquivo_saida = filedialog.asksaveasfilename(title="Salvar planilha como", defaultextension=".xlsx", filetypes=[("Arquivo Excel", "*.xlsx")])
    if not arquivo_saida:
        print("Nenhum local de salvamento definido.")
        return
    
    processar_planilha(arquivo_entrada, arquivo_saida)

# Executar seleção de arquivos
selecionar_arquivos()
'''
def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Selecione a planilha", filetypes=[("Arquivos Excel", "*.xlsx;*.xls;*.ods")])

    print("Digite o nome do arquivo de saída (ou pressione Enter para usar o padrão):")
    nome_arquivo = input().strip()
    arquivo_saida = nome_arquivo if nome_arquivo else "planilha_filtrada.xlsx"

    print(f'Arquivo salvo como {arquivo_saida} com {sum(len(df) for df in planilhas_filtradas.values())} entradas únicas.')
    print(f"Baixe a planilha aqui: {arquivo_saida}")

# Chamando a função principal
remove_duplicates()
