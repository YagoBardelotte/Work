import pandas as pd
import xlsxwriter
import numpy as np
import re

def so_str(df):
    
    '''
    Função para deixar somente letras na Razão Social
    INPUT: RECEBE O DF
    OUTPUT: DF COM A RAZÃO SOCIAL LIMPA
    '''
    
    new = []
    for i in df:
        
        try:
            new.append(''.join(char for char in i if char not in ['.','-','/','\\','!']))
        except (TypeError, ValueError):
            pass
        
    return(pd.Series(new))


def limpa(df,lista):
    
    '''
    Função para retirar as colunas não utilizadas
    
    INPUT: RECEBE O DF E A LISTA DE COLUNAS ESSENCIAIS
    OUTPUT: RETORNA O DF SOMENTE COM AS COLUNAS ESSENCIAIS
    '''
    
    for i in df:
        if i not in lista:
            df.drop([i], axis = 1, inplace = True)
    
    df.reset_index(drop = True, inplace = True)


def manipulação(fin, cod):
    
    print('MANIPULANDO O RELATÓRIO FINANCEIRO...\n')

    # EXCLUI COLUNAS NÃO UTLIZADAS E PREENCHE VALORES VAZIOS

    colunas = fin.columns

    if 'Data Pagamento' in colunas:

        x = 'Data Pagamento'
        lista = ['Razão Social','Valor Líquido', x,'Observação','Nome Banco','Tipo Entrada', 'Banco']
        
        fin[x] = fin[x].str.slice(stop = 10)
        fin.sort_values(by = ['Razão Social'], inplace = True)
        fin.reset_index(drop = True, inplace = True)

    elif 'Data Vencimento' in colunas:

        x = 'Data Vencimento'
        lista = ['Razão Social','Valor Líquido', x,'Observação','Nome Banco','Tipo Entrada', 'Banco']

        fin[x] = fin[x].str.slice(stop = 10)
        fin.sort_values(by = ['Razão Social'], inplace = True)
        fin.reset_index(drop = True, inplace = True)


    limpa(fin, lista)
    fin["Observação"].fillna('', inplace = True)
    fin.dropna(inplace = True)

    # TRANSFORMA OS VALORES DE STRING PARA FLOAT

    fun = lambda x: float(x.replace(".","").replace(",","."))
    fin["Valor Líquido"] = fin["Valor Líquido"].apply(fun)

    # RETIRA DA DATA O DIA DA SEMANA E SUBSTITUI A COLUNA NÃO FORMATADA

    fin["Data Pagamento"] = fin["Data Pagamento"].str.slice(stop = 10)
    fin.sort_values(by = ['Razão Social'], inplace = True)
    fin.reset_index(drop = True, inplace = True)

    # CRIA COLUNAS DE DÉBITO E CRÉDITO E PREENCHE COM A CONTA DE DUPLICATAS A COMPENSAR

    fin['DEBITO'] = ""
    fin['CREDITO'] = ''

    print('INSERINDO A CONTA CONTÁBIL DE DUPLICATAS PAGAS A COMPENSAR:')
    x = int(cod)
    print('\n')
    
    for i in range(len(fin['Nome Banco'])):
        if fin['Nome Banco'][i] not in ['CAIXA LETICIA','DANIELA','CAIXA GERENCIAL','COFRE']:
            fin['CREDITO'][i] = x
        else:
            fin['CREDITO'][i] = 5

def preenche(fornec, fin):
    
    print('PREENCHENDO O RELATÓRIO FINANCEIRO COM AS CONTAS DOS FORNECEDORES... \n')
    
    # LIMPA OS FORNECEDORES

    fornec = fornec[:][11:-2]
    fornec['codigo'] = fornec['Empresa:']
    fornec['FORNECEDOR'] = fornec['Unnamed: 11']
    lista = ['codigo','FORNECEDOR']
    limpa(fornec, lista)
    
    # TRANSFORMA A COLUNA RAZÃO SOCIAL E FORNECEDOR EM UMA LISTA CADA E LIMPA OS CARACTERES ESPECIAIS

    razao1 = fin['Razão Social'].to_list()
    fin['Razão Social'] = so_str(razao1)

    razao = fornec['FORNECEDOR'].to_list()
    fornec['FORNECEDOR'] = so_str(razao)

    # ORGANIZA POR ORDEM ALFABÉTICA E TRANSFORMA EM DICIONÁRIO

    fornec.sort_values(by = ['FORNECEDOR'], inplace = True)
    fornec.reset_index(drop = True, inplace = True)
    fornec.dropna(inplace = True)
    dic = fornec.set_index('FORNECEDOR').T.to_dict('list')

    # PREENCHE O DF DE ACORDO COM A TABELA DE FORNECEDORES
    
    lista = ['BRADESCO SA','BANCO COOPERATIVO SICRED SA','CAIXA ECONOMICA FEDERAL SA',
             'COMPANHIA PAULSTA DE FORCA ELUZ CPFL','VR BENEF E SERV DE PROCESSAMENTO LTDA',
             'ARCAL SUPERMERCADO LTDA','ARCAL RESCISAO E PROCESSOS','ARLINDO CALSA FILHO',
             'BANCO DO BRASIL SA','MINISTERIO DA FAZENDA','SUPERMERCADO UNION',
             'COOPIDEAL SUPERMERCADOS EIRELI','REDE LOCAL']
    
    fin.reset_index(drop = True, inplace = True)

    for i in range(len(fin['Razão Social'])):
        if fin['Razão Social'][i] in dic and fin['Razão Social'][i] not in lista:
            fin['DEBITO'][i] = dic[fin['Razão Social'][i]][0]

    fin.sort_values(by=['Razão Social'], inplace = True)

    # LIMPA AS LINHAS QUE NÃO VÃO SER PREENCHIDAS POIS NÃO SÃO FORNECEDORES VÁLIDOS

    fin.reset_index(drop = True, inplace = True)

    for i in range(len(fin['Razão Social'])):

        if fin['Razão Social'][i] in lista:
            fin.drop(i, inplace = True)

