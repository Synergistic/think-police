__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from transition import change_to_transition
from kivy.animation import Animation
import os, random
import data.gameData as c

Builder.load_string('''<Divide>:
    size_hint: (0.04, 1)
    canvas.before:
        Color:
            rgba: .2, .2, .2, 1
        Rectangle:
            pos: self.pos
            size: self.size
''')
class Divide(Widget):
    pass

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
    rec: recommend
    arr_desk: my_desk
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint: (1, 0.45)
            pos_hint: {'center_y': 0.6}
            Rules:
                orientation: 'vertical'

                id: rule_book
            Recs:
                orientation: 'vertical'
                id: recommend
        Widget:
            size_hint: (1, 0.01)
            canvas.before:
                Color:
                    rgba: .1, .1, .1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        Desk:
            id: my_desk
            size_hint: (1, 0.475)
        BoxLayout:
            size_hint: (1, 0.075)
            size: 200, 400
            Widget:
                id: vap
                canvas.before:
                    Color:
                        rgba: .5, .5, .5, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size: vap.size
                    pos: vap.pos
                    text: 'Vaporize'
            Divide:
            Widget:
                id: ree
                canvas.before:
                    Color:
                        rgba: .5, .5, .5, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size: ree.size
                    pos: ree.pos
                    text: 'Reeducate'
            Divide:
            Widget:
                id: imp
                canvas.before:
                    Color:
                        rgba: .5, .5, .5, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size: imp.size
                    pos: imp.pos
                    text: 'Imprison'
            Divide:
            Button:
                text: 'Quit'
                on_press: root.manager.current = 'main'
                on_release: root.playing = False
''')


class ThinkDesk(Screen):
    rb = ObjectProperty()
    rec = ObjectProperty()
    arr_desk = ObjectProperty()
    perps = []

    playing = False
    day = 1
    strikes = 0
    
    def on_pre_enter(self):
        if not self.playing:
            self.welcome_pop()
        self.start_day()
    
    def welcome_pop(self):
        p = Popup(title='Greetings',
                  content=Label(text = '\n'.join(['Welcome to the ThoughtPolice comrade.', ' ',
                        'You are responsible for processing individuals that break the law.',
                        'Drop their arrest card into the appropriate slot.', ' ',
                        'Here is a copy of the Law Enforcement Guide.',
                        'Violating Basic Truths multiple times will result in termination.',
                        'Crime pages list appropriate punishments, deviation may',
                        'have unintended consequences'])),
                  size_hint=(0.6, 0.6))
        p.open()
        
    def start_day(self):
        if not self.playing:
            
            self.playing = True
            self.day = 1
            self.strikes = 0
            self.perps = []
            self.manager.get_screen('status').money = 50
            self.manager.get_screen('status').sanity = 100
            self.manager.get_screen('status').loyalty = 100 
            
        if self.day < 6:
            self.rb.add_pages(self.day)
            self.rec.add_pages()
            perp_count = random.randrange(5, 6+self.day)
            print 'Day ' + str(self.day)
            print 'Today we will have ' + str(perp_count) + ' criminals'
            for i in range(perp_count):
                p = Person()
                self.perps.append(p)
            self.change_perp()
    
    def choice(self, ch, card):
        self.modify_stats(self.rb.check_rules(self.day, ch, self.current_perp))
        Clock.schedule_once(self.change_perp, 1)
        
    def modify_stats(self, changes):
        print 'You get', changes[0], '$,', changes[1], 'sanity, and', changes[2], 'loyalty'
        self.manager.get_screen('status').money += changes[0]
        self.manager.get_screen('status').sanity += changes[1]
        self.manager.get_screen('status').loyalty += changes[2]

    def change_perp(self, *dt):
        if len(self.perps) > 0:
            self.current_perp = self.perps.pop()
            self.arr_desk.arr_card.new_person(self.current_perp)
        else:
            self.next_phase()
    
    def next_phase(self):
        if self.strikes >= 5:
            change_to_transition(self.manager, text='Too many errors, goodbye comrade.', type=Ending, n='end')
            self.playing = False
        else:
            change_to_transition(self.manager, text='End of Work')
            if self.day < 5:
                self.day += 1
    
        

class Page(AccordionItem):
    
    def __init__(self, crime, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.title = crime       
        self.add_widget(self.crime_page(c.CRIMES[crime]))
            
    def crime_page(self, c):
        b = BoxLayout(orientation='vertical')
        b.add_widget(Label(text=c[0]))
        b.add_widget(Label(text='First Offense: ' + c[1]))
        b.add_widget(Label(text='Seconds Offense: ' +c[2]))
        return b
    
Builder.load_string('''<Card>:
    size: 200, 325
    canvas.before:
        Color:
            a: 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'data/images/card.png'
    BoxLayout:
        orientation: 'vertical'
        pos: root.x, root.y + 65
        size: root.size[0], root.size[1] - 65
        Label:
            text: root.name_text
        Label:
            text: root.age_text
        Label:
            text: root.tier_text
        
        Label:
            text: root.crime_text
