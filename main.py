__author__ = 'Synergy'

from kivy.app import App
from kivy.config import Config

Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)
Config.set('graphics', 'fullscreen', 'fake')

from kivy.uix.screenmanager import ScreenManager
from menus import Main, HowTo, Thanks
from think import ThinkDesk, Status
from kivy.core.window import Window

SCREENS = {'desk': ThinkDesk(),
           'status': Status(),
           'howto' : HowTo(),
           'main': Main(),
           'thanks': Thanks()}

class ThinkApp(App):
    
    def build(self, **kwargs):
        self.sm = ScreenManager()
        for scn_name in SCREENS.keys():
            self.sm.add_widget(SCREENS[scn_name])
        self.sm.current = 'main'
        Window.fullscreen = True
        return self.sm

if __name__ == '__main__':
    ThinkApp().run()
    