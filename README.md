# check_phone
Esse projeto ele sera especifico para uma revalidação de planilhas. visando ajudar a automatizar processos de pesquisas 
este inclusive é o repositorio oficial com o codigo que, ate agora, foi o que funcionou. 

nas primeira versão o codigo faz as seguintes instruções

Versão Base: Até o ponto em que rodou bem e padronizou os sites com "https://".

Objetivo:
Ler uma planilha (CSV, XLSX ou ODS) com uma coluna chamada "Site", adicionar "https://" às URLs quando necessário, consultar os sites e extrair informações (inicialmente texto genérico, depois telefones).

Funcionalidades Implementadas:
 1. Suporte a Múltiplos Formatos de Planilha:
 - Bibliotecas:
   - pandas pra CSV e XLSX.
   - openpyxl pra XLSX.
   - pyexcel_ods3 pra ODS (instalado via !pip install pyexcel-ods3 no Colab).
 - Implementação: Função carregar_planilha detecta o formato pelo nome do arquivo e carrega os dados em um DataFrame.
 - Exemplo:
    - Arquivo sites.csv, sites.xlsx ou sites.ods com coluna "Site".
    
 2. Interface de Upload no Google Colab:
  - Biblioteca: google.colab.files.
  - Implementação: Usa files.upload() pra abrir um seletor de arquivos, permitindo ao usuário subir a planilha diretamente no Colab.
  - Saída: O arquivo enviado é processado em memória com io.BytesIO.
    
 3. Padronização de URLs:
  - Onde: Função carregar_planilha.
  - Lógica: Adiciona "https://" às URLs da coluna "Site" se não começarem com "http://" ou "https://".

Código:
python 
df['Site'] = df['Site'].apply(lambda x: f"https://{x}" if not str(x).startswith(('http://', 'https://')) else x)

- Exemplo:
  - Entrada: "exemplo.com.br" -> Saída:"https://Exemplo.com.br".
  - Entrada: "http://outro.com" -> Saída: "https://outro.com' (mantido)

4. Consulta Básica Aos Sites:
  - Função: consultar_site.
  - Implementação:
    - usa requests.get com cabeçalho User_Agent para simular um navegador.
    - Extrai o texto da página com BeautifulSoup e retorna os primeiros 100 caracteres como exemplo
  - Erro: Se falahar (ex.: site fora do ar), retorna "erro na consulta"

 5. Extração de Telefones:
  - Evolução: Após a versão inicial do texto generico, ajustei o codigo para buscar os telefones.
  - Padrão: r'(?:(?:\+?55\s?)?(?:\(?\d{2}\)?)?\s?\d{4,5}[-.\s]?\d{4})'.
  - Formatos reconhecidos:
      - (11) 99999-9999
      - +5511987654321
      - 11 98765-4321
  - Saida: Lista de telefones únicos, juntados com virgula no resultado final.
 6. Saída em csv
  - Arquivo: resultado_telefones.csv.
  - Colunas: "site" (URL formatada) e "Telefone" (telefones encontrados ou " Nenhum telefone encontrado").
  - Implementação: Usa pandas.DataFrame.to_csv

 7. Controle de Requisição?
  - Paisa: time.sleep(2) entre consultas para evitar bloqueios por parte dos sites.
   
 8. Estrutura da planilha de Entrada:
   - coluna site:
       - A coluna Site precisa estar exatamente escrita com o " S " maiusculo para que a leitura do cdigo seja realizada. caso não esteja nesse padrão o programa retornara um erro e dizer que nao foi encontrada a coluna site;
        

 - Fluxo do Código:
   - Usuário faz upload da planilha via interface.
   - Código verifica o formato e carrega os dados.
   - URLs são padronizadas com "https://".
   - Cada site é consultado, telefones são extraídos.
   - Resultados são salvos em CSV.

 - Resultado Final:
   - Arquivo: resultados_telefones.csv.
   - Exemplo:
     -  Site,Telefone
       - https://exemplo.com.br,"(11) 99999-9999"
       - https://exemplo.com,"Nenhum telefone encontrado"



**Resumo das Etapas de Implementação:
 - Início: Suporte básico a CSV com upload manual e texto genérico.
 - Evolução 1: Adicionado suporte a XLSX e ODS.
 - Evolução 2: Interface de upload com files.upload().
 - Evolução 3: Padronização de URLs com "https://".
 - Evolução 4: Extração de telefones com regex em vez de texto genérico**

# Codigo teste 
checkwgmaps_tester.ipynb
Este arquivo refere-se a implemnentação de pesquisa com o google maps. 
ainda não foi solucionado a parte que o codigo pega o numero pela pesquina no google maps, a consulta é feita mas não vem resultados.
Estudando um pouco mais com videos e outros programas parecidos,


------------------------------------------------------------------------------------------------------------------------------------------

Futuras implementações e possiveis melhorias no codigo:

  - Implementar a leitura de outras formas de pesquisa de telefone como o Google Maps
  - Baixar o arquivo em varios formatos. - feito
  - interface grafica para facilitar o usuario utilizar o programa
  - leitura mais rapida e/ou esconder o processo pra não ficar tão extenso no terminal 
  
