import xlsxwriter
import pandas as pd
from utils import utilitarios
from kivy.logger import Logger

def pagamentos(balancete_dir, relatorio_dir, cod_conta):

    '''
    Função que ativa todo o processo de manipulação, preenchimento e exportação do relatório financeiro

    INPUT: PATH DOS ARQUIVOS DO BALANCETE E RELATORIO E O CODIGO DA CONTA DE DUPLICATAS
    OUTPUT: ARQUIVO SALVO PREENCHIDO NO MESMO PATH DO RELATORIO 
    '''

    # RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX

    Logger.info('IMPORTANDO AS TABELAS...\n')
    
    fornec = pd.read_csv(f'{balancete_dir}', sep=";",encoding = 'iso-8859-1')
    fin = pd.read_csv(f'{relatorio_dir}', sep = ';', encoding = 'iso-8859-1')

    cnpj = fornec[fornec.columns[5]][0].split('/')

    if cnpj[0] not in ['04.962.644','06.227.913']:
    
        Logger.info("Arquivo não pertence ao grupo Rede/Coopideal")
        utilitarios.manipulação(fin, cod_conta)
        utilitarios.preenche(fornec, fin)
        utilitarios.exporta(fin, relatorio_dir)
        utilitarios.resultados(fin)
    
    else:
        Logger.error('ERRO: ARQUIVO INCORRETO! TROCAR DE ABA')

def pagamentos_coop_rede(balancete_name, balancete_dir, relatorio_dir, cod_conta):

    '''
    SOMENTE PARA COOPIDEAL E REDE LOCAL

    Função que ativa todo o processo de manipulação, preenchimento e exportação do relatório financeiro

    INPUT: PATH DOS ARQUIVOS DO BALANCETE E RELATORIO E O CODIGO DA CONTA DE DUPLICATAS
    OUTPUT: ARQUIVO SALVO PREENCHIDO NO MESMO PATH DO RELATORIO 
    '''
    
    # RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX

    Logger.info('IMPORTANDO AS TABELAS...\n')
    
    fornec = pd.read_csv(f'{balancete_dir}', sep=";",encoding = 'iso-8859-1')
    fin = pd.read_csv(f'{relatorio_dir}', sep = ';', encoding = 'iso-8859-1')

    utilitarios.teste_coop_rede(balancete_name, fin, fornec, cod_conta, relatorio_dir)