#%%

def pagamentos(balancete_dir, relatorio_dir, cod_conta):

    print('IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS...\n')

    import xlsxwriter
    import pandas as pd
    from utils import utilitarios

    print(balancete_dir)

    # RODANDO TODO O PROCESSO DE MANIPULAÇÃO E PREENCHIMENTO DOS ARQUIVOS E EXPORTANDO NO FORMATO .XLSX


    print('IMPORTANDO AS TABELAS...\n')
    
    fornec = pd.read_csv(f'{balancete_dir}', sep=";",encoding = 'iso-8859-1')
    fin = pd.read_csv(f'{relatorio_dir}', sep = ';', encoding = 'iso-8859-1')

    balancete_name = balancete_dir.split('/')
    
    if '_coop' in balancete_name[-1] or '_rede' in balancete_name[-1]:
        
        utilitarios.teste_coop_rede(balancete_name[-1], fin, fornec, cod_conta, relatorio_dir)
    
    else:
        
        utilitarios.manipulação(fin, cod_conta)
        utilitarios.preenche(fornec, fin)
        utilitarios.exporta(fin, relatorio_dir)
        utilitarios.resultados(fin)