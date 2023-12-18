from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast

from integracao.definicoes.definicoes import TransformadorInformacoes
from integracao.modulos.functions import dimensionar_transformador


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
        self.dimensionar_butao = None
        self.tela_inicial_text_fields = None
        self.ficha_tecnica_text_fields = None
        self.ficha_tecnica_info = ["peso_ferro", "peso_cobre", "peso_total", "perdas_ferro", "perdas_cobre",
                                   "rendimento"]
        self.screen = Builder.load_file("../integracao/interface/main.kv")

    def executar_calculos(self, instance_button):
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
        else:
            toast("Preencha todos os campos.")

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

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        self.tela_inicial = self.screen.get_screen("telaInicial")
        self.ficha_tecnica = self.screen.get_screen("fichaTecnica")
        self.dimensionar_butao = self.tela_inicial.ids.dimensionar_button

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

        for textfield in self.tela_inicial_text_fields:
            textfield.bind(
                on_text_validate=set_error_message
            )

        self.dimensionar_butao.bind(
            on_press=self.executar_calculos
        )

        return self.screen


MainApp().run()
