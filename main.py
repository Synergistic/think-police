__author__ = 'Synergy'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from menus import Main, Settings, Pause
from think import ThinkDesk

SCREENS = {'main': Main(),
           'settings': Settings(),
           'desk': ThinkDesk()}

class ThinkApp(App):
    playing = False
    current_day = 0
    
    def build(self, **kwargs):
        self.sm = ScreenManager()
        for scn_name in SCREENS.keys():
            self.sm.add_widget(SCREENS[scn_name])
        self.sm.current = 'main'   
        return self.sm
        

if __name__ == '__main__':
    ThinkApp().run()