import csv
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from core.can_message.decoded_can_message import DecodedCanMessage
from core.utils import read_file
from gui.components.decoded_messages_widget.decoded_messages_widget import DecodedMessagesWidget
from gui.components.label_dictionary_widget.label_dictionary_widget import LabelDictionaryWidget
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

        self.live_mode_widget = LiveModeWidget()
        self.live_mode_widget.message_widget.message_filter_widget.btn_add_id_label.clicked.connect(
            self.on_clicked_add_id_label)

        self.live_mode_widget.message_widget.message_filter_widget.btn_add_message.clicked.connect(
            self.on_clicked_add_decoded_message
        )

        self.decoded_messages_widget = DecodedMessagesWidget()
        self.label_dictionary_widget = LabelDictionaryWidget()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.live_mode_widget, "&1 Live Mode")
        self.tab_widget.addTab(QWidget(), "&2 Playback Mode")
        self.tab_widget.addTab(self.decoded_messages_widget, "&3 Decoded Messages")
        self.tab_widget.addTab(self.label_dictionary_widget, "&4 Label Dictionary")
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
                "gui/can_sniffer_main_widget.css"
            )
        )

    def on_clicked_add_id_label(self):
        id_ = int(self.live_mode_widget.message_widget.message_filter_widget.line_id.text())
        label = self.live_mode_widget.message_widget.message_filter_widget.line_label.text()
        self.label_dictionary_widget.label_dictionary_view.label_dictionary_model.add_data(id_, label)

    def on_clicked_add_decoded_message(self):
        message = self.live_mode_widget.message_widget.messages_view.get_last_selected_row_message()

        if message:
            decoded_message = DecodedCanMessage(can_message=message.can_message, name="new")
            self.decoded_messages_widget.decoded_messages_table_view.decoded_messages_table_model.add_data(
                decoded_message)
