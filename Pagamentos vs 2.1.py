print('IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS...\n')

import xlsxwriter
import pandas as pd
import utils
import os

BASE_DIR = os.getcwd()
DATA_DIR = os.path.join( BASE_DIR, 'dados' )

# RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX

continuar = 'sim'

while True:
    
    if continuar.lower() == 'sim':

        print('Preencha o nome do arquivo com a lista de fornecedores:')
        print('Se for do grupo coopideal/rede local, especificar com _coop ou _rede no final.')
        balancete = input()
        print('\n')
        print('Preencha o nome do arquivo do relatório financeiro:')
        relatorio = input()
        print('\n')
        print('IMPORTANDO AS TABELAS...\n')
        
        fornec = pd.read_csv( f'{DATA_DIR}\\{balancete}.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')
        fin = pd.read_csv( f'{DATA_DIR}\\{relatorio}.csv', sep = ';', encoding = 'iso-8859-1', error_bad_lines = False)
        
        if '_coop' in balancete or '_rede' in balancete:

            print('MANIPULANDO O RELATÓRIO FINANCEIRO...\n')
            df, lojas = utils.prep_arq(fin)

            print('INSIRA A CONTA CONTÁBIL DE DUPLICATAS PAGAS A COMPENSAR:')
            conta_duplics = int(input())

            for i in range(len(df)):

                if lojas[i].endsWith('_rede'):
                    fornecedor = pd.read_csv(f'{balancete}.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')
                    
                else:
                    fornecedor = pd.read_csv(f'{balancete}.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')

                utils.separa_contas(df[i], lojas[i], fornecedor, conta_duplics)

            print('Arquivos salvos!')
            print('Mais arquivos? Sim/Não')
            continuar = input()
        
        else:
            
            utils.manipulação(fin)
            utils.preenche(fornec, fin)
            utils.exporta(fin)
            utils.resultados(fin)

            print('Arquivo(s) salvo(s)!')
            print('Mais arquivos? Sim/Não')
            continuar = input()
    
    elif continuar.lower() == 'não':
        break
    
    else:
        print('Comando incorreto! Por favor preencha Sim ou Não.\n')
        continuar = input()