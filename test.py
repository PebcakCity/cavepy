from kivy.uix.accordion import Accordion
from kivy.uix.accordion import AccordionItem
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window


# Todo - find a reliable way to determine whether this is running on a Raspberry Pi
Window.fullscreen = True


class MyAccordion(Accordion):
    def __init__(self, **kwargs):
        self.current_tab_name = ''
        super(MyAccordion, self).__init__(**kwargs)


class MyAccordionItem(AccordionItem):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.accordion.current_tab_name = self.title
            app = App.get_running_app()
            app.current_tab_name = self.title

        return super(MyAccordionItem, self).on_touch_down(touch)


class MyInputButton(Button):
    message = StringProperty()

    def __init__(self, msg='', **kwargs):
        self.message = msg
        super(MyInputButton, self).__init__(**kwargs)

    def on_release(self):
        app = App.get_running_app()
        tab = app.current_tab_name
        popup = app.root.ids['popup']
        popup_label = app.root.ids['popup_label']
        popup.title = tab
        popup_label.text = self.message
        popup.open()


class TestRootWidget(BoxLayout):
    def __init__(self, app, **kwargs):
        super(TestRootWidget, self).__init__(**kwargs)
        self.app = app
        self.build_accordion()

    def build_accordion(self):
        acc = MyAccordion()
        self.ids['accordion'] = acc
        acc.orientation = 'horizontal'
        for idx, tab_name in enumerate(self.app.available_tabs):
            item = MyAccordionItem(title=tab_name)
            self.ids['accordion_item_'+str(idx)] = item
            fl = FloatLayout()
            label = Label(text=tab_name)
            label.pos_hint = {'x': .09, 'y': .5}
            label.font_size = '20dp'
            label.size_hint_x = .8
            label.size_hint_y = .6
            fl.add_widget(label)
            gl = GridLayout(cols=4, spacing='20dp', size_hint_y=None, size_hint_x=.8)
            gl.pos_hint = {'x': .1, 'y': .5}
            for i in range(3):
                btn = MyInputButton(message='This is a message from button #'+str(i+1),
                                    size_hint_y=None, height='48dp', text='Button '+str(i+1))
                gl.add_widget(btn)
            fl.add_widget(gl)
            item.add_widget(fl)
            acc.add_widget(item)
        self.add_widget(acc)
        # select first (home) tab
        self.ids['accordion_item_0'].dispatch('on_touch_down', self.ids['accordion_item_0'])


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
            item = self.root.ids['accordion_item_'+str(idx)]
            # Make sure the tab is not already expanded.  If it is, the app will crash.
            if item.collapse:
                item.dispatch('on_touch_down', item)


if __name__ == "__main__":
    TestApp().run()
