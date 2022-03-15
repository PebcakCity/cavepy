from kivy.properties import NumericProperty
from kivy.uix.progressbar import ProgressBar


class StatusProgressBar(ProgressBar):
    """Frankly I'm surprised that this works.  We bind self.time to app.time in the .kv file,
    and then on call of self.start(), self.time is bound to a function which updates the value
    of the ProgressBar as the time changes.  self.stop() undoes this binding and resets the
    value of the ProgressBar to zero.  The result is a progress bar that is constantly
    "spinning" once start() is called until stop() is later called.
    """
    time = NumericProperty(0)

    def __init__(self, **kwargs):
        super(StatusProgressBar, self).__init__(**kwargs)

    def start(self):
        self.bind(time=self.time_callback)

    def stop(self):
        self.unbind(time=self.time_callback)
        self.value = 0

    def time_callback(self, *args):
        self.value = (self.time * 30) % 100
