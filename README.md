# cave
Controller for AV Equipment

[Contents]

- cave - a work in progress using Kivy, designed to run on a Raspberry Pi 7" touchscreen
- cave/drivers - equipment drivers - projectors, switchers, tvs

[Installing]

1. git clone https://github.com/tannmatter/cave
2. cd cave && python -m venv venv
3. pip install -r requirements.txt
   (or pip install -r requirements_rpi.txt (for testing on Raspberry Pi systems with GPIO))

[Running]

If running on a Raspberry Pi with 7" touch screen, configure Kivy to run fullscreen in ~/.kivy/config.ini

1. Copy cave/data/example_config.xml to cave/data/config.xml
2. Modify with your own equipment including addresses, ports, input codes, etc.
(You can calculate base64 input codes using driver as reference and base64.b64encode() in python library,
ex. base64.b64encode(b'\x00\x01') returns 'AAE=')
3. source venv/bin/activate
4. python app.py
