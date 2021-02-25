#%%

import xlsxwriter
import pandas as pd
from utils import utilitarios
from kivy.logger import Logger

def pagamentos(balancete_dir, relatorio_dir, cod_conta):

    # RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX

    Logger.info('IMPORTANDO AS TABELAS...\n')
    
    fornec = pd.read_csv(f'{balancete_dir}', sep=";",encoding = 'iso-8859-1')
    fin = pd.read_csv(f'{relatorio_dir}', sep = ';', encoding = 'iso-8859-1')

    balancete_name = balancete_dir.split('\\')
    
    if '_coop' in balancete_name[-1] or '_rede' in balancete_name[-1]:
        
        Logger.info("Arquivo pertence ao grupo Rede/Coopideal")
        utilitarios.teste_coop_rede(balancete_name[-1], fin, fornec, cod_conta, relatorio_dir)
    
    else:
        
        Logger.info("Arquivo não pertence ao grupo Rede/Coopideal")
        utilitarios.manipulação(fin, cod_conta)
        utilitarios.preenche(fornec, fin)
        utilitarios.exporta(fin, relatorio_dir)
        utilitarios.resultados(fin)