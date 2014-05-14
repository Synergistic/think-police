__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from transition import change_to_transition
import data.gameData as c

Builder.load_string('''<Main>:
    name: 'main'
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'top'
        Button:
            size_hint: (0.08229167, 0.14351852)
            background_normal: 'data/images/sound_on.png'
            on_release: root.toggle_sound(self)
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
                    on_release: root.manager.current = 'howto'
            BoxLayout:
                Button:
                    background_normal: 'data/images/exit.png'
                    on_release: app.stop()
                Button:
                    background_normal: 'data/images/thanx.png'
                    on_release: root.manager.current = 'thanks'
''')


class Main(Screen):
    sound = True
    
    def on_enter(self):
        if self.sound:
            c.bg_music.play()
        
    def new_game(self):
        #Fade to a transition screen
        change_to_transition(self.manager, text='Day 1')
    
    def toggle_sound(self, widget):
        self.sound = not self.sound
        if self.sound:
            widget.background_normal = 'data/images/sound_on.png'
            c.bg_music.play()
        else:
            widget.background_normal = 'data/images/sound_off.png'
            c.bg_music.stop()
        
Builder.load_string('''<HowTo>:
    name: 'howto'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Image:
            source: 'data/images/howto.png'
            size_hint: (0.666666667, 0.666666667)         
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'top'
        Button:
            size_hint: (0.0411, 0.0717)
            background_normal: 'data/images/back.png'
            on_release: root.manager.current = 'main'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        BoxLayout:
            size_hint: (1, .25)
            orientation: 'vertical'
            Label:
                text: root.instruction_text
''')

class HowTo(Screen):
    instruction_text = '\n'.join(["You will be graded based on your adherence to the Basic Truths and Big Brother's Guide.", 
                                  "Repeat poor performance will result in a pay decrease."])

Builder.load_string('''<Thanks>:
    name: 'thanks'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Label:
            size_hint: (0.15, 0.20)
            text: root.text
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'top'
        Button:
            size_hint: (0.0411, 0.0717)
            background_normal: 'data/images/back.png'
            on_release: root.manager.current = 'main'          
''')
    
class Thanks(Screen):
    text = '\n'.join(['Special Thanks', 'George Orwell for the novel 1984',
                                'Lucas Pope (@dukope) for his game Papers, Please', ' ',
                                'Game Design & Programming: Synergy (@synergistik)',
                                'Music: Roald Strauss',
                                'Creative Commons Attribution-ShareAlike 4.0 International License.'])