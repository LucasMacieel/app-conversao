import os

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from matplotlib import pyplot as plt
from kivy.core.window import Window

from integracao.definicoes.definicoes import TransformadorInformacoes
from integracao.modulos.functions import dimensionar_transformador, plot_corrente_mag


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


def exibir_informacoes(infos, fields):
    for index, textfield in enumerate(fields):
        info = infos[index]

        textfield.text = str(TransformadorInformacoes[info])


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tela_inicial = None
        self.dimensionamento = None
        self.ficha_tecnica = None
        self.corrente_magnetizacao = None
        self.tela_inicial_text_fields = None
        self.dimensionamento_text_fields = None
        self.ficha_tecnica_text_fields = None
        self.ficha_tecnica_info = ["peso_ferro", "peso_cobre", "peso_total", "perdas_ferro", "perdas_cobre",
                                   "rendimento"]
        self.dimensionamento_info = ["espiras_primario", "espiras_secundario", "cabo_AWG_primario",
                                     "cabo_AWG_secundario", "lamina", "quantidade_laminas", "peso_total",
                                     "dimensao_a", "dimensao_b"]
        self.screen = Builder.load_file("integracao/interface/main.kv")
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.plotar_grafico_mag
        )

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def change_screen(self, screen_name, back_effect):
        screen_manager = self.corrente_magnetizacao.ids.screen_manager
        screen_manager.current = screen_name

        if back_effect:
            screen_manager.transition.direction = 'right'
        else:
            screen_manager.transition.direction = 'left'

    def plotar_grafico_mag(self, path: str):
        """Plotar o gráfico da corrente de magnetização."""

        self.exit_manager()
        toast(path)

        try:
            espiras_primaria = TransformadorInformacoes["espiras_primario"]
            frequencia = float(self.tela_inicial.ids.frequency.text)
            tensao_primaria = float(self.tela_inicial.ids.primary_voltage.text)

            t, c = plot_corrente_mag(frequencia, espiras_primaria, tensao_primaria, path)

            fig, ax = plt.subplots()

            ax.plot(t, c)

            # Adiciona rótulos e título
            ax.set_xlabel('Im [A]')
            ax.set_ylabel('t [s]')
            ax.set_title('Corrente de Magnetização')

            # Adiciona grid
            ax.grid(True)

            screen1 = self.corrente_magnetizacao.ids.graph
            screen1.figure_wgt.figure = fig

        except Exception as e:
            mensagem_erro = ""
            if type(e).__name__ == "ValueError":
                mensagem_erro = "Verifique se todos os campos da Tela Inicial estão preenchidos."
            elif type(e).__name__ == "TypeError":
                mensagem_erro = f"Certifique-se de que o arquivo importado segue a estrutura recomendada."
            else:
                mensagem_erro = f"Debug: {e}"

            pop_up = MDDialog(title="Erro", text=mensagem_erro)
            pop_up.open()

    def abrir_arquivo_de_exemplo(self):
        # Substitua o caminho do arquivo de exemplo pelo caminho real do seu arquivo
        caminho_arquivo_exemplo = 'integracao/arquivo/MagCurve-1.txt'

        try:
            with open(caminho_arquivo_exemplo, 'r') as arquivo:
                conteudo = arquivo.read()

                pop_up = MDDialog(title="Arquivo Exemplo", text=conteudo)
                pop_up.open()

        except FileNotFoundError:
            print(f'O arquivo de exemplo não foi encontrado em: {caminho_arquivo_exemplo}')

    def executar_calculos(self):
        if self.verificar_campos():
            tensao_primaria = float(self.tela_inicial_text_fields[0].text)
            tensao_secundaria = float(self.tela_inicial_text_fields[1].text)
            potencia_secundaria = float(self.tela_inicial_text_fields[2].text)
            frequencia = float(self.tela_inicial_text_fields[3].text)
            espessura_lamina = float(self.tela_inicial_text_fields[4].text)

            result = dimensionar_transformador(tensao_primaria, tensao_secundaria, potencia_secundaria, frequencia,
                                               espessura_lamina)

            self.exibir_imagens_transformador()

            if not result:
                self.limpar_dados()
                toast("Os valores de entrada fornecidos não são adequados para dimensionar o transformador.")
            else:
                exibir_informacoes(self.dimensionamento_info, self.dimensionamento_text_fields)
                exibir_informacoes(self.ficha_tecnica_info, self.ficha_tecnica_text_fields)
        else:
            toast("Preencha todos os campos.")

    def exibir_imagens_transformador(self):
        box_images = self.dimensionamento.ids.box_transformer_images

        box_images.size_hint_y = None
        box_images.height = "200dp"
        box_images.spacing = "20dp"

        lamina = TransformadorInformacoes['lamina'].lower()
        self.dimensionamento.ids.imagem_transformador.source = "integracao/images/transformador.png"
        self.dimensionamento.ids.imagem_lamina.source = f"integracao/images/lamina_{lamina}.png"

    def verificar_campos(self):
        # Verificar se todos os campos estão preenchidos
        todos_preenchidos = []
        erros = []

        for text_input in self.tela_inicial_text_fields:
            todos_preenchidos.append(text_input.text)
            erros.append(text_input.error)

        # Ativar ou desativar o botão com base na condição
        return all(todos_preenchidos) and not any(erros)

    def limpar_dados(self):
        for textfield in self.dimensionamento_text_fields:
            textfield.text = "-"

        for textfield in self.ficha_tecnica_text_fields:
            textfield.text = "-"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        self.tela_inicial = self.screen.get_screen("telaInicial")
        self.dimensionamento = self.screen.get_screen("dimensionamento")
        self.ficha_tecnica = self.screen.get_screen("fichaTecnica")
        self.corrente_magnetizacao = self.screen.get_screen("correnteMagnetizacao")

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

        return self.screen


MainApp().run()
