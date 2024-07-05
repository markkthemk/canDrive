import serial.tools.list_ports
from PyQt5.QtCore import QThread

from gui.components.com_port.com_port_list_model import ComPortListModel


class ComPortsThread(QThread):
    def __init__(self, com_port_model: ComPortListModel):
        super().__init__()
        self.is_running = False
        self.com_port_model = com_port_model

    def stop(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            com_ports = serial.tools.list_ports.comports()
            name_list = list(port.device for port in com_ports)
            self.com_port_model.update_data(name_list)
            self.msleep(500)
