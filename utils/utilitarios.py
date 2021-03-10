# BIBLIOTECAS UTILIZADAS

from types import prepare_class
from numpy.core.numeric import NaN
import pandas as pd
import xlsxwriter
import os
import re
from kivy.logger import Logger

import warnings
warnings.filterwarnings('ignore')

#FUNÇÃO QUE RETIRA OS CARACTERES ESPECIAIS DOS NOMES DOS FORNECEDORES

def so_str(df):
    
    '''
    Função para deixar somente letras na Razão Social
    INPUT: RECEBE O DF
    OUTPUT: DF COM A RAZÃO SOCIAL LIMPA
    '''
    
    new = []
    tipo_emp = [' EIRELI', ' S.A.', ' SA', ' EPP', ' ME', ' LTDA']
    count=1
    for i in df:

        for j in tipo_emp:

            if type(i) != "string":
                pass
            elif j in i:
                i.replace(j,'')
        
        try:
            new.append(''.join(char for char in i if char not in ['.','-','/','\\','!']))

        except (TypeError, ValueError) as err:
            Logger.warning(f"{err}: Problemas na funcao de limpar a razao social")
            break
        
    return(pd.Series(new))

# FUNÇÃO QUE LIMPA AS COLUNAS NÃO UTILIZADAS PARA O ARQUIVO

def limpa(df,lista):
    
    '''
    Função para retirar as colunas não utilizadas
    
    INPUT: RECEBE O DF E A LISTA DE COLUNAS ESSENCIAIS
    OUTPUT: RETORNA O DF SOMENTE COM AS COLUNAS ESSENCIAIS
    '''
    try:
        for i in df:
            if i not in lista:
                df.drop([i], axis = 1, inplace = True)
        
        df.reset_index(drop = True, inplace = True)
        
    except Exception as err:
        Logger.warning(f"{err}: Problemas na funcao de retirar as colunas não utilizadas")


#FUNÇÃO QUE PREPARA O RELATÓRIO FINANCEIRO PARA PREENCHIMENTO DOS CAMPOS

def manipulação(fin, cod):

    '''
    Função para manipular o arquivo financeiro. 
    Limpeza, transforma dados, formata e cria novas colunas

    INPUT: DATAFRAME, DUPLICATAS CODE
    OUTPUT: CLEANED DATAFRAME
    '''
    
    Logger.info('MANIPULATE: MANIPULANDO O RELATORIO FINANCEIRO...\n')

    # EXCLUI COLUNAS NÃO UTLIZADAS E PREENCHE VALORES VAZIOS

    colunas = fin.columns

    for i in colunas:
        match = re.match('Data ', i)
        if match == True and i not in ["Data Entrada", "Data Emissão", "Data Vencimento", "Data Pagto Contábil"]:
            fin['Data Pagamento'] = fin[i]
            fin.drop(i, axis=1, inplace=True)
            break

    lista = ['Razão Social','Valor Líquido', 'Valor Parcela', 'Valor Abatimento', 'Valor Acréscimo', 'Data Pagamento', 'Observação','Nome Banco','Tipo Entrada', 'Banco']

    limpa(fin, lista)
    fin.fillna('', inplace = True)

    # TRANSFORMA OS VALORES DE STRING PARA FLOAT

    fun = lambda x: float(x.replace(".","").replace(",","."))

    try:
        fin["Valor Líquido"] = fin["Valor Líquido"].apply(fun)
    except [ValueError, KeyError] as err:
        Logger.warning(f"MANIPULATE: {err} ao formatar a coluna 'Valor Liquido'! Talvez ela nao exista no arquivo")
        fin["Valor Parcela"] = fin["Valor Parcela"].apply(fun)
        pass
    
    try:
        fin["Valor Abatimento"] = fin["Valor Abatimento"].apply(fun)
        fin["Valor Acréscimo"] = fin["Valor Acréscimo"].apply(fun)
    except Exception as err:
        Logger.warning(f"MANIPULATE: {err} ao formatar a coluna 'Valor abatimento' e/ou 'Valor Acrescimo'! Talvez ela(s) nao exista(m) no arquivo")
        pass

    # RETIRA DA DATA O DIA DA SEMANA E SUBSTITUI A COLUNA NÃO FORMATADA

    fin["Data Pagamento"] = fin["Data Pagamento"].str.slice(stop = 10)
    fin.sort_values(by = ['Razão Social'], inplace = True)
    fin.reset_index(drop = True, inplace = True)

    # CRIA COLUNAS DE DÉBITO E CRÉDITO E PREENCHE COM A CONTA DE DUPLICATAS A COMPENSAR

    fin['DEBITO'] = ""
    fin['CREDITO'] = ""

    Logger.info('MANIPULATE: INSERINDO A CONTA CONTABIL DE DUPLICATAS PAGAS A COMPENSAR:')
    x = int(cod)

    try:
        for i in range(len(fin['Nome Banco'])):
            if fin['Nome Banco'][i] not in ['CAIXA LETICIA','DANIELA','CAIXA GERENCIAL','COFRE', 'LIVRO CAIXA - ARCAL']:
                fin['CREDITO'][i] = x
            else:
                fin['CREDITO'][i] = 5
    except KeyError as err:
        Logger.warning(f"MANIPULATE: {err} ao buscar a coluna 'Nome Banco'. Talvez ela nao exista no arquivo.")
        fin['CREDITO'] = x

