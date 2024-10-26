from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,

)

from gui.components.com_port.com_port_combo_box import ComPortComboBox
from gui.components.message_widget.message_widget import MessageWidget


class LiveModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.__connected_to_serial = False
        self.__sniffing = False

        self.create_actions()

        self.message_widget = MessageWidget(self)
        self.main_layout.addWidget(self.message_widget)

    # noinspection PyAttributeOutsideInit
    # noinspection PyUnresolvedReferences
    def create_actions(self):
        actions_layout = QHBoxLayout()
        self.main_layout.addLayout(actions_layout)

        self.__combo_com_ports = ComPortComboBox()
        actions_layout.addWidget(self.__combo_com_ports)

        self.__btn_connecting = QPushButton("Connect")
        self.__btn_connecting.clicked.connect(self.__on_connecting)
        self.__btn_sniffing = QPushButton("Start Sniffing")
        self.__btn_sniffing.clicked.connect(self.__on_sniffing)

        self.__lbl_can_channel = QLabel("CAN Channel:")
        self.__combo_can_channel = QComboBox()
        self.__combo_can_channel.addItem("CAN_H")
        self.__combo_can_channel.addItem("CAN_M")
        self.__combo_can_channel.addItem("CAN_L")

        actions_layout.addWidget(self.__btn_connecting)
        actions_layout.addWidget(self.__btn_sniffing)
        actions_layout.addWidget(self.__lbl_can_channel)
        actions_layout.addWidget(self.__combo_can_channel)

        self.__update_actions()

    def __update_actions(self):
        if not self.__connected_to_serial:
            self.__btn_connecting.setText("Connect")
            self.__combo_com_ports.setEnabled(True)

            self.__btn_sniffing.setEnabled(False)
            self.__combo_can_channel.setEnabled(False)

        else:
            self.__btn_connecting.setText("Disconnect")
            self.__combo_com_ports.setEnabled(False)
            self.__btn_sniffing.setEnabled(True)

            if not self.__sniffing:
                self.__btn_sniffing.setText("Start Sniffing")
                self.__combo_can_channel.setEnabled(True)
                self.__btn_connecting.setEnabled(True)

            else:
                self.__btn_sniffing.setText("Stop Sniffing")
                self.__btn_connecting.setEnabled(False)
                self.__combo_can_channel.setEnabled(False)

    def __on_connecting(self):
        if not self.__connected_to_serial and self.__combo_com_ports.currentText() == "":
            return

        self.__connected_to_serial = not self.__connected_to_serial
        self.__update_actions()

    def __on_sniffing(self):
        self.__sniffing = not self.__sniffing
        self.__update_actions()
