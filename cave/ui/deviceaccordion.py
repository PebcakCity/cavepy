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
            self.build_input_buttons(device)
            if device.get('type') == 'television':
                self.build_channel_buttons(device)
                self.build_volume_controls(device)

    def build_input_buttons(self, device):
        atlas_file, atlas_url = \
            "cave/data/images/myatlas.atlas", \
            "atlas://cave/data/images/myatlas/"
        with open(atlas_file) as fp:
            atlas_data = json.load(fp)

        for input in device['inputs']:
            file = input.casefold().replace(' ', '_')
            # Check atlas file to see if icon exists for this input
            icon = atlas_url + 'blank' if file not in atlas_data['myatlas-0.png'] \
                else atlas_url + file
            btn = CommandButton(
                icon=icon,
                message='Input {} selected'.format(input),
                command=Command(
                    device['driver'],
                    'select_input',
                    input
                ),
                size_hint_y=None, height='48dp',
                text=input
            )
            self.ids['button_panel_center'].add_widget(btn)

    def build_channel_buttons(self, device):
        btn_ch_up = CommandButton(
            background_normal='atlas://cave/data/images/myatlas/arrow_up_normal',
            background_down='atlas://cave/data/images/myatlas/arrow_up_down',
            message='Channel up',
            command=Command(
                device['driver'],
                'channel_up'
            ),
            size_hint_y=None, height='48dp',
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .5},
            width='64dp',
            text=''
        )
        btn_ch_dn = CommandButton(
            background_normal='atlas://cave/data/images/myatlas/arrow_down_normal',
            background_down='atlas://cave/data/images/myatlas/arrow_down_down',
            icon='atlas://cave/data/images/myatlas/blank',
            message='Channel down',
            command=Command(
                device['driver'],
                'channel_dn'
            ),
            size_hint_y=None, height='48dp',
            size_hint_x=None,
            pos_hint={'center_x': .5, 'center_y': .5},
            width='64dp',
            text=''
        )
        self.ids['button_panel_left'].add_widget(btn_ch_up)
        self.ids['button_panel_left'].add_widget(btn_ch_dn)

    def build_volume_controls(self, device):
        btn_vol_up = CommandButton(
            background_normal='atlas://cave/data/images/myatlas/plus_normal',
            background_down='atlas://cave/data/images/myatlas/plus_down',
            message='Volume up',
            command=Command(
                device['driver'],
                'volume_up'
            ),
            size_hint_y=None, height='48dp',
            size_hint_x=None,
            pos_hint={'center_x': .5},
            width='64dp',
            text=''
        )
        btn_vol_dn = CommandButton(
            background_normal='atlas://cave/data/images/myatlas/minus_normal',
            background_down='atlas://cave/data/images/myatlas/minus_down',
            message='Volume down',
            command=Command(
                device['driver'],
                'volume_dn'
            ),
            size_hint_y=None, height='48dp',
            size_hint_x=None,
            pos_hint={'center_x': .5},
            width='64dp',
            text=''
        )
        self.ids['button_panel_right'].add_widget(btn_vol_up)
        self.ids['button_panel_right'].add_widget(btn_vol_dn)
