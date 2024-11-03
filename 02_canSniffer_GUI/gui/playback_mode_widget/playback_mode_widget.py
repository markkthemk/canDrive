from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox

from core.project_data import ProjectData
from gui.components.message_widget.message_widget import MessageWidget


class PlaybackModeWidget(QWidget):
    def __init__(self, project_data: ProjectData = ProjectData(), parent=None):
        super().__init__(parent=parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.__connected_to_serial = False
        self.__sniffing = False

        self.create_actions()

        self.message_widget = MessageWidget(project_data)
        self.main_layout.addWidget(self.message_widget)

    def create_actions(self):
        actions_layout = QHBoxLayout()
        self.main_layout.addLayout(actions_layout)

        self.__btn_open_file = QPushButton("Open session")
        self.__btn_open_file.clicked.connect(self.__on_open_file)

        self.__btn_start_stop_playack = QPushButton("Start playback")
        self.__btn_start_stop_playack.clicked.connect(self.__on_start_stop_playack)

        self.__lbl_playback_delay = QLabel("Playback delay:")
        self.__spin_playback_delay = QSpinBox()

        actions_layout.addWidget(self.__btn_open_file)
        actions_layout.addWidget(self.__btn_start_stop_playack)
        actions_layout.addWidget(self.__lbl_playback_delay)
        actions_layout.addWidget(self.__spin_playback_delay)

    def __on_open_file(self):
        print("__on_open_file")

    def __on_start_stop_playack(self):
        print("__on_start_stop_playack")
