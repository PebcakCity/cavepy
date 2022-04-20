from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class Command:
    def __init__(self, obj=None, mthd=None, *args):
        self._object = obj
        self._method = mthd
        self._args = args

    def execute(self):
        if self._object is not None and self._method is not None:
            method = getattr(self._object, self._method)
            return method(*self._args)
        elif self._args is not None:
            print(*self._args)


class CommandButton(Button):
    icon = StringProperty('')
    message = StringProperty('')
    command = ObjectProperty(None)

    def __init__(self, icon='', message='', **kwargs):
        super(CommandButton, self).__init__(**kwargs)
        self.icon = icon
        self.message = message
        self.app = App.get_running_app()

    def on_release(self):
        try:
            if self.command is not None:
                self.command.execute()
        except Exception as e:
            self.app.update_status(e.args[0])
        else:
            self.app.update_status(self.message)