#FUNÇÃO QUE PREENCHE O RELATÓRIO FINANCEIRO COM OS CÓDIGOS DOS FORNECEDORES

def preenche(fornec, fin):

    '''
    Ajusta o arquivo dos fornecedores e preenche as colunas de débito com os respectivos códigos.
    Limpa os fornecedores, transforma algumas colunas para retirar os caracteres especiais,
    organiza em ordem alfabetica, preenche o relatório financeiro, retira linhas inválidas.

    INPUT: DATAFRAMES (PROVIDER AND FINANCIAL FILE)
    OUTPUT: FINANCIAL FILE FILLED
    '''
    
    Logger.info('FILLING: PREENCHENDO O RELATORIO FINANCEIRO COM AS CONTAS DOS FORNECEDORES... \n')
    
    # LIMPA OS FORNECEDORES

    if fornec['Empresa:'][3] == 'CONSOLIDADO': # PARA EMPRESAS COM MATRIZ E FILIAIS NO MESMO RELATÓRIO
        fornec = fornec[:][12:-2] # RETIRA AS LINHAS NÃO UTILIZADAS
    else:
        fornec = fornec[:][11:-2]

    fornec['codigo'] = fornec['Empresa:'] # CRIA UMA NOVA COLUNA COM OS CÓDIGOS DOS FORNECEDORES
    fornec['FORNECEDOR'] = fornec['Unnamed: 11'] # CRIA UMA NOVA COLUNA COM OS NOMES DOS FORNECEDORES

    lista = ['codigo','FORNECEDOR']
    Logger.info("FILLING: LIMPANDO LISTA DE FORNECEDORES")
    limpa(fornec, lista)
    
    # TRANSFORMA A COLUNA RAZÃO SOCIAL E FORNECEDOR EM UMA LISTA CADA E LIMPA OS CARACTERES ESPECIAIS

    razao1 = fin['Razão Social'].to_list()
    Logger.info("FILLING: FORMATANDO RAZAO SOCIAL DO FINANCEIRO")
    fin['Razão Social'] = so_str(razao1)

    razao = fornec['FORNECEDOR'].to_list()
    Logger.info("FILLING: FORMATANDO RAZAO SOCIAL DO BALANCETE")
    fornec['FORNECEDOR'] = so_str(razao)

    # ORGANIZA POR ORDEM ALFABÉTICA E TRANSFORMA EM DICIONÁRIO

    fornec.sort_values(by = ['FORNECEDOR'], inplace = True)
    fornec.reset_index(drop = True, inplace = True)
    fornec.dropna(inplace = True)
    dic = fornec.set_index('FORNECEDOR').T.to_dict('list')

    # PREENCHE O DF DE ACORDO COM A TABELA DE FORNECEDORES
    
    lista = ['BRADESCO SA','BANCO COOPERATIVO SICRED SA','CAIXA ECONOMICA FEDERAL SA',
             'COMPANHIA PAULSTA DE FORCA ELUZ CPFL','VR BENEF E SERV DE PROCESSAMENTO LTDA',
             'BANCO DO BRASIL SA','MINISTERIO DA FAZENDA','SUPERMERCADO UNION',
             'COOPIDEAL SUPERMERCADOS EIRELI','REDE LOCAL']

    for i in range(len(fin['Razão Social'])):
        if fin['Razão Social'][i] in dic and fin['Razão Social'][i] not in lista:
            fin['DEBITO'][i] = dic[fin['Razão Social'][i]][0]

    fin.sort_values(by=['Razão Social'], inplace = True)

    # LIMPA AS LINHAS QUE NÃO VÃO SER PREENCHIDAS POIS NÃO SÃO FORNECEDORES VÁLIDOS

    fin.reset_index(drop = True, inplace = True)

    for i in range(len(fin['Razão Social'])):

        if fin['Razão Social'][i] in lista:
            fin.drop(i, inplace = True)

