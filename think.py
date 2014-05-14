__author__ = 'Synergy'

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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
    def __init__(self, age_limit=45, **kwargs):
        gender = random.choice(["male_names.txt", "female_names.txt"])
        self.name = self.find_random_name(gender) + " " + self.find_random_name("last_names.txt")
        self.tier = self.find_random_tier()
        self.crime = self.find_random_crime()
        self.age = self.find_random_age(age_limit)
        
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
    
    def find_random_tier(self):
        choices = [('proletariat', 4),  ('inner party', 2), ('outer party', 3)]
        population = [val for val, cnt in choices for i in range(cnt)]
        return random.choice(population)
    
    def find_random_age(self, upper_limit):
        return random.choice(xrange(20, upper_limit))


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
        Widget:
            size_hint: (1, 0.061625)
            canvas.after:
                Color:
                    a: 1
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: 'data/images/tubes.png'
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'top'
        Button:
            size_hint: (0.0411, 0.0717)
            background_normal: 'data/images/back.png'
            on_release: root.quit()
''')


class ThinkDesk(Screen):
    rb, rec, arr_desk = ObjectProperty(), ObjectProperty(), ObjectProperty()
    perps = []
    playing = False
    day, strikes, score = 0, 0, 0
    
    def on_pre_enter(self):
        c.set_random_sentences()
        self.start_day()
       
    def start_day(self):
        if not self.playing:   
            self.day = 1
            self.strikes = 0
            self.perps = []
            self.playing = True
            
        if self.day < 6:
            self.rb.add_pages(self.day)
            self.score = 0
            self.rb.choices = []
            self.rec.add_pages()
            self.perp_count = random.randrange(6, 8+self.day)
            max_age = 45
            for i in range(self.perp_count):
                p = Person(max_age)
                if p.age >= 40:
                    max_age -=2
                self.perps.append(p)
                
            self.change_perp()
    
    def choice(self, ch, card):
        self.modify_stats(self.rb.check_rules(self.day, ch, self.current_perp))
        Clock.schedule_once(self.change_perp, 1)
        
    def modify_stats(self, changes):
        self.score += changes
        
    def change_perp(self, *dt):
        if len(self.perps) > 0:
            self.current_perp = self.perps.pop()
            self.arr_desk.arr_card.new_person(self.current_perp)
        else:
            self.next_phase()
    
    def next_phase(self):
        if self.strikes >= 4:
            change_to_transition(self.manager, text='[i]Divergence is doubleplus ungood.[/i]', type=Ending, n='end')
            self.playing = False
        else:
            change_to_transition(self.manager, text='End of Work')
            if self.day <= 5:
                self.day += 1
            self.manager.get_screen('status').get_stats(self.score, self.perp_count)
            
    def quit(self):
        self.manager.current = 'main'
        self.playing = False
    
        

class Page(AccordionItem):
    
    def __init__(self, crime, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.title = crime       
        self.add_widget(self.crime_page(c.CRIMES[crime]))
            
    def crime_page(self, c):
        b = BoxLayout(orientation='vertical')
        b.add_widget(Label(text=c[0]))
        b.add_widget(Label(text=c[1]))
        return b
    
Builder.load_string('''<Card>:
    size: 200, 325
    canvas:
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
    
    def new_person(self, new):
        self.name_text = new.name
        self.tier_text = new.tier.capitalize()
        self.age_text = ' '.join(['Aged', str(new.age)])
        self.crime_text = new.crime

        self.center_y = self.parent.parent.parent.height / 3.0
        self.center_x = self.parent.parent.parent.width / 2.0
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
        width = self.parent.parent.parent.width
        height = self.parent.parent.parent.height * 0.06
        points = [(width * 0.24479167 , height), (0.41458333 * width, height),
                  (0.5859375 * width, height), (0.75859375 * width, height)]
        options = ['vaporize', 'reeducate', 'room', 'joycamp']
        if not self.decided:
            for point in points:
                if self.collide_point(point[0], point[1]):
                    ch_index = points.index(point)
                    choice = options[ch_index]
                    self.decided = True
                    self.parent.parent.parent.choice(choice[:3], self)
                    Animation(y=point[1]-self.height, duration=0.5).start(self)
                    if self.parent.parent.parent.manager.get_screen('main').sound:
                        c.ticket_sound.play()
            
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
        self.choices = []
        for i in range(day):
            rule_text = str(i+1) + '. ' + c.RULES[i]
            self.rule_list.add_widget(Label(text=rule_text))
     
    def check_suggested(self, ch, p):
        answer = c.CRIMES[p.crime][1][:3].lower()
        if answer == ch:
            result = 1.0
        else:
            result = 0.5
        return result
    
    def check_rules(self, rules, choice, person):
        net_change = self.check_suggested(choice, person)
        self.choices.append(choice)
        failed = False
        if rules >= 1:
            if not self.check_one(choice, person):
                failed = True
        if rules >= 2:
            if not self.check_two(choice, person):
                failed = True
        if rules >= 3:
            if not self.check_three(choice, person):
                failed = True
        if rules >= 4:
            if not self.check_four(choice, person):
                failed = True
        if rules >= 5:
            if not self.check_five(choice, person):
                failed = True
                
        if failed: #fail a rule = no money gain
            net_change = 0
            self.parent.parent.parent.strikes += 1
        return net_change
    
    def check_one(self, ch, p):
        #Do not use the same punish more than twice in a row
        if len(self.choices) > 2:
            if ch == self.choices[-2] and ch == self.choices[-3]:
                return False
        return True
    
    def check_two(self, ch, p):
        #Reeducation is not to be wasted on proletariat
        if p.tier == 'proletariat' and ch == 'ree':
            return False
        return True    


    def check_three(self, ch, p):
        #Inner Party members < 35 years cannot be sent to joycamp
        if p.tier == 'inner party' and p.age < 35:
            if ch == 'joy':
                return False
        return True

    def check_four(self, ch, p):
        #Outer party members should not be vaporized
        if p.tier == 'outer party' and ch == 'vap':
            return False
        return True
    
    def check_five(self, ch, p):
        #People > 40 years of age are to be vaporized
        if p.age > 40:
            if ch != 'vap':
                return False
        return True
    
