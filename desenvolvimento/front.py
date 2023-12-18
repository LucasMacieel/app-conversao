style_app_kv = '''
<ContentNavigationDrawer>

    MDList:

        OneLineListItem:
            text: "Modelagem do transformador"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 1"

        OneLineListItem:
            text: "Corrente de Magnetização"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 2"


MDScreen:

    MDTopAppBar:
        pos_hint: {"top": 1}
        elevation: 4
        title: "MDNavigationDrawer"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager

            MDScreen:
                name: "scr 1"

                GridLayout:
                    cols: 2
                    spacing: "20dp"
                    padding: [dp(10), dp(150)]  # Ajuste o segundo valor conforme necessário
                    size_hint_x: 0.8  # Ajuste conforme necessário para controlar a largura
                    col_default_width: "150dp"  # Defina a largura padrão das colunas

                    MDTextField:
                        hint_text: "Tensão Primária"
                        mode: "round"
                        max_text_length: 15
                        size_hint_y: None
                        height: "30dp"

                    MDTextField:
                        hint_text: "Tensão Secundária"
                        mode: "round"
                        max_text_length: 15
                        size_hint_y: None
                        height: "30dp"

                    MDTextField:
                        hint_text: "Potência Secundária"
                        mode: "round"
                        max_text_length: 15
                        size_hint_y: None
                        height: "30dp"

                    MDTextField:
                        hint_text: "Frequência"
                        mode: "round"
                        max_text_length: 15
                        size_hint_y: None
                        height: "30dp"

                    MDRaisedButton:
                        text: "Iniciar Aplicação"
                        size_hint: (None, None)
                        size: ("150dp", "40dp")
                        on_press: app.start_application()  # Substitua 'app.start_application()' pela função real
                        col_span: 2

            MDScreen:
                name: "scr 2"

                MDLabel:
                    text: "Corre 2"
                    halign: "center"

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''
