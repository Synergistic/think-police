from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial
from kivy.properties import StringProperty

Builder.load_string('''<DayChange>:
    Label:
        text: root.my_text
''')



class DayChange(Screen):
    my_text = StringProperty('')
    
def change_to_transition(sm, text='Day 1', n='newday', type=DayChange):
    '''Takes a screenmananager, text to display, the transition screen name, the actual
    transition screen, and the transition type. Makes the switch and then schedules the
    next transition to the next phase of the game.'''
    
    start_screen = sm.current 
    if sm.has_screen(n):
        sm.get_screen(n).my_text = text
        sm.current = n
    else:
        s = type(name=n)
        s.my_text = text
        sm.add_widget(s)
        sm.current = n
    
    sm.transition = FadeTransition()
    if sm.current == 'newday':        
        Clock.schedule_once(partial(next_phase, sm, start_screen), 1)
    elif sm.current == 'end':
        Clock.schedule_once(partial(restart, sm), 8)
    
def next_phase(sm, start, dt):

    if start == 'main':
        sm.current = 'desk'
    elif start == 'desk':
        sm.current = 'status'
    elif start == 'status':
        sm.current = 'desk'
    

def restart(sm, dt):
    sm.current = 'main'
    