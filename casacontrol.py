# (C) Copyright 2014 Pascal Bach <pascal.bach@nextrem.ch>
#
# SPDX-License-Identifier:     MIT
#

from urllib.request import urlopen
from time import sleep
from html.parser import HTMLParser

class CasaControl:
    def __init__(self, ip, sn):
        self.addr="http://%s" % ip
        self.sn = sn

    def PowerPlug(self, addr):
        return PowerPlug(self, addr)


class PowerPlug:
    def __init__(self, server, addr):
        """
        To communicate with a casa control base station you need to know the
        it's IP address and it's serial number

        >>> c = CasaControl("192.168.0.123", "023456789000")

        now you can create an associated device like a power plug with a desired address

        >>> p0 = c.PowerPlug(0)

        this will create a PowerPlug object with the address 0

        """
        self.server = server
        self.addr = addr
        

    def pair(self):
        """
        To pair a device you need to push the button on the device until the led starts to blink

        then execute the pairing sequence on the device with the desired address

        >>> p0.pair()

        After this is done the device will be associated with the given address till it is paired again differently.
        """
        self.on()
        self.off()
        print("Paired %02x" % self.addr)


    def on(self):
        """
        The on command is 0x11 and it is the last part of the command string

        to switch on a device

        >>> p0.on()

        """
        return self.send(0x11)

    def off(self):
        """
        The off command is 0x12 and it is the last part of the command string

        to switch on a device

        >>> p0.off()

        """
        return self.send(0x12)


    def send(self, command):
        """

        A command has the following structure:

            All entries are in hex
            :<edition>:<device>:<?>:<command>
            edition = 0x01|0x02 probably the model 0x01=basic, 0x02=premium
            device = 0x00-0xff number of the device, multiple plugs can be registered to the same address
            ? = 00 seems to only work if 00
            command = 0x11|0x12 for powerplugs 0x11=ON, 0x12=OFF

        """
        command_t = ":02:%02x:00:%02x"

        command = command_t % (self.addr, command)
        print(command)
        urlopen("%s/txcomm.asp" % self.server.addr)
        res=urlopen("%s/goform/commtx?command=%s&serialn=%s" % (self.server.addr, command, self.server.sn))
        class ResponseHTML(HTMLParser):
            found=False
            value=""
            def handle_starttag(self, tag, attrs):
                if tag == "h2":
                    self.found=True
            def handle_endtag(self, tag):
                if tag == "h2":
                    self.found=False
            def handle_data(self, data):
                if self.found:
                    self.value=data

        p = ResponseHTML()
        p.feed(res.read().decode("utf-8"))
        return int(p.value)
