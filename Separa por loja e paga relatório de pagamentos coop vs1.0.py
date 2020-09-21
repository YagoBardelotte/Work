import pandas as pd
import numpy as np

# IMPORT THE .CSV FILE, CLEANS THE USELESS COLUMNS, MODIFY AND ORGANIZE FOR DATE COLUMNS

# NOTE: REMEMBER TO IMPORT THE CSV FILE TO THE JUPYTER NOTEBOOK BEFORE RUN THE CODE!!!

df = pd.read_csv("Consulta_de_Pagamento_Fornecedor.csv", sep = ';', encoding = 'iso-8859-1', error_bad_lines = False)


df.drop(['Nome Banco','Conta','Dias Atraso Entrada','Dias Atraso Vencimento','Agência','Data Entrada','Data Emissão',
         'Valor Parcela','Valor Abatimento','Valor Documento','Valor Dedução','Data Vencimento','Data Pagamento',
         'Valor Acréscimo',"Fornecedor","Parcela","Situação","Situação Bancária Boleto",'N° Documento','N° Cheque',
         'Tipo Pagamento','Banco'], axis = 1, inplace = True)

df["Data Pagto Contábil"] = df["Data Pagto Contábil"].str.slice(stop = 10)

df.fillna(np.nan)

df.sort_values(by = ["Data Pagto Contábil",'Loja'], inplace = True)

# FUNCTION TO SAVE THE SEPARATED DATAFRAMES IN XLSX

# NOTE: ISN'T BEING USED!!

# def export(df):

#     #INPUT: FILE NAME TO BE SAVED AND THE DATAFRAME
#     #OUTPUT: FILE IN .XLSX FORMAT

#     a=input()
#     with pd.ExcelWriter((f'{a}.xlsx'), engine = 'xlsxwriter') as df_limpo:
#         df.to_excel(df_limpo, sheet_name=(f'{a}'), index=False)
#         df_limpo.save()

# FUNCTION TO SEPARATE THE DATAFRAME FOR STORE AND RETURNS A LIST WITH THE NAME OF EACH\n",

def prep_arq(df):

    loja_03_rede = df.loc[(df['Loja']) == 'CB1 PORTO FELIZ']
    deposito_rede = df.loc[(df['Loja']) == 'CB6 DEPOSITO']
    loja_05_rede = df.loc[(df['Loja']) == 'CB2 CERQUILHO']
    loja_08_rede = df.loc[(df['Loja']) == 'CB3 PIRA 08']
    loja_01_coop = df.loc[(df['Loja']) == 'CI LOJA 01']
    loja_04_coop = df.loc[(df['Loja']) == 'CB3 PIRA 04']
    loja_05_coop = df.loc[(df['Loja']) == 'CI LOJA 05']
    loja_07_coop = df.loc[(df['Loja']) == 'CI LOJA 07']
    loja_08_coop = df.loc[(df['Loja']) == 'CI LOJA 08']
    loja_09_coop = df.loc[(df['Loja']) == 'CB5 INDAIA']
    
    lojas = [deposito_rede, loja_08_rede, loja_05_rede, loja_03_rede, 
             loja_01_coop, loja_04_coop, loja_05_coop, loja_07_coop, loja_08_coop, loja_09_coop]

    nomes = ['deposito_rede', 'loja_08_rede', 'loja_05_rede', 'loja_03_rede', 
             'loja_01_coop', 'loja_04_coop', 'loja_05_coop', 'loja_07_coop', 'loja_08_coop', 'loja_09_coop']

    return(lojas, nomes)

# ALGUMAS FUNÇÕES A SEREM UTILIZADAS

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

# LIMPA OS FORNECEDORES

fornecedor = fornecedor[:][11:-2]
fornecedor['codigo'] = fornecedor['Empresa:']
fornecedor['FORNECEDOR'] = fornecedor['Unnamed: 11']
lista = ['codigo','FORNECEDOR']
limpa(fornecedor, lista)

# SEPARATE EACH DATAFRAME SAVED WITH prep_arq() FOR BANK ACCOUNT AND SAVE IN .XLSX FORMAT\n",

def export_excel(df, loja, fornec, x):
    
    # CHANGE THE 'VALOR LÍQUIDO' COLUMN FROM CHAR TO NUMERIC

    df['Valor Líquido'] = df['Valor Líquido'].apply(lambda x: float(x.replace('.','').replace(',','.')))

    # INPUT: DATAFRAME TO BE TREATED
    # OUTPUT: FILE SAVED IN XLSX SEPARATED FOR STORE\n",

#     print('1ª STEP: To know what and how many store which has payments!\n\n\n')

    # CREATE A LIST WITH THE INFORMED DATAFRAME ACCOUNTS

#     bco = []
#     for x in df.groupby('Conta').indices.keys():
#         bco.append(x)

    # NAME THE STORE FOR LATER USE

#     print(f'Exist {len(bco)} accounts where they have payments from {loja}!\n')

    print('To create files to be cleaned and concatenate all in one work directory with many spreadsheets\n\n\n')

    # The function separa_contas() creates new df for each bank account and saves all in one single excel file\n",

    def separa_contas(df, loja, fornec, x):
        
        with pd.ExcelWriter((f'{loja}.xlsx'), engine = 'xlsxwriter') as df_limpo:

            print("Prepares the df to fill the debit and credit columns\n"),
            
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

    separa_contas(df, loja, fornec, x)

# Where everything happens...

print('MANIPULANDO O RELATÓRIO FINANCEIRO...\n')
df, lojas = prep_arq(df)

rede = 'Balancete_rede'
coop = 'Balancete_coop'

print('INSIRA A CONTA CONTÁBIL DE DUPLICATAS PAGAS A COMPENSAR:')
conta_duplics = int(input())


for i in range(len(df)):
    
    if lojas[i].endsWith('_rede'):
        fornecedor = pd.read_csv(f'{rede}.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')
    else:
        fornecedor = pd.read_csv(f'{coop}.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')
        
    export_excel(df[i], lojas[i], fornecedor, conta_duplics)

print('Files Saved!')


# EUREKA! Your files are ready to use!
# ========================================