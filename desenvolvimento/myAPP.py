from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDFillRoundFlatIconButton

from kivy.clock import Clock

from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


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
        self.screen = Builder.load_file("../integracao/interface/telaInicialTeste.kv")

    def build(self):
        # self.theme_cls.material_style = "M3"
        # self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"  # "Purple", "Red"

        textfields = [
            self.screen.ids.primary_voltage,
            self.screen.ids.secondary_voltage,
            self.screen.ids.secondary_power,
            self.screen.ids.frequency,
            self.screen.ids.blade_thickness
        ]

        for textfield in textfields:
            textfield.bind(
                on_text_validate=set_error_message
            )

        return self.screen


MainApp().run()
