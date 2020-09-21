def pagamentos(balancete_dir, relatorio_dir, balancete_name, relatorio_name, cod_conta):

    print('IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS...\n')

    import xlsxwriter
    import pandas as pd
    from utils import utilitarios
    import os

    print(balancete_dir, balancete_name, relatorio_dir, relatorio_name, cod_conta)

    # RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX

    print('IMPORTANDO AS TABELAS...\n')
    
    fornec = pd.read_csv(f'{balancete_dir}\\{balancete_name}.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')
    fin = pd.read_csv(f'{relatorio_dir}\\{relatorio_name}.csv', sep = ';', encoding = 'iso-8859-1', error_bad_lines = False)
    
    if '_coop' in balancete_name or '_rede' in balancete_name:

        print('MANIPULANDO O RELATÓRIO FINANCEIRO...\n')
        df, lojas = utilitarios.prep_arq(fin)

        print('INSERINDO A CONTA CONTÁBIL DE DUPLICATAS PAGAS A COMPENSAR:')
        conta_duplics = int(cod_conta)

        for i in range(len(df)):

            if lojas[i].endsWith('_rede'):
                fornecedor = pd.read_csv(f'{balancete_dir}\\{balancete_name}.csv.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')
                
            else:
                fornecedor = pd.read_csv(f'{relatorio_dir}\\{relatorio_name}.csv', encoding = 'iso-8859-1', error_bad_lines = False, sep = ';')

            utilitarios.separa_contas(df[i], lojas[i], fornecedor, conta_duplics)
    
    else:
        
        utilitarios.manipulação(fin)
        utilitarios.preenche(fornec, fin)
        utilitarios.exporta(fin, relatorio_dir)
        utilitarios.resultados(fin)