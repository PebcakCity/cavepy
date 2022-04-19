import json

from kivy.app import App
from kivy.properties import StringProperty

from cave.ui.swipeaccordion import SwipeAccordion, SwipeAccordionItem
from cave.ui.commandbutton import CommandButton, Command


class DeviceAccordion(SwipeAccordion):
    def __init__(self, **kwargs):
        super(DeviceAccordion, self).__init__(**kwargs)


class DeviceTab(SwipeAccordionItem):
    device_id = StringProperty('')

    def __init__(self, device=None, **kwargs):
        super(DeviceTab, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.device_id = device['id'] if device else None
        if device is None:
            # No device, maybe this is home screen?
            pass
        else:
            atlas_file, atlas_url = \
                "cave/data/images/myatlas.atlas",\
                "atlas://cave/data/images/myatlas/"
            with open(atlas_file) as fp:
                atlas_data = json.load(fp)

            for input in device['inputs']:
                file = input.casefold().replace(' ', '_')
                # Check atlas file to see if icon exists for this input
                icon = atlas_url+'blank' if file not in atlas_data['myatlas-0.png']\
                    else atlas_url+file
                btn = CommandButton(
                    icon=icon,
                    message='Input {} selected'.format(input),
                    command=Command(
                        self.app.equipment[self.device_id]['driver'],
                        'select_input',
                        input
                    ),
                    size_hint_y=None, height='48dp',
                    text=input
                )
                self.ids['inputs_grid'].add_widget(btn)
