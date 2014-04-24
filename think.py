__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from transition import change_to_transition
import os, random
import data.gameData as c


class Person:
    def __init__(self, **kwargs):
        self.name = self.find_random_name("male_names.txt") + " " + self.find_random_name("last_names.txt")
        self.tier = self.find_random_tier()
        self.crime = self.find_random_crime()
        self.offenses = self.find_weighted_random() + ' Offense'
        self.age = self.find_random_age()
        
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
        choices = [('First', 2), ('Second', 1)]
        population = [val for val, cnt in choices for i in range(cnt)]
        return random.choice(population)
    
    def find_random_tier(self):
        return random.choice(['proletariat', 'inner party', 'outer party', 'prominent'])
    
    def find_random_age(self):
        return random.choice(xrange(18, 61))


Builder.load_string('''<ThinkDesk>:
    name: 'desk'
    rb: rule_book
    arr_warrant: arrest_warrant
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
                    text: 'Vaporize'
                    on_press: root.vaporize()
                Button:
                    text: 'Reeducate'
                    on_press: root.reeducate()
                Button:
                    text: 'Imprison'
                    on_press: root.imprison()
                Button:
                    text: 'Quit'
                    on_press: root.manager.current = 'main'
''')


class ThinkDesk(Screen):
    rb = ObjectProperty()
    arr_warrant = ObjectProperty()
    perps = []
    playing = False
    day = 1
    
    def on_pre_enter(self):
        self.start_day()
        
    def start_day(self):
        if not self.playing and self.day < 6:
            self.rb.add_rules(self.day)
            self.rb.add_pages()
            self.playing = True   
            for i in range(random.randrange(4, 7)):
                p = Person()
                self.perps.append(p)
            self.change_perp()
    
    def reeducate(self):
        self.rb.check_rule(self.day, 'edu', self.current_perp)
        self.change_perp()
    
    def imprison(self):
        self.rb.check_rule(self.day, 'imp', self.current_perp)       
        self.change_perp()
    
    def vaporize(self):
        self.rb.check_rule(self.day, 'vap', self.current_perp)
        self.change_perp()
        
    def change_perp(self):
        if len(self.perps) > 0:
            self.current_perp = self.perps.pop()
            self.arr_warrant.new_person(self.current_perp)
        else:
            self.next_phase()
    
    def next_phase(self):
        change_to_transition(self.manager, text='End of Work')
        self.playing = False
        if self.day < 5:
            self.day += 1
    
        
Builder.load_string('''<Rules>:
    start_tab: basic
    rule_list: rules
    orientation: 'vertical'
    do_default_tab: True
    default_tab_text: 'Start>>'
    default_tab_content: root.default_label
    tab_pos: 'top_left'
    tab_width: self.width / 5
    TabbedPanelItem:
        id: basic
        text: 'Basic Truths'
        BoxLayout:
            orientation: 'vertical'
            id: rules
''')
class Page(TabbedPanelItem):
    
    def __init__(self, crime, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.text = crime       
        self.add_widget(self.crime_page(c.CRIMES[crime]))
            
    def crime_page(self, c):
        b = BoxLayout(orientation='vertical')
        b.add_widget(Label(text=c[0]))
        b.add_widget(Label(text=c[1]))
        b.add_widget(Label(text=c[2]))
        return b
    
class Rules(TabbedPanel):
    rule_list = ObjectProperty()
    crime_tab = c.CRIMES.keys()
    default_label = Label(text='HELLO') #having trouble getting the first page's widgets to show up
    choices = []
    
    def add_pages(self):
        self.clear_widgets()
        for c in self.crime_tab:
            self.add_widget(Page(c))
            
    def add_rules(self, day):
        self.rule_list.clear_widgets()
        rule_text = str(day) + '. ' + c.RULES[day-1]
        self.rule_list.add_widget(Label(text=rule_text))
            
    def check_rule(self, rule, choice, person):
        self.choices.append(choice)
        if rule >= 1:
            if not self.check_one(choice, person):
                print "You failed rule 1"
                return 0
        if rule >= 2:
            if not self.check_two(choice, person):
                print "You failed rule 2"
                return 0
        if rule >= 3:
            if not self.check_three(choice, person):
                print "You failed rule 3"
                return 0
        if rule >= 4:
            if not self.check_four(choice, person):
                print "You failed rule 4"
                return 0
        if rule >= 5:
            if not self.check_five(choice, person):
                print "You failed rule 5"

    def check_one(self, c, p):
        #Reeducation is not to be wasted on proletariat
        if p.tier == 'proletariat' and c == 'edu':
            return False
        return True
    
    def check_two(self, c, p):
        #Outer Party members > 42 years of age are to be vaporized
        if p.tier == 'outer party' and p.age > 42:
            if c != 'vap':
                return False
        return True

    def check_three(self, c, p):
        #Inner Party members < 40 years of age are to be reeducated
        if p.tier == 'inner party' and p.age < 40:
            if c != 'edu':
                return False
        return True

    def check_four(self, c, p):
        #Prominent members are never to be imprisoned
        if p.tier == 'prominent' and c == 'imp':
            return False
        return True
    
    def check_five(self, c, p):
        #Do not use the same punish more than twice in a row
        if len(self.choices) > 2:
            if c == self.choices[-2] and c == self.choices[-3]:
                return False
        return True
    
Builder.load_string('''<Warrant>:
    orientation: 'vertical'
    BoxLayout:
    
        Label:
            text: root.name_text
        Label:
            text: root.age_text
    Label:
        text: root.tier_text
    BoxLayout:
        Label:
            text: root.crime_text
        Label:
            text: root.offenses_text
''')

    
class Warrant(BoxLayout):
    name_text = StringProperty('')
    tier_text = StringProperty('')
    crime_text = StringProperty('')
    offenses_text = StringProperty('')
    age_text = StringProperty('')
    
    def __init__(self, **kwargs):
        super(Warrant, self).__init__(**kwargs)
        first = Person()
        self.new_person(first)
    
    def new_person(self, new):
        self.name_text = new.name
        self.tier_text = new.tier
        self.crime_text = new.crime
        self.offenses_text = new.offenses   
        self.age_text = 'Age: ' + str(new.age)
    

        
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
''')        

class Status(Screen):
    def get_day(self):
        d = 'Day '+str(self.manager.get_screen('desk').day)
        return d

    def move_on(self):
        change_to_transition(self.manager, text=self.get_day())