# FUNCTION TO SEPARATE THE DATAFRAME FOR STORE AND RETURNS A LIST WITH THE NAME OF EACH\n",

def prep_arq(df):

    CB01_PORTO_FELIZ_rede = df.loc[(df['Loja']) == 'CB01 PORTO FELIZ']
    CB02_DEPOSITO_rede = df.loc[(df['Loja']) == 'CB02 DEPOSITO']
    CB03_CERQUILHO_rede = df.loc[(df['Loja']) == 'CB03 CERQUILHO']
    CB04_PIRA_01_ST_rede = df.loc[(df['Loja']) == 'CB04 PIRA 01 ST']
    CB05_INDAIATUBA_rede = df.loc[(df['Loja']) == 'CB05 INDAIATUBA']
    CB06_PIRA_02_MD_rede = df.loc[(df['Loja']) == 'CB06 PIRA 02 MD']
    CI_LOJA_01_coop = df.loc[(df['Loja']) == 'CI LOJA 01']
    CI_LOJA_04_coop = df.loc[(df['Loja']) == 'CI LOJA 04']
    CI_LOJA_05_coop = df.loc[(df['Loja']) == 'CI LOJA 05']
    CI_LOJA_07_coop = df.loc[(df['Loja']) == 'CI LOJA 07']
    CI_LOJA_08_coop = df.loc[(df['Loja']) == 'CI LOJA 08']
    CI_LOJA_09_coop = df.loc[(df['Loja']) == 'CI LOJA 09']

    lojas = [CB01_PORTO_FELIZ_rede,CB02_DEPOSITO_rede,CB03_CERQUILHO_rede,CB04_PIRA_01_ST_rede,CB05_INDAIATUBA_rede,
        CB06_PIRA_02_MD_rede,CI_LOJA_01_coop,CI_LOJA_04_coop,CI_LOJA_05_coop,CI_LOJA_07_coop,CI_LOJA_08_coop,CI_LOJA_09_coop]

    nomes = ['CB01_PORTO_FELIZ_rede','CB02_DEPOSITO_rede','CB03_CERQUILHO_rede','CB04_PIRA_01_ST_rede','CB05_INDAIATUBA_rede',
        'CB06_PIRA_02_MD_rede','CI_LOJA_01_coop','CI_LOJA_04_coop','CI_LOJA_05_coop','CI_LOJA_07_coop','CI_LOJA_08_coop','CI_LOJA_09_coop']

    return(lojas, nomes)

# SEPARATE EACH DATAFRAME SAVED WITH prep_arq() FOR BANK ACCOUNT AND SAVE IN .XLSX FORMAT\n",