# FUNCTION TO SEPARATE THE DATAFRAME FOR STORE AND RETURNS A LIST WITH THE NAME OF EACH ONE

def prep_arq(df, balancete_name):

    '''
    Prepara os arquivos referente às empresas Coopideal e Rede Local para fazer todo o processo de manipulação.
    '''

    if balancete_name.endswith('_coop.csv'):

        CI_LOJA_01_coop = df.loc[(df['Loja']) == 'CI LOJA 01']
        # CI_LOJA_04_coop = df.loc[(df['Loja']) == 'CI LOJA 04']
        # CI_LOJA_05_coop = df.loc[(df['Loja']) == 'CI LOJA 05']
        # CI_LOJA_07_coop = df.loc[(df['Loja']) == 'CI LOJA 07']
        # CI_LOJA_08_coop = df.loc[(df['Loja']) == 'CI LOJA 08']
        # CI_LOJA_09_coop = df.loc[(df['Loja']) == 'CI LOJA 09']

        lojas = [CI_LOJA_01_coop] #CI_LOJA_04_coop, CI_LOJA_05_coop, CI_LOJA_07_coop, CI_LOJA_08_coop, CI_LOJA_09_coop]

        nomes = ['CI_LOJA_01_coop'] # 'CI_LOJA_04_coop', 'CI_LOJA_05_coop', 'CI_LOJA_07_coop', 'CI_LOJA_08_coop', 'CI_LOJA_09_coop']

        return(lojas, nomes)

    elif balancete_name.endswith('_rede.csv'):

        CB01_PORTO_FELIZ_rede = df.loc[(df['Loja']) == 'CB01 PORTO FELIZ']
        CB02_DEPOSITO_rede = df.loc[(df['Loja']) == 'CB02 DEPOSITO']
        CB03_CERQUILHO_rede = df.loc[(df['Loja']) == 'CB03 CERQUILHO']
        CB04_PIRA_01_ST_rede = df.loc[(df['Loja']) == 'CB04 PIRA 01 ST']
        CB05_INDAIATUBA_rede = df.loc[(df['Loja']) == 'CB05 INDAIATUBA']
        CB06_PIRA_02_MD_rede = df.loc[(df['Loja']) == 'CB06 PIRA 02 MD']
        CB07_TIETE_rede = df.loc[(df['Loja']) == 'CB07 TIETE']
        CB08_LARANJAL_rede = df.loc[(df['Loja']) == 'CB08 LARANJAL']
        CB09_LEME_rede = df.loc[(df['Loja']) == 'CB09 LEME']

        lojas = [CB01_PORTO_FELIZ_rede, CB02_DEPOSITO_rede, CB03_CERQUILHO_rede, CB04_PIRA_01_ST_rede, 
                CB05_INDAIATUBA_rede, CB06_PIRA_02_MD_rede, CB07_TIETE_rede, CB08_LARANJAL_rede, 
                CB09_LEME_rede]

        nomes = ['CB01_PORTO_FELIZ_rede', 'CB02_DEPOSITO_rede', 'CB03_CERQUILHO_rede', 'CB04_PIRA_01_ST_rede', 
                'CB05_INDAIATUBA_rede', 'CB06_PIRA_02_MD_rede', 'CB07_TIETE_rede', 'CB08_LARANJAL_rede', 
                'CB09_LEME_rede']

        return(lojas, nomes)
    
    else:
        return False

