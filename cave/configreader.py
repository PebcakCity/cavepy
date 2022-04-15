import base64
from kivy.app import App
from xml.etree import ElementTree


class ConfigReader:
    def __init__(self, file='cave/data/config.xml'):
        self.config = file
        self.app = App.get_running_app()

    def parse(self):
        print('ConfigReader reading file {}'.format(self.config))
        xml_root = ElementTree.parse(self.config)
        self.app.location = xml_root.find('./location').text
        equips = xml_root.findall('./equipment/equip')

        for tag in equips:
            assert('id' in tag.attrib and 'name' in tag.attrib),\
                "Required device attributes 'id' and/or 'name' missing."
            device = {
                'id': tag.get('id'),
                'name': tag.get('name')
            }
            inputs = tag.find('inputs')
            device['input_default'] = inputs.get('default')

            inputs_type = inputs.get('type')
            device['inputs'] = {}
            for input_tag in inputs:
                input_name = input_tag.get('name')
                if inputs_type == 'base64':
                    device['inputs'][input_name] = base64.b64decode(input_tag.text.strip())
                elif inputs_type == 'string':
                    device['inputs'][input_name] = input_tag.text.strip()
                elif inputs_type == 'numeric':
                    device['inputs'][input_name] = int(input_tag.text.strip())
                elif inputs_type == 'bytes':
                    device['inputs'][input_name] = input_tag.text.strip().encode()

            if 'serial' in tag.attrib:
                device['connection'] = 'serial'
                if 'baud' in tag.attrib:
                    device['comms'] = (tag.get('serial'), int(tag.get('baud')))
                else:
                    device['comms'] = (tag.get('serial'), 9600)
            elif 'ip' in tag.attrib:
                device['connection'] = 'ip'
                if 'port' in tag.attrib:
                    device['comms'] = (tag.get('ip'), int(tag.get('port')))
                else:
                    device['comms'] = (tag.get('ip'), 21)

            assert('driver' in tag.attrib), "Required device attribute 'driver' is unspecified."
            device['driver_path'] = tag.get('driver')
            self.app.equipment[device['id']] = device
