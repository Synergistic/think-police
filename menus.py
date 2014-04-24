__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from transition import change_to_transition

Builder.load_string('''<Main>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Main Menu'
            font_size: '60sp'
        Button:
            text: 'Start Game'
            on_press: root.new_game()
        Button:
            text: 'Settings'
            on_press: app.open_settings()
''')


class Main(Screen):
    
    def new_game(self):
        #Fade to a transition screen
        change_to_transition(self.manager, text='Day 1')
        
