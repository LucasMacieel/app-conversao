# instalação
# pip install kivy
# Intalar o kivMD na página: https://kivymd.readthedocs.io/en/1.1.1/getting-started/

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from front import style_app_kv


# class ContentNavigationDrawer(MDScrollView):
#     screen_manager = ObjectProperty()
#     nav_drawer = ObjectProperty()
#
#
# class MyApp(MDApp):
#     # Window.size = (300, 600)
#
#     def build(self):
#         self.theme_cls.primary_palette = "Orange"
#         self.theme_cls.theme_style = "Dark"
#         return Builder.load_file("../integracao/interface/telaInicial.kv")
#
#
# MyApp().run()

from integracao.modulos.functions import calcular_secao_magnetica, encontrar_produto_mais_proximo, \
    calcular_perdas_ferro, calcular_peso_ferro, dimensionar_transformador
from integracao.definicoes.definicoes import Transformador, Lamina, AWG
from integracao.modulos.suporte import definir_dimensoes, arredondar_para_meio

# print(encontrar_produto_mais_proximo(60.75))
# print(definir_dimensoes(5, 5))
# print(encontrar_produto_mais_proximo(32))
# print(calcular_peso_ferro(Lamina.PADRONIZADA, 4, 5))
dimensionar_transformador(120, 220, 300, 60)
