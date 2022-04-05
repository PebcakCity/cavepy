from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import StringProperty


class InputButton(Button):
    message = StringProperty()
    icon = StringProperty()

    def __init__(self, device=None, input='', icon='', message='',  **kwargs):
        super(InputButton, self).__init__(**kwargs)
        self._device_id = device
        self._input = input
        self.message = message
        self.icon = icon

    def on_release(self):
        app = App.get_running_app()

        # ..
        # app.equip[self._device_id].select_input(self._input)
        # ..

        tab = app.current_tab_name
        popup = app.root.ids['popup']
        popup_label = app.root.ids['popup_label']
        popup.title = tab
        popup_label.text = self.message
        popup.open()
