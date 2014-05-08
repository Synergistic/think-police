__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from transition import change_to_transition
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_string('''<Main>:
    name: 'main'
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'top'
        Button:
            size_hint: (0.08229167, 0.14351852)
            background_normal: 'data/images/exit.png'
            on_release: app.stop()
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Image:
            source: 'data/images/thinkpol.png'
            size_hint: (0.260417, 0.347222)
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        BoxLayout:
            size_hint: (.30625, .29444)
            orientation: 'vertical'
            BoxLayout:
                Button:
                    background_normal: 'data/images/start.png'
                    on_release: root.new_game()
                Button:
                    background_normal: 'data/images/l2p.png'
                    on_release: root.welcome_pop()
            BoxLayout:
                Button:
                    background_normal: 'data/images/config.png'
                    on_release: app.open_settings()
                Button:
                    background_normal: 'data/images/thanx.png'
                    on_release: root.credit_pop()
''')


class Main(Screen):
    
    def new_game(self):
        #Fade to a transition screen
        change_to_transition(self.manager, text='Day 1')
        
    def welcome_pop(self):
        p = Popup(title='Greetings',
                  content=Label(text = '\n'.join(['You are responsible for processing crimethinkers.',
                        'Drop their arrest card into the appropriate slot.', ' ',
                        'You will be given a copy of the Law Enforcement Guide.',
                        'Violating Basic Truths multiple times will result in termination.',
                        'Crime pages list appropriate punishments, these do no supercede Basic Truths.'])),
                  size_hint=(0.4, 0.6))
        p.open()
    
    def credit_pop(self):
        p = Popup(title='Credits&Thanks',
                  content=Label(text = '\n'.join(['This is a placeholder',''])),
                  size_hint=(0.4, 0.6))
        p.open()