''')
class Card(Widget):
    name_text = StringProperty('')
    age_text = StringProperty('')
    tier_text = StringProperty('')
    crime_text = StringProperty('')
    decided = False
    
    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.new_person(Person())
    
    def new_person(self, new):
        self.name_text = new.name
        self.tier_text = new.tier.capitalize()
        self.age_text = ' '.join(['Aged', str(new.age)])
        self.crime_text = ' '.join([new.offenses.partition(' ')[0], new.crime])

        self.center_y = 268
        self.x = 500
        self.decided = False
    

    def on_touch_move(self, touch):
        if not self.decided:
            if self.x + self.width >= touch.x >= self.x and\
               self.y + self.height >= touch.y >= self.y:
                self.center_y = touch.y
                self.center_x = touch.x
    
    def on_touch_up(self, touch):
        '''detects which choice it is let go in, then returns that choice
        to the main game object and animates the card'''
        points = [(240, 60), (720, 60), (1200, 60)]
        options = ['vaporize', 'reeducate', 'imprison']
        if not self.decided:
            for point in points:
                if self.collide_point(point[0], point[1]):
                    c = options[points.index(point)]
                    self.decided = True
                    self.parent.parent.parent.choice(c[:3], self)
                    Animation(y=point[1]-self.height, duration=0.5).start(self)
                
Builder.load_string('''<Desk>:
    canvas:
        Color:
            a: 1
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'data/images/desk.png'

    arr_card: crd
    Card:
        id: crd
        center_y: root.center_y
        x: root.x + (root.center_x - (self.width/2))
 
''')

class Desk(Widget):
    arr_card = ObjectProperty()
    
class Rules(Accordion):
    crime_tab = c.CRIMES.keys()
    choices = []
    
    def add_pages(self, day):
        self.clear_widgets()    
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
            self.parent.parent.parent.strikes += 1
        else:
            print 'You passed all rules.'
            
        changes = [i*modifiers[multiplier.index(i)] for i in multiplier]
        return changes
    
    def check_one(self, ch, p):
        #Do not use the same punish more than twice in a row
        if len(self.choices) > 2:
            if ch == self.choices[-2] and ch == self.choices[-3]:
                self.choices = []
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
    

class Recs(Accordion):
    crime_tab = c.CRIMES.keys()
    
    def add_pages(self):
        self.clear_widgets()
        for c in self.crime_tab:
            self.add_widget(Page(c))  
            
        l = '\n'.join(['Proletariat - faggots',
                       'Outer Party - Less faggots',
                       'Inner Party - Not faggots',
                       'Prominent - Large, recognizable dicks'])
        a = AccordionItem(title='Classes')
        class_list = BoxLayout(orientation='vertical')
        class_list.add_widget(Label(text=l))
        a.add_widget(class_list)
        self.add_widget(a)

        lab = Label(text=l)
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
                person.value -= 25
        else:
            self.manager.get_screen('desk').playing = False

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
        elif int(self.get_day()[4]) >= 6:
            change_to_transition(self.manager, text='The reeducation is complete.', type=Ending, n='end')
            return True
        return False
        
        
            
