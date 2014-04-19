from kivy.uix.screenmanager import Screen, SlideTransition, SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition
from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial
from kivy.properties import StringProperty

Builder.load_string('''<DayChange>:
    Label:
        text: root.my_text
''')


class DayChange(Screen):
    my_text = StringProperty('Day 1')

def change_to_transition(sm, text='Day 1', n='newday', type=DayChange, trans=WipeTransition()):
    start_screen = sm.current 
    if sm.has_screen(n):
        sm.get_screen(n).my_text = text
        sm.current = n
    else:
        sm.switch_to(type(name=n), transition=trans)
        
    Clock.schedule_once(partial(wait_n_change, sm, start_screen), 1)
    
def wait_n_change(sm, start, dt):
    if start == 'main':
        sm.current = 'desk'
    elif start == 'desk':
        sm.current = 'status'
    elif start == 'status':
        sm.current = 'desk'
        