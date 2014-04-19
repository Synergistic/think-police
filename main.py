__author__ = 'Synergy'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from menus import Main
from think import ThinkDesk, Status

SCREENS = {'main': Main(),
           'desk': ThinkDesk(),
           'status': Status()}

class ThinkApp(App):
    current_day = 0

    
    def build(self, **kwargs):
        self.sm = ScreenManager()
        for scn_name in SCREENS.keys():
            self.sm.add_widget(SCREENS[scn_name])
        self.sm.current = 'main'   
        return self.sm

if __name__ == '__main__':
    ThinkApp().run()