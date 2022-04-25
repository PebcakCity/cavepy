import importlib
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from kivy.properties import (
    BooleanProperty,
    DictProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty
)

from cave.configreader import ConfigReader
from cave.ui.statusactivityindicator import StatusActivityIndicator
from cave.ui.deviceaccordion import DeviceAccordion, DeviceTab
from cave.ui.commandbutton import Command, CommandButton
from cave.ui.confirmpopup import ConfirmPopup


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.app = App.get_running_app()
        self.app.root_widget_created = True

    def add_device_tab(self, equipment_item):
        id = equipment_item['id']
        tab = DeviceTab(equipment_item, title=equipment_item['name'])
        self.ids[id] = tab
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
        super(CaveApp, self).__init__(**kwargs)
        self.config_reader = ConfigReader()

    def on_root_widget_created(self, inst, val):
        Clock.schedule_once(self.read_config, .1)

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        return RootWidget()

    def _update_clock(self, *args):
        self.time = time.time()

    def read_config(self, *args):
        self.config_reader.parse()
        # Select the first available tab to set app.current_tab_title & id
        if any(self.available_tabs):
            first_tab = list(self.available_tabs)[0]
            self.root.ids[first_tab].dispatch('on_touch_down', self.root.ids[first_tab])

    def go_tab(self, id):
        if self.root is not None:
            tab = self.root.ids[id]
            if tab.collapse:
                tab.dispatch('on_touch_down', tab)

    def go_home(self):
        if len(self.available_tabs) > 0:
            self.go_tab(list(self.available_tabs.keys())[0])

    def on_equipment(self, instance, value):
        last_key_added = list(value.keys())[len(value.keys())-1]
        device = value[last_key_added]

        # Create the driver
        module_path, driver_class_name = device['driver_path'].rsplit('.', 1)
        module = importlib.import_module(module_path)
        class_ = getattr(module, driver_class_name)

        if 'connection' in device:
            if device['connection'] == 'serial':
                ser_io, baudrate = device['comms']
                device['driver'] = class_(
                    serial_device=ser_io,
                    serial_baudrate=baudrate,
                    inputs=device['inputs']
                )
            elif device['connection'] == 'ip':
                address, port = device['comms']
                device['driver'] = class_(
                    ip_address=address,
                    port=port,
                    inputs=device['inputs']
                )
        else:
            device['driver'] = class_(inputs=device['inputs'])
        self.root.add_device_tab(device)

    def update_status(self, text):
        self.status = text
        Clock.schedule_once(self.clear_status, 10)

    def clear_status(self, *args):
        self.status = ''
        self.root.ids['sai'].stop()

    def power_on_pressed(self):
        title = self.current_tab_title
        confirm = ConfirmPopup(
            title=title,
            message="Power on device '{}'?".format(title),
            command=Command(self, 'power_device_on')
        )
        confirm.open()

    def power_device_on(self):
        # Get the device for the current tab (or None)
        device = self.equipment.get(self.current_tab_id)
        try:
            if device is not None and 'driver' in device:
                power_on = getattr(device['driver'], 'power_on')
                if power_on():
                    self.root.ids['sai'].start()
                    self.update_status('Making it so...')
        except Exception as e:
            print('Exception: {}'.format(e.args))
            self.update_status(str(e.args[0]))

    def power_off_pressed(self):
        title = self.current_tab_title
        confirm = ConfirmPopup(
            title=title,
            message="Do you really want to power OFF device '{}'?".format(title),
            command=Command(self, 'power_device_off')
        )
        confirm.open()

    def power_device_off(self):
        device = self.equipment.get(self.current_tab_id)
        try:
            if device is not None and 'driver' in device:
                power_off = getattr(device['driver'], 'power_off')
                if power_off():
                    # self.root.ids['sai'].stop()
                    self.update_status('Shutting off display...')
        except Exception as e:
            print('Exception: {}'.format(e.args))
            self.update_status(str(e.args[0]))


if __name__ == "__main__":
    CaveApp().run()
