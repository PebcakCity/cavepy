from kivy.uix.accordion import Accordion
from kivy.uix.accordion import AccordionItem
from kivy.app import App

from cave.utils import (
    key_for_value,
    index_for_key,
    index_for_value
)

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
    def __init__(self, **kwargs):
        super(SwipeAccordionItem, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.app.current_tab_title = self.title
            self.app.current_tab_id = key_for_value(self.app.available_tabs, self.title)

        return super(SwipeAccordionItem, self).on_touch_down(touch)
