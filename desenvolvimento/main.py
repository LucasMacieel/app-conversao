#instalação
#pip install kivy
#Intalar o kivMD na página: https://kivymd.readthedocs.io/en/1.1.1/getting-started/

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from front import style_app_kv


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MyApp(MDApp):
    #Window.size = (300, 600)

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(style_app_kv)


MyApp().run()