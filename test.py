from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty

from cave.ui.iconbutton import IconButton
from cave.ui.swipeaccordion import SwipeAccordion, SwipeAccordionItem


class TestRootWidget(BoxLayout):
    def __init__(self, app, **kwargs):
        super(TestRootWidget, self).__init__(**kwargs)
        self.app = app
        self.build_accordion()

    def build_accordion(self):
        acc = self.ids['acc']
        for idx, tab_title in enumerate(self.app.available_tabs):
            tab = self.build_accordion_tab(idx, tab_title)
            acc.add_widget(tab)
        # select first (home) tab
        self.ids['accordion_tab_0'].dispatch('on_touch_down', self.ids['accordion_tab_0'])

    def build_accordion_tab(self, idx=0, tab_title=''):
        tab = SwipeAccordionItem(title=tab_title)
        self.ids['accordion_tab_' + str(idx)] = tab
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
            btn = IconButton(msg='This is a message from button #' + str(i + 1),
                             icn='cave/data/images/keyboard.png', size_hint_y=None, height='48dp',
                             text='Button ' + str(i + 1))
            gl.add_widget(btn)
        fl.add_widget(gl)
        tab.add_widget(fl)
        return tab


class TestApp(App):
    current_tab_name = StringProperty()

    def __init__(self):
        self.available_tabs = ['Home', 'Projector', 'Switcher']
        super(TestApp, self).__init__()

    def build(self):
        return TestRootWidget(self)

    def go_tab(self, idx):
        # Make sure the root window has been created (meaning App.build has returned)
        if self.root is not None:
            tab = self.root.ids['accordion_tab_' + str(idx)]
            # Make sure the tab is not already expanded.  If it is, the app will crash.
            if tab.collapse:
                tab.dispatch('on_touch_down', tab)


if __name__ == "__main__":
    TestApp().run()
