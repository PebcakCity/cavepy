from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import StringProperty


class IconButton(Button):
    message = StringProperty()
    icon = StringProperty()

    def __init__(self, msg='', icn='', **kwargs):
        self.message = msg
        self.icon = icn
        super(IconButton, self).__init__(**kwargs)

    def on_release(self):
        app = App.get_running_app()
        tab = app.current_tab_name
        popup = app.root.ids['popup']
        popup_label = app.root.ids['popup_label']
        popup.title = tab
        popup_label.text = self.message
        popup.open()
