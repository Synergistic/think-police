__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scatter import Scatter 
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
import os, random
import data.gameData as c

Builder.load_string('''<ThinkDesk>:
    name: 'desk'
    rb: rule_book
    FloatLayout:
        Button:
            size_hint: (0.1, 0.1)
            pos_hint: {'center_x': 0.05, 'top': 1}
            text: 'Quit'
            on_press: root.manager.current = 'main'
        Rules:
            id: rule_book
        IdCards:
            id: identitycards
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        size_hint: (1, 0.2)
        BoxLayout:
            orientation: 'vertical'
            BoxLayout: 
                Button: 
                    text: 'Execute'
                Button:
                    text: 'Change Name'
                    on_press: identitycards.new_name()
                Button:
                    text: 'Imprison'
            BoxLayout:
                Button:
                    text: 'Begin'
                    on_press: root.start_day()
                Button:
                    text: 'add a day'
                    on_press: root.increment_day()
''')


class ThinkDesk(Screen):
    rb = ObjectProperty()
    playing = False
    
    def start_day(self):
        if not self.playing:
            self.rb.add_rules(self.manager.parent.current_day)
            self.playing = True
        else:
            self.rb.rule_list.clear_widgets()
            self.playing = False
    def increment_day(self):
        self.manager.parent.current_day += 1
        
Builder.load_string('''<Rules>:
    rule_list: rule_box
    do_rotation: False
    do_scale: False
    size_hint: (0.4, 0.8)
    pos: 400, 200
    canvas:
        Color: 
            r: .5
            g: 0.7
            b: .1
        Rectangle:
            size: self.size
    BoxLayout:
        id: rule_box
        orientation: 'vertical'
        pos: root.width/3, root.height/3
        spacing: 50
        padding: 10
''')

class Rules(Scatter):
    rule_list = ObjectProperty()
    
    def add_rules(self, day):
        for i in range(day):
            rule_text = str(i+1) + '. ' + c.RULES[i]
            self.rule_list.add_widget(Label(text=rule_text, font_size=(str(self.parent.height/50)+'sp')))
        

Builder.load_string('''<IdCards>:
    do_rotation: False
    do_scale: False
    size_hint: (0.3, 0.3)
    pos: 200, 200
    name_text: namelabel
    canvas:
        Color: 
            r: 0
            g: .2
            b: .5
        Rectangle:
            size: self.size
            
    BoxLayout:
        pos: root.width/4, root.height/3
        orientation: 'vertical'
        Label:
            id: namelabel
            text: root.find_random_name("male_names.txt") + " " + root.find_random_name("last_names.txt")
''')


class IdCards(Scatter):
    name_text = ObjectProperty()
    
    def find_random_name(self, file_text):
        #function to pick a random line in a text file and return a name on that line
        name_file = os.path.join(os.path.curdir, 'data', file_text)
        with open(name_file, 'r+') as f:
          
            f_size = os.stat(name_file)[6] #get file size
            
            #change current pointer pos + random size
            f.seek((f.tell() + random.randint(0, f_size-1))%f_size)
            f.readline() #skip a line in case we're in the middle
            
            #split the next line at 1st blank, take the first partition and capitalize it
            name = f.readline().partition(' ')[0].capitalize()
            return name
    
    def new_name(self):
        self.name_text.text = ' '.join([self.find_random_name("male_names.txt"),
                                    self.find_random_name("last_names.txt")])
        