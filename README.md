# cavepy
Controller for AV Equipment

[Contents]

- cavepy - a work in progress using Kivy, designed to run on a Raspberry Pi 7" touchscreen
- cavepy/drivers - equipment drivers - projectors, switchers, tvs

[Installing]

1. git clone https://github.com/tannmatter/cavepy
2. cd cavepy && python -m venv venv
3. pip install -r requirements.txt
   (or pip install -r requirements_rpi.txt (for testing on Raspberry Pi systems with GPIO))

[Running]

If running on a Raspberry Pi with 7" touch screen, configure Kivy to run fullscreen in ~/.kivy/config.ini

1. Copy cavepy/data/example_config.xml to cavepy/data/config.xml
2. Modify with your own equipment including addresses, ports, input codes, etc.
(You can calculate base64 input codes using driver as reference and base64.b64encode() in python library,
ex. base64.b64encode(b'\x00\x01') returns 'AAE=')
3. source venv/bin/activate
4. python app.py
