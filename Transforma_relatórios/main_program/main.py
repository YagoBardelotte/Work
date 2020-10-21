# IMPORTAÇÕES DAS LIBS E FUNÇÕES UTILIZADAS

import kivy
kivy.require('1.11.1')

import warnings
warnings.filterwarnings('ignore')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from utils.Pagamentos import pagamentos
from tkinter import *
from tkinter import filedialog as dlg

# CARREGANDO ARQUIVO .KV COM ENCODING UTF-8

BASE_DIR = os.getcwd()
DESIGN = os.path.join(BASE_DIR + '\design.kv')

bld = Builder.load_string(open(DESIGN, encoding="utf-8").read(), rulesonly=True)

# CLASSES DA APLICAÇÃO

class Gerenciador(ScreenManager):
    pass

class Inicio(Screen):
    pass

class Principal(Screen):

    def get_path1(self):
        
        root = Tk()
        root.withdraw()
        opcoes = {'initialdir': '', 'title': 'Caminho para Balancete'}
        caminho = os.path.abspath(dlg.askopenfilename(**opcoes))
        filename = caminho.split('\\')
        self.ids.cam_balancete.text = caminho
        self.ids.nome_balancete.text = filename[-1]
    
    def get_path2(self):

        root = Tk()
        root.withdraw()
        opcoes = {'initialdir': '', 'title': 'Caminho para Relatório'}
        caminho = os.path.abspath(dlg.askopenfilename(**opcoes))
        filename = caminho.split('\\')
        self.ids.cam_relatorio.text = caminho
        self.ids.nome_relatorio.text = filename[-1]
    
    def iniciando(self):

        self.ids.mensagem.text = 'Processando...'


    def processamento(self):

        balancete_name = self.ids.nome_balancete.text
        balancete_dir = self.ids.cam_balancete.text
        relatorio_name = self.ids.nome_relatorio.text
        relatorio_dir = self.ids.cam_relatorio.text
        cod_conta = self.ids.conta.text
        
        if balancete_name == '' or balancete_dir == '' or relatorio_name == '' or relatorio_dir == '' or cod_conta == '':
            self.ids.mensagem.color = 1,0,0,1
            self.ids.mensagem.font_size = 15
            self.ids.mensagem.bold = True
            self.ids.mensagem.text = 'ATENÇÃO! TODOS OS CAMPOS SÃO DE PREENCHIMENTO OBRIGATÓRIO'

        else:            
            pagamentos(balancete_dir, relatorio_dir, cod_conta)
            self.ids.mensagem.text = "Arquivo salvo!"
        
    def limpeza(self):
        self.ids.cam_balancete.text = ''
        self.ids.cam_relatorio.text = ''
        self.ids.conta.text = ''
        self.ids.nome_balancete.text = ''
        self.ids.nome_relatorio.text = ''
        
class Ajuda(Screen):
    pass

class transformador(App):
    def build(self):
        self.title = 'Transformador de arquivos'
        bld
        return Gerenciador()

# RODANDO O APLICATIVO
if __name__ == '__main__':
    transformador().run()
