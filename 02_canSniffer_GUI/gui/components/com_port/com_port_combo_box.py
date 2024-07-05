from PyQt5.QtWidgets import QComboBox

from gui.components.com_port.com_port_list_model import ComPortListModel
from gui.components.com_port.com_port_thread import ComPortsThread


class ComPortComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.combo_model = ComPortListModel()
        self.setModel(self.combo_model)

        self.com_port_thread = ComPortsThread(self.combo_model)
        self.com_port_thread.start()

    def __del__(self):
        self.com_port_thread.stop()
