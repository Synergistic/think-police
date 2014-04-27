__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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
        choices = [('proletariat', 3),  ('inner party', 2), ('outer party', 2), ('prominent', 1)]
        population = [val for val, cnt in choices for i in range(cnt)]
        return random.choice(population)
    
    def find_random_age(self):
        return random.choice(xrange(18, 71))


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
                    on_release: root.playing = False
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
        if not self.playing:
            self.playing = True
            self.day = 1
            self.manager.get_screen('status').money = 50
            self.manager.get_screen('status').sanity = 100
            self.manager.get_screen('status').loyalty = 100 
            
        if self.day < 6:
            self.rb.add_pages(self.day)    
            for i in range(random.randrange(4, 7)):
                p = Person()
                self.perps.append(p)
            self.change_perp()
    
    def reeducate(self):
        self.modify_stats(self.rb.check_rules(self.day, 'ree', self.current_perp))
        self.change_perp()
    
    def imprison(self):
        self.modify_stats(self.rb.check_rules(self.day, 'imp', self.current_perp))
        self.change_perp()
  
    def vaporize(self):
        self.modify_stats(self.rb.check_rules(self.day, 'vap', self.current_perp))
        self.change_perp()
    
    def modify_stats(self, changes):
        print 'You get', changes[0], '$,', changes[1], 'sanity, and', changes[2], 'loyalty'
        self.manager.get_screen('status').money += changes[0]
        self.manager.get_screen('status').sanity += changes[1]
        self.manager.get_screen('status').loyalty += changes[2]

    def change_perp(self):
        if len(self.perps) > 0:
            self.current_perp = self.perps.pop()
            self.arr_warrant.new_person(self.current_perp)
        else:
            self.next_phase()
    
    def next_phase(self):
        change_to_transition(self.manager, text='End of Work')
        if self.day < 5:
            self.day += 1
    
        
