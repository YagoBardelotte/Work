import pandas as pd
import numpy as np

# IMPORT THE .CSV FILE, CLEANS THE USELESS COLUMNS, MODIFY AND ORGANIZE FOR DATE COLUMNS

# NOTE: REMEMBER TO IMPORT THE CSV FILE TO THE JUPYTER NOTEBOOK BEFORE RUN THE CODE!!!

df = pd.read_csv("Consulta_de_Pagamento_Fornecedor.csv", sep = ';', encoding = 'iso-8859-1', error_bad_lines = False)

df.drop(['Razão Social','Nome Banco','Agência','Data Entrada','Data Emissão','Valor Parcela','Valor Abatimento','Valor Documento',          'Valor Dedução','Data Vencimento','Data Pagamento','Valor Acréscimo','Selecionado',         "Conferido", "Exportado","Fornecedor","Parcela","Situação","Situação Bancária Boleto",          'N° Documento','N° Cheque','Tipo Pagamento'], axis = 1, inplace = True)

df["Data Pagto Contábil"] = df["Data Pagto Contábil"].str.slice(stop = 10)

df.fillna(np.nan)

df.sort_values(by = ["Data Pagto Contábil",'Loja','Conta'], inplace = True)

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

    deposito = df.loc[(df['Loja']) == ['DEPOSITO', 'WHAREOUSE']]
    loja_01 = df.loc[(df['Loja']) == 'LOJA 01']
    loja_03 = df.loc[(df['Loja']) == 'LOJA 03']
    loja_04 = df.loc[(df['Loja']) == 'LOJA 04']
    loja_05 = df.loc[(df['Loja']) == 'LOJA 05']
    loja_07 = df.loc[(df['Loja']) == 'LOJA 07']
    loja_08 = df.loc[(df['Loja']) == 'LOJA 08']
    loja_09 = df.loc[(df['Loja']) == 'LOJA 09']

    lojas = [deposito, loja_01, loja_03, loja_04, loja_05, loja_07, loja_08, loja_09]

    nomes = []
    
    for i in df.groupby('Loja').indices.keys():
        nomes.append(i)
  
    return(lojas,nomes)

# SEPARATE EACH DATAFRAME SAVED WITH prep_arq() FOR BANK ACCOUNT AND SAVE IN .XLSX FORMAT\n",

def export_excel(df,loja):
    
    # CHANGE THE 'VALOR LÍQUIDO' COLUMN FROM CHAR TO NUMERIC

    df['Valor Líquido'] = df['Valor Líquido'].apply(lambda x: float(x.replace('.','').replace(',','.')))

    # INPUT: DATAFRAME TO BE TREATED
    # OUTPUT: FILE SAVED IN XLSX SEPARATED FOR ACCOUNT\n",

    print('1ª STEP: To know what and how many accounts which has the store payments!\n\n\n')

    # CREATE A LIST WITH THE INFORMED DATAFRAME ACCOUNTS

    bco = []
    for x in df.groupby('Conta').indices.keys():
        bco.append(x)

    # NAME THE STORE FOR LATER USE

    print(f'Exist {len(bco)} accounts where they have payments from {loja}!\n\\n')

    print('2ª STEP: To create files to be cleaned and concatenate all in one work directory with many spreadsheets\n\n\n')

    # The function separa_contas() creates new df for each bank account and saves all in one single excel file\n",

    def separa_contas(loja,bco,df):
        
        with pd.ExcelWriter((f'{loja}.xlsx'), engine = 'xlsxwriter') as df_limpo:

            df.to_excel(df_limpo, sheet_name=(f'Pgtos{loja}'), index=False)            
            print('The first spreadsheet contains all the payments of all bank accounts!\n')

            "Prepares the df to fill the debit and credit columns\n",
 
            df['importação'] = 'importação'
            df['Data'] = df['Data Pagto Contábil']
            df['Valor'] = df['Valor Líquido']
            df['Debito'] = ''
            df['Credito'] = ''
            df['Historico'] = df['Tipo Entrada']
            df['Historico2'] = df['Observação']
            df.drop(['Data Pagto Contábil','Tipo Entrada','Observação','Loja','Valor Líquido','Banco'],axis = 1, inplace = True)

            # Separate the df

            for i in range(len(bco)):
                s = bco[i]
                print(f'A {i + 1}ª conta é:{s}')
                print(f'O nome da aba na planilha ficou: {s}_Pgto_{loja}\n')
                bco[i] = df.loc[(df['Conta']) == s]
                bco[i].drop(['Conta'],axis = 1, inplace = True)
                bco[i].to_excel(df_limpo, sheet_name = (f'{s}Pgto{loja}'), index = False)

            df.drop(['Conta'], axis = 1, inplace = True)
            df_limpo.save()

        print('File Saved!')

    separa_contas(loja,bco,df)

# Where everything happens...

df,lojas = prep_arq(df)
for i in range(len(df)):
    loja = lojas[i]
    export_excel(df[i],loja)


print('EUREKA! Your files are ready to use!')
print('========================================')