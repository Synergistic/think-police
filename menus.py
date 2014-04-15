__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

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
            on_press: root.manager.current = 'settings'
''')


class Main(Screen):
    
    def new_game(self):
        self.manager.current = 'desk'
        self.manager.parent.playing = True
        self.manager.parent.current_day = 1
        print self.width, self.height
        
    
Builder.load_string('''<Settings>:
    name: 'settings'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Settings'
            font_size: '60sp'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'main'
''')
    
    
class Settings(Screen):
    pass

class Pause(Screen):
    pass