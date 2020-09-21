#%%

def pagamentos(balancete_dir, relatorio_dir, balancete_name, relatorio_name, cod_conta):

    print('IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS...\n')

    import xlsxwriter
    import pandas as pd
    from utils import utilitarios

    # RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX

    print('IMPORTANDO AS TABELAS...\n')
    
    fornec = pd.read_csv(f'{balancete_dir}/{balancete_name}.csv', sep=";",encoding = 'iso-8859-1')
    fin = pd.read_csv(f'{relatorio_dir}/{relatorio_name}.csv', sep = ';', encoding = 'iso-8859-1')
    
    if '_coop' in balancete_name or '_rede' in balancete_name:
        
        utilitarios.teste_coop_rede(balancete_name, fin, fornec, cod_conta, relatorio_dir)
    
    else:
        
        utilitarios.manipulação(fin, cod_conta)
        utilitarios.preenche(fornec, fin)
        utilitarios.exporta(fin, relatorio_dir)
        utilitarios.resultados(fin)