def separa_contas(df, loja, fornec, x):

    with pd.ExcelWriter((f'{loja}.xlsx'), engine = 'xlsxwriter') as df_limpo: # pylint: disable=abstract-class-instantiated

        print("Prepares the df to fill the debit and credit columns\n")

        df['Valor Líquido'] = df['Valor Líquido'].apply(lambda x: float(x.replace('.','').replace(',','.')))

        df["Observação"].fillna('', inplace = True)
        df.dropna(inplace = True)

        df.sort_values(by = ['Razão Social'], inplace = True)
        df.reset_index(drop = True, inplace = True)

        # Creating columns

        df['Loja'] = df['Loja']
        df['importação'] = 'importação'
        df['Data'] = df['Data Pagto Contábil']
        df['Valor'] = df['Valor Líquido']
        df['Debito'] = '' # Will be fullfiled with provider code
        df['Credito'] = x
        df['Historico'] = df['Razão Social']
        df['Historico2'] = df['Tipo Entrada']
        df['Historico3'] = df['Observação']

        # TRANSFORMA A COLUNA RAZÃO SOCIAL E FORNECEDOR EM UMA LISTA CADA E LIMPA OS CARACTERES ESPECIAIS

        razao1 = df['Razão Social'].to_list()
        df['Razão Social'] = so_str(razao1)

        razao = fornec['FORNECEDOR'].to_list()
        fornec['FORNECEDOR'] = so_str(razao)

        # ORGANIZA POR ORDEM ALFABÉTICA E TRANSFORMA EM DICIONÁRIO

        fornec.sort_values(by = ['FORNECEDOR'], inplace = True)
        fornec.reset_index(drop = True, inplace = True)
        fornec.dropna(inplace = True)
        dic = fornec.set_index('FORNECEDOR').T.to_dict('list')

        print(f'PREENCHENDO O RELATÓRIO FINANCEIRO DA LOJA {loja} COM AS CONTAS DOS FORNECEDORES... \n')

        # PREENCHE O DF DE ACORDO COM A TABELA DE FORNECEDORES

        df.reset_index(drop = True, inplace = True)

        for i in range(len(df['Razão Social'])):
            if df['Razão Social'][i] in dic:
                df['Debito'][i] = dic[df['Razão Social'][i]][0]

        df.sort_values(by=['Razão Social'], inplace = True)

        # LIMPA AS LINHAS QUE NÃO VÃO SER PREENCHIDAS POIS NÃO SÃO FORNECEDORES VÁLIDOS

        df.reset_index(drop = True, inplace = True)

        lista = ['BANCO BRADESCO S/A.','BANCO COOPERATIVO SICRED SA','CAIXA ECONOMICA FEDERAL SA',
                'BANCO DO BRASIL SA','BANCO ITAU S/A','BANCO SAFRA S/A','BANCO SANTANDER S/A','BANCO TOPAZIO S.A.',
                'BANCO TRIANGULO S/A','CAIXA ECONOMICA FEDERAL-NOIVA DA COLINA']

        for i in range(len(df['Historico'])):

            if df['Historico'][i] in lista:
                df.drop(i, inplace = True)

        df.drop(['Data Pagto Contábil','Tipo Entrada','Observação',
                 'Valor Líquido','Razão Social', 'Loja'],axis = 1, inplace = True) 

        # Separate the df by bank account

#             for i in range(len(bco)):
#                 s = bco[i]
#                 print(f'A {i + 1}ª conta é:{s}')
#                 print(f'O nome da aba na planilha ficou: {s}_Pgto_{loja}\n')
#                 bco[i] = df.loc[(df['Conta']) == s]
#                 bco[i].drop(['Conta'],axis = 1, inplace = True)
#                 bco[i].to_excel(df_limpo, sheet_name = (f'{s}Pgto{loja}'), index = False)

        print(f"The tab's name in the spredsheet is: Pgto_{loja}\n")
        df.to_excel(df_limpo, sheet_name = (f'Pgto_{loja}'), index = False)
        df_limpo.save()

def resultados(fin):
    
    print('FORNECEDORES SEM PREENCHIMENTO: \n')

    # MOSTRA QUAIS FORNECEDORES FICARAM SEM PREENCHIMENTO

    forn_sem_conta = []

    fin.reset_index(inplace = True)

    for i in range(len(fin['DEBITO'])):
        if fin['DEBITO'][i] == '':
            forn_sem_conta.append(fin['Razão Social'][i])

    print(set(forn_sem_conta),'\n')

    # SOMA O TOTAL DE PAGAMENTOS REALIZADOS AOS FORNECEDORES

    soma = 0

    for i in range(len(fin['Tipo Entrada'])):

        if fin['Tipo Entrada'][i] in ['COMERCIALIZACAO E REVENDA', 'COMPRA DE MERCADORIAS', 
                                      'COMPRA DE MERCADORIAS P/ PRODUCAO INTERNA']:
            soma += fin['Valor Líquido'][i]

    print('Total de pagamentos realizados no mês: R$ %.2f'%(soma),'\n')

    # MOSTRA QUANTAS LINHAS FICARAM SEM PREENCHIMENTO

    soma = 0
    for i in range(len(fin['DEBITO'])):
        if fin['DEBITO'][i] == '':
            soma +=1

    print(f'Total de linhas sem preenchimento: {soma}\n\nTotal de fornecedores sem preenchimento: {len(set(forn_sem_conta))}\n')


# Fazer um pacote e criar funções dos processos da transformação

# Tem que ter um arquivo __init__.py
# Fazer o pacote e subir no Github todos os arquivos

# Tentar capturar os erros

def exporta(fin, data_dir):
    
    # EXPORTAR PARA NOVO ARQUIVO

    # fin.drop('index', axis = 1, inplace = True)

    fin_limpo = pd.ExcelWriter(f'{data_dir}\\arq_limpo.xlsx', engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    fin.to_excel(fin_limpo, index = False,  float_format="%.2f")
    fin_limpo.save()