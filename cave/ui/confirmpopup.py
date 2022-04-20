from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from cave.ui.commandbutton import Command


class ConfirmPopup(Popup):
    message = StringProperty('')
    command = ObjectProperty(None)

    def __init__(self, message='', command=None, **kwargs):
        super(ConfirmPopup, self).__init__(**kwargs)
        self.message = message
        if not isinstance(command, Command):
            raise Exception('Invalid command object')
        self.command = command

    def okay(self):
        self.command.execute()
        self.dismiss()

    def cancel(self):
        self.dismiss()
