from kivy.uix.accordion import Accordion
from kivy.uix.accordion import AccordionItem
from kivy.app import App

SWIPE_THRESHOLD = 20


class SwipeAccordion(Accordion):
    def __init__(self, **kwargs):
        self.current_tab_name = ''
        self.initial = 0
        super(SwipeAccordion, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        self.initial = touch.x
        return super(SwipeAccordion, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        app = App.get_running_app()
        idx = app.available_tabs.index(app.current_tab_name)
        # Swiping right - move a tab to the left
        if touch.x - self.initial > SWIPE_THRESHOLD:
            if idx > 0:
                app.go_tab(idx - 1)
        # Swiping left - move a tab to the right
        elif self.initial - touch.x > SWIPE_THRESHOLD:
            if idx < len(app.available_tabs) - 1:
                app.go_tab(idx + 1)
        return super(SwipeAccordion, self).on_touch_up(touch)


class SwipeAccordionItem(AccordionItem):
    def __init__(self, **kwargs):
        super(SwipeAccordionItem, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.accordion.current_tab_name = self.title
            app = App.get_running_app()
            app.current_tab_name = self.title

        return super(SwipeAccordionItem, self).on_touch_down(touch)