class Recs(Accordion):
    crime_tab = c.CRIMES.keys()
    
    def add_pages(self):
        self.clear_widgets()
        for c in self.crime_tab:
            self.add_widget(Page(c))  
            
        l = '\n'.join(['Proletariat - The working poor, non-believers of IngSoc.',
                       'Outer Party - Middle class members of The Party',
                       'Inner Party - Individuals having demonstrated dedication to Ingsoc and The Party.'])
        a = AccordionItem(title='Classes')
        class_list = BoxLayout(orientation='vertical')
        class_list.add_widget(Label(text=l))
        a.add_widget(class_list)
        self.add_widget(a)

        lab = Label(text=l)
Builder.load_string('''<Ending>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (0.4, 0.60)
            Image:
                source: 'data/images/ingsoc.jpg'
            Label:
                markup: True
                text: root.slogan
            Label:
            Label:
                markup: True
                text: root.my_text
                font_size: '32sp'
                
''')

class Ending(Screen):
    my_text = StringProperty('Game Over')
    slogan = StringProperty('[b]          WAR IS PEACE    \n    FREEDOM IS SLAVERY \nIGNORANCE IS STRENGTH[/b]')
 
Builder.load_string('''<Status>:
    name: 'status'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (.15312, 0.8)
            Label:
                markup: True
                text: root.title
                font_size: '48sp'
            ProgressBar:
                value: root.grade_value
                max: 100
            Label:
                markup: True
                font_size: '22sp'
                text: root.grade_letter
            Label:
            Label:
            Button:
                background_normal: 'data/images/okay.png'
                on_release: root.move_on()
''')        

class Status(Screen):
    grade_letter = StringProperty('')
    title = StringProperty('')
    grade_value = NumericProperty(0)
    d_grades = 0
        
    def get_day(self):
        d = 'Day '+str(self.manager.get_screen('desk').day)
        return d

    def get_stats(self, correct, total):
        finished_day = int(self.get_day()[4]) -1
        self.title = '[b]Day ' + str(finished_day) + ' Assessment[/b]'
        self.grade_value = (correct/total)*100.0
        self.grade_letter = self.number_to_letter(self.grade_value)
   
    def number_to_letter(self, grade):
        if grade >= 90.0:
            letter = '[i]Doubleplusgood[/i]'
        elif grade >= 80.0:
            letter = '[i]Plusgood[/i]'
        elif grade >= 70.0:
            letter = '[i]Good[/i]'
        elif grade >= 60.0:
            letter = '[i]Ungood[/i]'
        elif grade < 60.0:
            letter = '[i]Doubleplusungood[/i]'
        if grade < 70.0:
            self.d_grades += 1
        return 'Rating: ' + letter
    
    def move_on(self):
        if not self.ending():
            change_to_transition(self.manager, text=self.get_day())
        else:
            self.manager.get_screen('desk').playing = False
            self.d_grades = 0
        
    def ending(self):
        if self.d_grades >= 2:
            end = random.choice(['[i]illness.[/i]', '[i]starvation.[/i]'])
            end_text = ' '.join(["[i]Your family has died from", end, '\nYou have failed to progress The Party.[/i]'])
            change_to_transition(self.manager, text=end_text, type=Ending, n='end')
            return True
        elif int(self.get_day()[4]) >= 6:
            change_to_transition(self.manager, text='[i]    Congratulations.\nYour reeducation is complete.\nWelcome to ThinkPol comrade.[/i]', type=Ending, n='end')
            return True
        return False
        
        