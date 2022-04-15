import os.path

from kivy.uix.accordion import Accordion
from kivy.uix.accordion import AccordionItem
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from cave.ui.commandbutton import Command, CommandButton
from cave.utils import key_for_value, index_for_key

SWIPE_THRESHOLD = 20


class SwipeAccordion(Accordion):
    def __init__(self, **kwargs):
        self.initial = 0
        super(SwipeAccordion, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_touch_down(self, touch):
        self.initial = touch.x
        return super(SwipeAccordion, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        idx = index_for_key(self.app.available_tabs, self.app.current_tab_id)
        # Swiping right - move a tab to the left
        if touch.x - self.initial > SWIPE_THRESHOLD:
            if idx > 0:
                new_tab_id = list(self.app.available_tabs)[idx-1]
                self.app.go_tab(new_tab_id)
        # Swiping left - move a tab to the right
        elif self.initial - touch.x > SWIPE_THRESHOLD:
            if idx < len(self.app.available_tabs) - 1:
                new_tab_id = list(self.app.available_tabs)[idx+1]
                self.app.go_tab(new_tab_id)
        return super(SwipeAccordion, self).on_touch_up(touch)


class SwipeAccordionItem(AccordionItem):
    def __init__(self, device=None, **kwargs):
        super(SwipeAccordionItem, self).__init__(**kwargs)
        self.app = App.get_running_app()
        if device is None:
            # No device, maybe this is home screen?
            pass
        else:
            device_id = device['id']
            fl = FloatLayout()
            label = Label(text=device['name'])
            label.pos_hint = {'x': .09, 'y': .5}
            label.font_size = '20dp'
            label.size_hint_x = .8
            label.size_hint_y = .6
            fl.add_widget(label)
            gl = GridLayout(cols=4, spacing='20dp', size_hint_y=None, size_hint_x=.8)
            gl.pos_hint = {'x': .1, 'y': .5}
            for input in device['inputs']:
                atlas = "atlas://cave/data/images/myatlas/"
                file = input.casefold().replace(' ', '_')
                icon = atlas+'blank' if not os.path.exists('cave/data/images/'+file+'.png')\
                    else atlas+file
                btn = CommandButton(
                    icon=icon,
                    message='Input {} selected'.format(input),
                    command=Command(
                        self.app.equipment[device_id]['driver'],
                        'select_input',
                        input
                    ),
                    size_hint_y=None, height='48dp',
                    text=input
                )
                gl.add_widget(btn)
            fl.add_widget(gl)
            self.add_widget(fl)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.app.current_tab_title = self.title
            self.app.current_tab_id = key_for_value(self.app.available_tabs, self.title)

        return super(SwipeAccordionItem, self).on_touch_down(touch)
