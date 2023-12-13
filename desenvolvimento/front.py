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
                MDTextField:
                    hint_text: "Tensão Primária"
                    mode: "round"
                    max_text_length: 15
                    pos_hint: {"center_x": .5, "center_y": .8}
                    size_hint_x: .6

                MDTextField:
                    hint_text: "Tensão Secundária"
                    mode: "round"
                    max_text_length: 15
                    pos_hint: {"center_x": .5, "center_y": .7}
                    size_hint_x: .6

                MDTextField:
                    hint_text: "Potência Secundária"
                    mode: "round"
                    max_text_length: 15
                    pos_hint: {"center_x": .4, "center_y": .6}
                    size_hint_x: .4  

                MDTextField:
                    hint_text: ""
                    mode: "round"
                    max_text_length: 15
                    pos_hint: {"center_x": .7, "center_y": .6}
                    size_hint_x: .1

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
