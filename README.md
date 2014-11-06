casacontrol.py
==============

A small python library that allows to communicate with the Casa Control system http://www.casacontrol.info/

usage
-----

``
from casacontrol import CasaControl

# sn is the serial number of the base station
c = CasaControl("192.168.0.123", sn="023456789000")

p = c.PowerPlug(0)

# Now press the button on the device until it starts to blink
p.pair()

p.on()
p.off()
``