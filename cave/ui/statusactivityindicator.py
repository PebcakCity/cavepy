from kivy.properties import NumericProperty
from kivy.uix.progressbar import ProgressBar


class StatusActivityIndicator(ProgressBar):
    """Bind time property to app.time in the .kv file.  On call of self.start()
    time is also bound to a callback which continually updates the value of the
    ProgressBar component as the time updates.  self.stop() undoes this binding
    and resets the value of the ProgressBar component to zero.  The result is a
    progress bar that is constantly looping once start() is called until stop()
    is called.
    """
    time = NumericProperty(0)

    def __init__(self, **kwargs):
        super(StatusActivityIndicator, self).__init__(**kwargs)

    def start(self):
        self.bind(time=self.time_callback)

    def stop(self):
        self.unbind(time=self.time_callback)
        self.value = 0

    def time_callback(self, *args):
        self.value = (self.time * 30) % 100
