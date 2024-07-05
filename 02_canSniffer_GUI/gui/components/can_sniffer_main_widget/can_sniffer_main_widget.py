import csv
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from core.utils import read_file
from gui.components.live_mode_widget.live_mode_widget import LiveModeWidget


class CanSnifferMainWidget(QWidget):
    def __init__(self, project_location: Path, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.__project_location = project_location
        print(self.__project_location)

        self.__id_labels = []
        self.__decoded_messages = []

        self.__id_labels_csv = Path(self.__project_location / "id_labels.csv")
        self.__decoded_messages_csv = Path(
            self.__project_location / "decoded_messages.csv"
        )

        self.load_csv(self.__id_labels_csv, self.__id_labels)
        self.load_csv(self.__decoded_messages_csv, self.__decoded_messages)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(LiveModeWidget(), "&1 Live Mode")
        self.tab_widget.addTab(QWidget(), "&2 Playback Mode")
        self.tab_widget.addTab(QWidget(), "&3 Decoded Messages")
        self.tab_widget.addTab(QWidget(), "&4 Label Dictionary")
        self.tab_widget.tabBar().setExpanding(True)
        self.tab_widget.tabBar().setDocumentMode(True)

        self.main_layout.addWidget(self.tab_widget)

        self.__load_styles()

    @staticmethod
    def load_csv(path: Path, container: list):
        if path.exists():
            with open(str(path), "r") as stream:
                for row_data in csv.reader(stream):
                    container.append(row_data)

    def __load_styles(self):
        self.setStyleSheet(
            read_file(
                "gui/components/can_sniffer_main_widget/can_sniffer_main_widget.css"
            )
        )