# TESTA SE O BALANCETE É DA REDE OU DA COOP

def teste_coop_rede(balancete_name, fin, fornec, cod_conta, relatorio_dir):

    '''
    Verifica de qual empresa o arquivo com os fornecedores se refere.
    '''
    
    Logger.info('COOP_REDE: MANIPULANDO O RELATÓRIO FINANCEIRO...\n')
    df, lojas = prep_arq(fin, balancete_name)

    Logger.info('COOP_REDE: INSERINDO A CONTA CONTÁBIL DE DUPLICATAS PAGAS A COMPENSAR:')
    conta_duplics = int(cod_conta)

    for i in range(len(lojas)):

        separa_contas(df[i], lojas[i], fornec, conta_duplics, relatorio_dir)

# SEPARATE EACH DATAFRAME SAVED WITH prep_arq() FUNCTION AND SAVE IN .XLSX FORMAT

def separa_contas(df, loja, fornec, x, relatorio_dir):

    '''
    Separa, manipula e salva os arquivos referentes ao grupo Rede/Coopideal organizados e preenchidos
    com as contas de fornecedor.
    '''
    
    # CRIA UM ARQUIVO XLSX PARA CADA LOJA

    path = os.path.dirname(relatorio_dir)

    with pd.ExcelWriter((f'{path}/Pgto_{loja}.xlsx'), engine = 'xlsxwriter', date_format='DD-MM-YYYY') as df_limpo: # pylint: disable=abstract-class-instantiated

        Logger.info("COOP_REDE: PREPARANDO O DF PARA PREENCHER AS COLUNAS DE CRÉDITO E DÉBITO...\n")
        
        #FORMATA OS VALORES QUE SERÃO UTILIZADOS

        df['Valor Líquido'] = df['Valor Líquido'].apply(lambda x: float(x.replace('.','').replace(',','.')))
        df['Valor Abatimento'] = df['Valor Abatimento'].apply(lambda x: float(x.replace('.','').replace(',','.')))
        df['Valor Acréscimo'] = df['Valor Acréscimo'].apply(lambda x: float(x.replace('.','').replace(',','.')))

        df.fillna('', inplace = True) # PREENCHE TODOS OS CAMPOS QUE NÃO TEM NENHUM CARACTER COM VAZIO
        
        df.sort_values(by = ['Razão Social'], inplace = True) #ORGANIZA PELA RAZÃO SOCIAL
        
        # CRIANDO AS COLUNAS

        df['Loja'] = df['Loja']
        df['importação'] = 'importação'
        df['Data'] = df['Data Pagto Contábil']
        df['Valor'] = df['Valor Líquido']
        df['Juros'] = df['Valor Acréscimo']
        df['Descontos'] = df['Valor Abatimento']
        df['Debito'] = '' # SERÁ PREENCHIDO COM O CÓDIGO FORNECIDO PELO BALANCETE
        df['Credito'] = x # SERÁ PREENCHIDO COM O CÓDIGO FORNECIDO PELO USUÁRIO
        df['Historico'] = df['Razão Social']
        df['Historico2'] = df['Tipo Entrada']
        df['Historico3'] = df['Observação']
        
        #RETIRA O DIA DA SEMANA DA DATA
        
        df["Data"] = df["Data"].str.slice(stop = 10)
        df.reset_index(drop = True, inplace = True)

        # LIMPA O ARQUIVO DO BALANCETE

        if fornec['Empresa:'][3] == 'CONSOLIDADO':
            fornec = fornec[:][12:-2] # RETIRA AS LINHAS NÃO UTILIZADAS
        else:
            fornec = fornec[:][11:-2]

        fornec['codigo'] = fornec['Empresa:'] # CRIA UMA NOVA COLUNA COM OS CÓDIGOS DOS FORNECEDORES
        fornec['FORNECEDOR'] = fornec['Unnamed: 11'] #CRIA UMA NOVA COLUNA COM OS NOMES DOS FORNECEDORES
        
        # LIMPA O BALANCETE MANTENDO APENAS AS DUAS COLUNAS CRIADAS
        lista = ['codigo','FORNECEDOR']
        limpa(fornec, lista)

        # TRANSFORMA A COLUNA RAZÃO SOCIAL E FORNECEDOR EM UMA LISTA CADA E LIMPA OS CARACTERES ESPECIAIS

        razao1 = df['Razão Social'].to_list()
        df['Razão Social'] = so_str(razao1)

        razao = fornec['FORNECEDOR'].to_list()
        fornec['FORNECEDOR'] = so_str(razao)

        # ORGANIZA O BALANCETE POR ORDEM ALFABÉTICA E TRANSFORMA EM DICIONÁRIO

        fornec.sort_values(by = ['FORNECEDOR'], inplace = True)
        fornec.reset_index(drop = True, inplace = True)
        fornec.dropna(inplace = True)
        dic = fornec.set_index('FORNECEDOR').T.to_dict('list')

        Logger.info(f'COOP_REDE: PREENCHENDO O RELATORIO FINANCEIRO DA LOJA {loja} COM AS CONTAS DOS FORNECEDORES... \n')

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
        
        #LIMPA O RELATÓRIO FINANCEIRO MANTENDO SOMENTE AS COLUNAS ESSENCIAIS
        
        lista = ['importação','Data','Valor','Juros','Descontos','Debito','Credito','Nome Banco','Historico','Historico2','Historico3']
        limpa(df,lista)
        
        #SALVA O RELATÓRIO FINANCEIRO
        
        Logger.info(f"COOP_REDE: O nome da tabela e Pgto_{loja}\n")
        df.to_excel(df_limpo, sheet_name = (f'Pgto_{loja}'), index = False)
        df_limpo.save()
    Logger.info(f"COOP_REDE: Arquivos salvos com sucesso!\n")

