#%%

import xlsxwriter
import pandas as pd
from utils import utilitarios
import logging
from datetime import date
logging.basicConfig(filename=f"log_{date.today().strftime('%d-%m-%Y')}.log", 
                    filemode='a', 
                    encoding="utf-8", 
                    level=logging.DEBUG, 
                    format= "%(asctime)s :: %(funcName)s :: %(levelno)s :: %(lineno)d")

def pagamentos(balancete_dir, relatorio_dir, cod_conta):

    # RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX

    logging.warning('IMPORTANDO AS TABELAS...\n')
    
    fornec = pd.read_csv(f'{balancete_dir}', sep=";",encoding = 'iso-8859-1')
    fin = pd.read_csv(f'{relatorio_dir}', sep = ';', encoding = 'iso-8859-1')

    balancete_name = balancete_dir.split('\\')
    
    if '_coop' in balancete_name[-1] or '_rede' in balancete_name[-1]:
        
        logging.warning("Arquivo pertence ao grupo Rede/Coopideal")
        utilitarios.teste_coop_rede(balancete_name[-1], fin, fornec, cod_conta, relatorio_dir)
    
    else:
        
        logging.warning("Arquivo não pertence ao grupo Rede/Coopideal")
        utilitarios.manipulação(fin, cod_conta)
        utilitarios.preenche(fornec, fin)
        utilitarios.exporta(fin, relatorio_dir)
        utilitarios.resultados(fin)