import base64
import importlib

from kivy.app import App

from xml.etree import ElementTree

from cave.drivers.projector import ProjectorInterface
from cave.drivers.switcher import SwitcherInterface
from cave.drivers.tv import TVInterface


class ConfigReader:
    def __init__(self, root=None, file='cave/data/config.xml'):
        print('ConfigReader init')
        self.app = App.get_running_app()
        self.config = ElementTree.parse(file)
        xml_root = self.config

        # quick and dirty
        self.location = xml_root.find('./location')

        equips = xml_root.findall('./equipment/equip')
        my_equips = {}

        for tag in equips:
            assert('id' in tag.attrib and 'name' in tag.attrib),\
                "Required device attributes 'id' and/or 'name' missing."
            equip = {
                'id': tag.get('id'),
                'name': tag.get('name')
            }

            inputs = tag.find('inputs')
            equip['input_default'] = inputs.get('default')

            inputs_type = inputs.get('type')
            equip['inputs'] = {}
            for input_tag in inputs:
                if 'base64' == inputs_type:
                    equip['inputs'][input_tag.get('name')] = base64.b64decode(input_tag.text.strip())
                elif 'string' == inputs_type:
                    equip['inputs'][input_tag.get('name')] = input_tag.text.strip()
                elif 'numeric' == inputs_type:
                    equip['inputs'][input_tag.get('name')] = int(input_tag.text.strip())
                elif 'bytes' == inputs_type:
                    equip['inputs'][input_tag.get('name')] = input_tag.text.strip().encode()

            if 'serial' in tag.attrib:
                equip['comms_method'] = 'serial'
                if 'baud' in tag.attrib:
                    equip['comms'] = (tag.get('serial'), int(tag.get('baud')))
                else:
                    equip['comms'] = (tag.get('serial'), 9600)
            elif 'ip' in tag.attrib:
                equip['comms_method'] = 'ip'
                if 'port' in tag.attrib:
                    equip['comms'] = (tag.get('ip'), int(tag.get('port')))
                else:
                    equip['comms'] = (tag.get('ip'), 21)

            assert('driver' in tag.attrib), "Required device attribute 'driver' is unspecified."

            equip['driver_path'] = tag.get('driver')

            # at this point, we set app.equipment[equip['id']] to this equip,
            # and continue the loop
            # CaveApp will see this new key added to the dictionary (theoretically)
            # and do everything that used to be done below:

            # driver_path = tag.get('driver')
            # module_path, driver_class_name = driver_path.rsplit('.', 1)
            # module = importlib.import_module(module_path)
            # class_ = getattr(module, driver_class_name)
            #
            # # Instantiate the device's driver
            # # .. equip['driver'] = class_(...)
            # if 'comms_method' in equip:
            #     if equip['comms_method'] == 'serial':
            #         device, baudrate = equip['comms']
            #         equip['driver'] = class_(serial_device=device, serial_baudrate=baudrate, inputs=equip['inputs'])
            #     elif equip['comms_method'] == 'ip':
            #         address, port = equip['comms']
            #         equip['driver'] = class_(ip_address=address, port=port, inputs=equip['inputs'])
            # else:
            #     equip['driver'] = class_(inputs=equip['inputs'])
            #
            # # Add the device to the app's collection of devices
            # my_equips[equip['id']] = equip
            #
            # # Add the device's control tab
            # self.root_widget.add_device_tab(equip['id'], equip)

            self.app.equipment[equip['id']] = equip
