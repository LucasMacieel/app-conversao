import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import NavigationToolbar2Kivy, FigureCanvasKivyAgg
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.scrollview import MDScrollView
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.core.window import Window
import matplotlib.pyplot as plt
import os

# from integracao.definicoes.definicoes import TransformadorInformacoes
# from integracao.modulos.functions import dimensionar_transformador, plot_corrente_mag 

from lib.definicoes import TransformadorInformacoes
from lib.functions import dimensionar_transformador, plot_corrente_mag 

def set_error_message(instance_textfield):
    try:
        # Tenta converter o valor do input para um número
        float_value = float(instance_textfield.text)
    except ValueError:
        # Se a conversão falhar, significa que não é um número
        instance_textfield.error = True
        toast("Apenas números são aceitos")
    else:
        # Se a conversão for bem-sucedida, verifica se o número é maior que zero
        if float_value <= 0:
            # Se não for maior que zero, ativa o erro
            instance_textfield.error = True
            # Exibe a mensagem informando que o número deve ser maior que zero
            toast("O número deve ser maior que zero.")
        else:
            # Se for maior que zero, nenhum erro é ativado
            instance_textfield.error = False



class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tela_inicial = None
        self.ficha_tecnica = None
        self.corrente_magnetizacao = None
        # self.dimensionar_butao = None
        self.tela_inicial_text_fields = None
        self.ficha_tecnica_text_fields = None
        self.bx = None
        self.nav = None
        self.ficha_tecnica_info = ["peso_ferro", "peso_cobre", "peso_total", "perdas_ferro", "perdas_cobre",
                                   "rendimento"]
        self.dimensionamento_info = ["espiras_primario", "espiras_secundario", "cabo_AWG_primario", "cabo_AWG_secundario", "lamina",
                                   "quantidade_laminas", "peso_total", "dimensao_a", "dimensao_b"]
        self.screen = Builder.load_file("../integracao/interface/main.kv")
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.plotar_grafico_mag
        )
        #self.screen = Builder.load_file("../integracao/interface/main.kv")


    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def clear_graph_widgets(self):
        if self.bx and self.nav:
            self.bx.clear_widgets()
            self.bx = None
            self.nav = None


    def plotar_grafico_mag(self, path: str):
        '''Plotar o gráfico da corrente de magnetização.'''

        self.exit_manager()
        self.clear_graph_widgets()
        toast(path)
    
        try:

            espiras_primaria = TransformadorInformacoes["espiras_primario"]
            frequencia = float(self.tela_inicial.ids.frequency.text)
            tensao_primaria =  float(self.tela_inicial.ids.primary_voltage.text)

            #Valores utilizados para teste da funcionalidade
            #tensao_primaria = 230 * (2 ** 0.5)
            #frequencia = 60
            #espiras_primaria = 850

            t,c = plot_corrente_mag(frequencia, espiras_primaria, tensao_primaria, path) 

            plt.ylabel("Im [A]")
            plt.xlabel("t [s]")
            plt.plot(t, c)
            plt.grid()


            canvas = FigureCanvasKivyAgg(plt.gcf())
            self.bx = self.corrente_magnetizacao.ids.graph
            self.nav = NavigationToolbar2Kivy(canvas)

            self.bx.add_widget(self.nav.actionbar)
            self.bx.add_widget(canvas)

        except Exception as e:
            mensagem_erro = f"\n{type(e).__name__}, {str(e)}"
            content = MDLabel(text=mensagem_erro, halign='left', valign='top', markup=True, padding=(12, 10))
            pop_up = MDDialog(title="Erro", size_hint=(0.8, 0.4))
            pop_up.add_widget(content)
            pop_up.open()

            #toast("Verifique se os valores de frequência, número de espiras e tensão do primario foram setados")

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def select_path(self, path: str):
        self.exit_manager()
        self.plotar_grafico_cm(path)

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


    def executar_calculos(self):
        if self.verificar_campos():
            tensao_primaria = float(self.tela_inicial_text_fields[0].text)
            tensao_secundaria = float(self.tela_inicial_text_fields[1].text)
            potencia_secundaria = float(self.tela_inicial_text_fields[2].text)
            frequencia = float(self.tela_inicial_text_fields[3].text)
            espessura_lamina = float(self.tela_inicial_text_fields[4].text)

            result = dimensionar_transformador(tensao_primaria, tensao_secundaria, potencia_secundaria, frequencia,
                                               espessura_lamina)

            if not result:
                self.limpar_dados()
                toast("Os valores de entrada fornecidos não são adequados para dimensionar o transformador.")
            else:
                self.exibir_ficha_tecnica()
                self.exibir_detalhamento()
                self.exibir_dimensionamento()
        else:
            toast("Preencha todos os campos.")

    def exibir_dimensionamento(self):
        self.root.current = "dimensionamento"

        for index, textfield in enumerate(self.dimensionamento_text_fields):
            info = self.dimensionamento_info[index]
            textfield.text = str(TransformadorInformacoes[info])


    def verificar_campos(self):
        # Verificar se todos os campos estão preenchidos
        todos_preenchidos = []
        erros = []

        for text_input in self.tela_inicial_text_fields:
            todos_preenchidos.append(text_input.text)
            erros.append(text_input.error)

        # print("Preenchidos:", all(todos_preenchidos))
        # print("Corretos:", any(erros))

        # Ativar ou desativar o botão com base na condição
        return all(todos_preenchidos) and not any(erros)

    def exibir_detalhamento(self):
        # TODO: IMPLEMENTAR LOGICA PARA EXIBIR AS INFORMACOES DA TELA DE DETALHAMENTO
        pass

    def exibir_ficha_tecnica(self):
        for index, textfield in enumerate(self.ficha_tecnica_text_fields):
            info = self.ficha_tecnica_info[index]
            textfield.text = str(TransformadorInformacoes[info])

    def limpar_dados(self):
        # TODO: IMPLEMENTAR LOGICA PARA LIMPAR OS INFORMACOES DA TELA DE DETALHAMENTO

        for textfield in self.ficha_tecnica_text_fields:
            textfield.text = "-"

    def change_screen(self, screen_name):
        screen_manager = self.corrente_magnetizacao.ids.screen_manager
        screen_manager.current = screen_name


    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        self.tela_inicial = self.screen.get_screen("telaInicial")
        self.ficha_tecnica = self.screen.get_screen("fichaTecnica")
        self.corrente_magnetizacao = self.screen.get_screen("correnteMagnetizacao")
        self.dimensionamento = self.screen.get_screen("dimensionamento")
        # self.dimensionar_butao = self.tela_inicial.ids.dimensionar_button

        self.tela_inicial_text_fields = [
            self.tela_inicial.ids.primary_voltage,
            self.tela_inicial.ids.secondary_voltage,
            self.tela_inicial.ids.secondary_power,
            self.tela_inicial.ids.frequency,
            self.tela_inicial.ids.blade_thickness
        ]

        self.ficha_tecnica_text_fields = [
            self.ficha_tecnica.ids.peso_ferro,
            self.ficha_tecnica.ids.peso_cobre,
            self.ficha_tecnica.ids.peso_total,
            self.ficha_tecnica.ids.perda_ferro,
            self.ficha_tecnica.ids.perda_cobre,
            self.ficha_tecnica.ids.rendimento
        ]

        self.dimensionamento_text_fields = [
            self.dimensionamento.ids.espiras_primario,
            self.dimensionamento.ids.espiras_secundario,
            self.dimensionamento.ids.cabo_AWG_primario,
            self.dimensionamento.ids.cabo_AWG_secundario,
            self.dimensionamento.ids.lamina,
            self.dimensionamento.ids.quantidade_laminas,
            self.dimensionamento.ids.peso_total,
            self.dimensionamento.ids.dimensao_a,
            self.dimensionamento.ids.dimensao_b
        ]

        for textfield in self.tela_inicial_text_fields:
            textfield.bind(
                on_text_validate=set_error_message
            )

        # self.dimensionar_butao.bind(
        #     on_press=self.executar_calculos
        # )

        return self.screen


MainApp().run()
