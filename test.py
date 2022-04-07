import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

from cave.xmlroomconfigreader import XmlRoomConfigReader

from cave.ui.inputbutton import InputButton
from cave.ui.statusactivityindicator import StatusActivityIndicator
from cave.ui.swipeaccordion import SwipeAccordion, SwipeAccordionItem

from cave.drivers.projector.nec import NEC


class TestRootWidget(BoxLayout):
    def __init__(self, app, **kwargs):
        super(TestRootWidget, self).__init__(**kwargs)
        self.app = app
        # self.build_accordion()

        # Horrible...
        self.config = XmlRoomConfigReader(self)

        # Once all the tabs have been created, fire touch_down event on the first tab.
        # This will in turn set app.current_tab_title and app.current_tab_id.
        # (see SwipeAccordionItem.on_touch_down())
        first_tab = list(self.app.available_tabs)[0]
        self.ids[first_tab].dispatch('on_touch_down', self.ids[first_tab])

    def build_accordion(self):
        acc = self.ids['acc']
        for id, title in self.app.available_tabs:
            tab = self.build_accordion_tab(id, title)
            acc.add_widget(tab)
        # select first (home) tab
        # self.ids['accordion_tab_0'].dispatch('on_touch_down', self.ids['accordion_tab_0'])
        first_tab = list(self.app.available_tabs)[0]
        self.ids[first_tab].dispatch('on_touch_down', self.ids[first_tab])

    def build_accordion_tab(self, id, tab_title=''):
        tab = SwipeAccordionItem(title=tab_title)
        self.ids[id] = tab
        fl = FloatLayout()
        label = Label(text=tab_title)
        label.pos_hint = {'x': .09, 'y': .5}
        label.font_size = '20dp'
        label.size_hint_x = .8
        label.size_hint_y = .6
        fl.add_widget(label)
        gl = GridLayout(cols=4, spacing='20dp', size_hint_y=None, size_hint_x=.8)
        gl.pos_hint = {'x': .1, 'y': .5}
        for i in range(3):
            btn = InputButton(device=tab_title, input=str(i+1),
                              message='Selecting input: ' + str(i+1),
                              icon='cave/data/images/computer.png',
                              size_hint_y=None, height='48dp',
                              text='Button ' + str(i+1))
            gl.add_widget(btn)
        fl.add_widget(gl)
        tab.add_widget(fl)
        return tab

    def add_device_tab(self, id, equip=None):
        if equip is None:
            return
        tab = SwipeAccordionItem(title=equip['name'])
        # tab = SwipeAccordionItem(title='accordion_tab_'+str(idx))
        self.ids[id] = tab
        fl = FloatLayout()
        label = Label(text=equip['name'])
        label.pos_hint = {'x': .09, 'y': .5}
        label.font_size = '20dp'
        label.size_hint_x = .8
        label.size_hint_y = .6
        fl.add_widget(label)
        gl = GridLayout(cols=4, spacing='20dp', size_hint_y=None, size_hint_x=.8)
        gl.pos_hint = {'x': .1, 'y': .5}
        for inp in equip['inputs']:
            btn = InputButton(device=equip['id'], input=inp, icon='cave/data/images/blank.png',
                              message='Input {} selected'.format(inp),
                              size_hint_y=None, height='48dp',
                              text=inp)
            gl.add_widget(btn)
        fl.add_widget(gl)
        tab.add_widget(fl)
        self.ids['acc'].add_widget(tab)
        self.app.available_tabs[id] = equip['name']


class TestApp(App):
    location = StringProperty()
    current_tab_id = StringProperty()
    current_tab_title = StringProperty()
    status = StringProperty()
    time = NumericProperty(0)

    def __init__(self):
        super(TestApp, self).__init__()
        self.location = 'Burdick 115'
        self.available_tabs = {}
        self.equip = {}

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        return TestRootWidget(self)

    def go_tab(self, id):
        # Make sure the root window has been created (meaning App.build has returned)
        if self.root is not None:
            tab = self.root.ids[id]
            # Make sure the tab is not already expanded.  If it is, the app will crash.
            if tab.collapse:
                tab.dispatch('on_touch_down', tab)

    def _update_clock(self, *args):
        self.time = time.time()


if __name__ == "__main__":
    TestApp().run()
