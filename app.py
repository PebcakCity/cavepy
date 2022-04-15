import importlib
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy.properties import (
    BooleanProperty,
    DictProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty
)

from cave.configreader import ConfigReader
from cave.ui.statusactivityindicator import StatusActivityIndicator
from cave.ui.swipeaccordion import SwipeAccordion, SwipeAccordionItem
from cave.ui.commandbutton import Command, CommandButton


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.app = App.get_running_app()
        self.app.root_widget_created = True

    def add_device_tab(self, equipment_item):
        id = equipment_item['id']
        tab = SwipeAccordionItem(title=equipment_item['name'])
        self.ids[id] = tab
        fl = FloatLayout()
        label = Label(text=equipment_item['name'])
        label.pos_hint = {'x': .09, 'y': .5}
        label.font_size = '20dp'
        label.size_hint_x = .8
        label.size_hint_y = .6
        fl.add_widget(label)
        gl = GridLayout(cols=4, spacing='20dp', size_hint_y=None, size_hint_x=.8)
        gl.pos_hint = {'x': .1, 'y': .5}
        for inp in equipment_item['inputs']:
            input_code_and_icon = equipment_item['inputs'][inp]
            input_code = input_code_and_icon[0]
            icon = input_code_and_icon[1]
            btn = CommandButton(
                icon=icon,
                message='Input {} selected'.format(inp),
                command=Command(
                    self.app.equipment[id]['driver'],
                    'select_input',
                    inp
                ),
                size_hint_y=None, height='48dp',
                text=inp
            )
            gl.add_widget(btn)
        fl.add_widget(gl)
        tab.add_widget(fl)
        self.ids['accordion'].add_widget(tab)
        self.app.available_tabs[id] = equipment_item['name']


class CaveApp(App):
    root_widget_created = BooleanProperty(False)
    time = NumericProperty(0)
    location = StringProperty('')
    equipment = DictProperty({})
    available_tabs = DictProperty({})
    current_tab_id = StringProperty('')
    current_tab_title = StringProperty('')
    status = StringProperty('')

    def __init__(self, **kwargs):
        print('app init')
        super(CaveApp, self).__init__(**kwargs)
        self.config_reader = None

    def on_root_widget_created(self, inst, val):
        print('on_root_widget_created')
        Clock.schedule_once(self.read_config, .1)

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        return RootWidget()

    def _update_clock(self, *args):
        self.time = time.time()

    def read_config(self, *args):
        print('read_config called')
        self.config_reader = ConfigReader()
        if any(self.available_tabs):
            first_tab = list(self.available_tabs)[0]
            self.root.ids[first_tab].dispatch('on_touch_down', self.root.ids[first_tab])

    def go_tab(self, id):
        if self.root is not None:
            tab = self.root.ids[id]
            if tab.collapse:
                tab.dispatch('on_touch_down', tab)

    def on_equipment(self, instance, value):
        print('on_equipment called')
        last_key_added = list(value.keys())[len(value.keys())-1]
        equipment_item = value[last_key_added]

        # Create the driver
        module_path, driver_class_name = equipment_item['driver_path'].rsplit('.', 1)
        module = importlib.import_module(module_path)
        class_ = getattr(module, driver_class_name)

        inputs = {}
        if 'inputs' in equipment_item:
            for input_subkey in equipment_item['inputs']:
                # Each value is a tuple due to the ConfigReader including the icon info it read.
                # Just get the first part of the tuple, which should be the input code
                data = equipment_item['inputs'][input_subkey][0]
                inputs[input_subkey] = data

        if 'comms_method' in equipment_item:
            if equipment_item['comms_method'] == 'serial':
                device, baudrate = equipment_item['comms']
                equipment_item['driver'] = class_(
                    serial_device=device,
                    serial_baudrate=baudrate,
                    # inputs=equipment_item['inputs'],
                    inputs=inputs
                )
            elif equipment_item['comms_method'] == 'ip':
                address, port = equipment_item['comms']
                equipment_item['driver'] = class_(
                    ip_address=address,
                    port=port,
                    # inputs=equipment_item['inputs'],
                    inputs=inputs
                )
        else:
            equipment_item['driver'] = class_(inputs=inputs)

        self.root.add_device_tab(equipment_item)


if __name__ == "__main__":
    CaveApp().run()
