#!/usr/bin/env python
"""
i2cvisualiser.py
Provides a simple GUI for reading and writing bytes to and from the i2c
interface
"""
import pygtk
pygtk.require("2.0")
import gtk
from datetime import datetime
import smbus

WINDOW_TITLE = "I2C Visualiser"


# exceptions
class FormatError(Exception):
    pass

# classes
class I2CVisualiser(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)

        # controls
        self.addr_label = gtk.Label("Address:")
        self.addr_entry = gtk.Entry()
        self.read_button = gtk.Button("Read")
        self.read_button.connect("clicked", self.read_button_clicked)

        self.addr_label.show()
        self.addr_entry.show()
        self.read_button.show()

        top_hbox = gtk.HBox()
        top_hbox.pack_start(self.addr_label, False)
        top_hbox.pack_start(self.addr_entry, False)
        top_hbox.pack_start(self.read_button)
        top_hbox.show()
        self.pack_start(top_hbox, False)

        self.value_label = gtk.Label("Value:")
        self.value_entry = gtk.Entry()
        self.write_button = gtk.Button("Write")
        self.write_button.connect("clicked", self.write_button_clicked)

        self.value_label.show()
        self.value_entry.show()
        self.write_button.show()

        bottom_hbox = gtk.HBox()
        bottom_hbox.pack_start(self.value_label, False)
        bottom_hbox.pack_start(self.value_entry, False)
        bottom_hbox.pack_start(self.write_button)
        bottom_hbox.show()
        self.pack_start(bottom_hbox, False)

        # log window
        textview = gtk.TextView()
        textview.show()
        textview.set_editable(False)

        self.logbuffer = textview.get_buffer()

        scrolledwindow = gtk.ScrolledWindow(hadjustment=None)
        scrolledwindow.add_with_viewport(textview)
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scrolledwindow.show()
        self.pack_end(scrolledwindow)

        self.show()

    def append_to_log(self, text):
        """Appends the text given to the end of the log window"""
        enditer = self.logbuffer.get_end_iter()
        time = datetime.now()
        strtime = "%02d:%02d:%02d" % (time.hour, time.minute, time.second)
        self.logbuffer.insert(enditer, "%s: %s\n" % (strtime, text))

    def get_address(self):
        """Returns the address as an integer"""
        addr_str = self.addr_entry.get_text()
        try:
            if "0x" in addr_str:
                address = int(addr_str, 16)
            elif "0b" in addr_str:
                address = int(addr_str, 2)
            else:
                address = int(addr_str)
        except ValueError:
            raise FormatError("Please enter a valid address (format: dec/hex/bin).")
        else:
            return address

    def get_value(self):
        """Returns the address as an integer"""
        value_str = self.value_entry.get_text()
        try:
            if "0x" in value_str:
                value = int(value_str, 16)
            elif "0b" in value_str:
                value = int(value_str, 2)
            else:
                value = int(value_str)
        except ValueError:
            raise FormatError("Please enter a valid value (format: dec/hex/bin).")
        else:
            return value

    def read_i2c(self, address):
        """Returns the byte at the address specified"""
        #return 42 # stub for now
        bus = smbus.SMBus(0)
        return bus.read_byte(address)

    def write_i2c(self, address, value):
        """Returns the byte at the address specified"""
        #pass # stub
        bus = smbus.SMBus(0)
        bus.write_byte(address, value)

    def show_error(self, err_message):
        msgdiag = gtk.MessageDialog(None,
                gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,
                gtk.BUTTONS_OK, err_message)
        msgdiag.run()
        msgdiag.destroy()

    def read_button_clicked(self, widget, data=None):
        """Performs an I2C read and prints it to the log"""
        try:
            address = self.get_address()
        except FormatError as e:
            self.show_error(str(e))
        else:
            i2c_ret_value = self.read_i2c(address)
            self.append_to_log("Reading address %s => %s" % (hex(address), i2c_ret_value))

    def write_button_clicked(self, widget, data=None):
        """Performs an I2C read and prints it to the log"""
        try:
            address = self.get_address()
            value   = self.get_value()
        except FormatError as e:
            self.show_error(str(e))
        else:
            self.write_i2c(address, value)
            self.append_to_log("Writing address %s => %s" % (hex(address), value))
        

def main():
    w = gtk.Window()
    w.connect("delete-event", gtk.main_quit)
    w.set_title(WINDOW_TITLE)
    w.add(I2CVisualiser())
    w.show()
    gtk.main()

if __name__ == "__main__":
    main()
