__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from transition import change_to_transition
import os, random
import data.gameData as c


class Person:
    def __init__(self, **kwargs):
        self.name = self.find_random_name("male_names.txt") + " " + self.find_random_name("last_names.txt")
        self.crime = self.find_random_crime()
        self.offenses = self.find_weighted_random() + ' Offense'
        
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
        
    def find_random_crime(self):
        return random.choice(c.CRIMES.keys())

    def find_weighted_random(self):
        choices = [('First', 2), ('Second', 3), ('Third', 1)]
        population = [val for val, cnt in choices for i in range(cnt)]
        return random.choice(population)


Builder.load_string('''<ThinkDesk>:
    name: 'desk'
    rb: rule_book
    BoxLayout:
        size_hint: (1, 0.8)
        pos_hint: {'center_y': 0.6}
        Rules:
            id: rule_book
        Warrant:
            id: arrest_warrant
    AnchorLayout:
        size_hint: (1, 0.2)
        BoxLayout:
            orientation: 'vertical'
            BoxLayout: 
                Button: 
                    text: 'Erase'
                Button:
                    text: 'Reeducate'
                Button:
                    text: 'Imprison'
                Button:
                    text: 'New Perp'
                    on_press: arrest_warrant.new_person()
                Button:
                    text: 'Quit'
                    on_press: root.manager.current = 'main'
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
    
    def next_phase(self):
        change_to_transition(self.manager, text='End of Work')
        if self.manager.parent.current_day < 5:
            self.manager.parent.current_day += 1
    
    
        
Builder.load_string('''<Rules>:

    pos: 400, 200
    do_default_tab: False
    TabbedPanelItem:
        text: 'Basic'

''')

class Rules(TabbedPanel):
    rule_list = ObjectProperty()
    
    def add_rules(self, day):
        for i in range(day):
            rule_text = str(i+1) + '. ' + c.RULES[i]
            self.rule_list.add_widget(Label(text=rule_text, font_size=(str(self.parent.height/50)+'sp')))
        

Builder.load_string('''<Warrant>:
    orientation: 'vertical'
    Label:
        text: root.name_text
    Label:
        text: root.crime_text
    Label:
        text: root.offenses_text
''')

    
class Warrant(BoxLayout):
    name_text = StringProperty('')
    crime_text = StringProperty('')
    offenses_text = StringProperty('')
    
    def __init__(self, **kwargs):
        super(Warrant, self).__init__(**kwargs)
        first = Person()
        self.name_text = first.name
        self.crime_text = first.crime
        self.offenses_text = first.offenses
    
    def new_person(self):
        new = Person()
        self.name_text = new.name
        self.crime_text = new.crime
        self.offenses_text = new.offenses        
    

        
Builder.load_string('''<Status>:
    name: 'status'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Status'        
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Wife'
            ProgressBar:
                max: 100
                value: 50
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Child'
            ProgressBar:
                max: 100
                value: 50
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Child'
            ProgressBar:
                max: 100
                value: 50
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'You'
            ProgressBar:
                max: 100
                value: 50
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Done'
                on_press: root.move_on()
            Button:
                text: 'dongs'
''')        

class Status(Screen):
    def get_day(self):
        d = 'Day '+str(self.manager.parent.current_day)
        return d

    def move_on(self):
        change_to_transition(self.manager, text=self.get_day())