# FUNÇÃO QUE MOSTRA O RESULTADO DO PREENCHIMENTO (QUANTAS LINHAS SEM CÓDIGO DE FORNECEDOR 
# E O VALOR TOTAL DOS PAGAMENTOS)

def resultados(fin):

    # MOSTRA QUAIS FORNECEDORES FICARAM SEM PREENCHIMENTO

    forn_sem_conta = []

    fin.reset_index(inplace = True)

    for i in range(len(fin['DEBITO'])):
        if fin['DEBITO'][i] == '':
            forn_sem_conta.append(fin['Razão Social'][i])

    Logger.info(f"RESULTADOS: Fornecedores sem contas: {set(forn_sem_conta)} \n")

    # SOMA O TOTAL DE PAGAMENTOS REALIZADOS AOS FORNECEDORES

    soma = 0
    try:
        for i in range(len(fin['Tipo Entrada'])):

            if fin['Tipo Entrada'][i] in ['COMERCIALIZACAO E REVENDA', 'COMPRA DE MERCADORIAS', 
                                        'COMPRA DE MERCADORIAS P/ PRODUCAO INTERNA']:
                soma += fin['Valor Líquido'][i]
        soma = round(soma, 2)

        Logger.info(f'RESULTADOS: Total de pagamentos realizados no mes: R$ {soma} \n')

    except KeyError as err:
        Logger.warning(f'{err}: Não ha a coluna de Tipo Entrada para realizar a soma do total de pagamentos das compras!\n')

    # MOSTRA QUANTAS LINHAS FICARAM SEM PREENCHIMENTO

    soma = 0
    
    for i in range(len(fin['DEBITO'])):
        if fin['DEBITO'][i] == '':
            soma +=1

    Logger.info(f'RESULTADOS: Total de linhas sem preenchimento: {soma} \n')
    Logger.info(f'RESULTADOS: Total de fornecedores sem preenchimento: {len(set(forn_sem_conta))}\n')

# FUNÇÃO QUE EXPORTA O RELATÓRIO FINANCEIRO PRONTO

def exporta(fin, data_dir):
    
    # EXPORTAR PARA NOVO ARQUIVO

    path = os.path.dirname(data_dir)

    fin_limpo = pd.ExcelWriter(f'{path}/arq_limpo.xlsx', engine = 'xlsxwriter') # pylint: disable=abstract-class-instantiated
    fin.to_excel(fin_limpo, index = False,  float_format="%.2f")
    fin_limpo.save()
    Logger.info("Arquivo salvo com sucesso!\n")