Builder.load_string('''<Rules>:
    orientation: 'vertical'
        
''')
class Page(AccordionItem):
    
    def __init__(self, crime, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.title = crime       
        self.add_widget(self.crime_page(c.CRIMES[crime]))
            
    def crime_page(self, c):
        b = BoxLayout(orientation='vertical')
        b.add_widget(Label(text=c[0]))
        b.add_widget(Label(text=c[1]))
        b.add_widget(Label(text=c[2]))
        return b
    
class Rules(Accordion):
    crime_tab = c.CRIMES.keys()
    choices = []
    
    def add_pages(self, day):
        self.clear_widgets()
        for c in self.crime_tab:
            self.add_widget(Page(c))        
        a = AccordionItem(title='Basic Truths')
        self.rule_list = BoxLayout(orientation='vertical')
        a.add_widget(self.rule_list)
        self.add_rules(day)
        self.add_widget(a)

            
    def add_rules(self, day):
        for i in range(day):
            rule_text = str(i+1) + '. ' + c.RULES[i]
            self.rule_list.add_widget(Label(text=rule_text))
     
    def check_suggested(self, ch, p):
        rank = ['imp', 'ree', 'vap']
        if p.offenses[0] == 'F':
            answer = c.CRIMES[p.crime][1][:3].lower()
        else:
            answer = c.CRIMES[p.crime][2][:3].lower()
            
        if rank.index(answer) == rank.index(ch):
            #suggested matches, +money, +loyalty
            result = [1, 0, 1]
            print 'Same as suggested'
        if rank.index(answer) < rank.index(ch):
            #more severe than suggested, +money, -2x sanity, +loyalty
            result = [1, -2, 1]
            print 'More than suggested'
        elif rank.index(answer) > rank.index(ch):
            #less severe than suggested, no money, -sanity, -loyalty
            result = [0, -1, -1]
            print 'Less than suggested'
        return result
    
    def check_rules(self, rules, choice, person):
        multiplier = self.check_suggested(choice, person)
        self.choices.append(choice)
        modifiers = [c.MONEY_C, c.SANITY_C, c.LOYALTY_C]
        failed = False
        if rules >= 1:
            if not self.check_one(choice, person):
                print "You failed rule 1"
                failed = True
        if rules >= 2:
            if not self.check_two(choice, person):
                print "You failed rule 2"
                failed = True
        if rules >= 3:
            if not self.check_three(choice, person):
                print "You failed rule 3"
                failed = True
        if rules >= 4:
            if not self.check_four(choice, person):
                print "You failed rule 4"
                failed = True
        if rules >= 5:
            if not self.check_five(choice, person):
                print "You failed rule 5"
                failed = True
                
        if failed: 
            multiplier = [0, multiplier[1], -2]
        else:
            print 'You passed all rules.'
            
        changes = [i*modifiers[multiplier.index(i)] for i in multiplier]
        return changes
    
    def check_one(self, ch, p):
        #Do not use the same punish more than twice in a row
        if len(self.choices) > 2:
            if ch == self.choices[-2] and ch == self.choices[-3]:
                return False
        return True

    def check_two(self, ch, p):
        #Rereecation is not to be wasted on proletariat
        if p.tier == 'proletariat' and ch != 'vap':
            return False
        return True
    
    def check_three(self, ch, p):
        #Outer Party members > 42 years of age are to be vaporized
        if p.age > 42:
            if ch != 'vap':
                return False
        return True

    def check_four(self, ch, p):
        #Inner Party members < 40 years of age are to be rereecated
        if p.tier == 'inner party' and p.age < 40:
            if ch != 'ree':
                return False
        return True

    def check_five(self, ch, p):
        #Prominent members are never to be imprisoned
        if p.tier == 'prominent' and ch == 'imp':
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
    

      
      
Builder.load_string('''<Ending>:
    Label:
        text: root.my_text
''')

class Ending(Screen):
    my_text = StringProperty('Game Over') 
 
Builder.load_string('''<Status>:
    name: 'status'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Status'
        BoxLayout:
            Label:
                text: 'Money: ' + str(root.money)
            Label:
                text: 'Loyalty:  ' + str(root.loyalty)
            Label:
                text: 'Sanity: ' + str(root.sanity)
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Feed'
                on_press: root.feed(wifey)
            Label:
                text: 'Wife'
            ProgressBar:
                id: wifey
                max: 100
                value: 50
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Feed'
                on_press: root.feed(kid)            
            Label:
                text: 'Child'
            ProgressBar:
                id: kid
                max: 100
                value: 50
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Feed'
                on_press: root.feed(you)
            Label:
                text: 'You'
            ProgressBar:
                id: you
                max: 100
                value: 50
        Button:
            text: 'Done'
            on_press: root.move_on(you, kid, wifey)
''')        

class Status(Screen):
    money = NumericProperty(50)
    loyalty = NumericProperty(100)
    sanity = NumericProperty(100)
    starving = False
    
    def get_day(self):
        d = 'Day '+str(self.manager.get_screen('desk').day)
        return d

    def move_on(self, *args):
        for person in args:
            if person.value <= 0:
                self.starving = True
        if not self.ending():
            change_to_transition(self.manager, text=self.get_day())
            for person in args:
                person.value -= 35

    def feed(self, p):
        if self.money >= c.FOOD_COST:
            self.money -= c.FOOD_COST
            p.value += c.FOOD_EFFECT
        else:
            print 'Not enough money'
        
    def ending(self):
        if self.loyalty <= 0:
            change_to_transition(self.manager, text='You were caught', type=Ending, n='end')
            return True
        elif self.sanity <= 0:
            change_to_transition(self.manager, text='You went insane', type=Ending, n='end')
            return True
        elif self.starving:
            change_to_transition(self.manager, text='You & your family starved', type=Ending, n='end')
            return True
        return False
        
        
            
