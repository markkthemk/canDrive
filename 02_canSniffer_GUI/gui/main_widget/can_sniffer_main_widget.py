from pathlib import Path

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from core.can_message.decoded_can_message import DecodedCanMessage
from core.project_data import load_sniff
from core.utils import read_file
from gui.decoded_messages_widget.decoded_messages_widget import DecodedMessagesWidget
from gui.label_dictionary_widget.label_dictionary_widget import LabelDictionaryWidget
from gui.live_mode_widget.live_mode_widget import LiveModeWidget


class CanSnifferMainWidget(QWidget):
    def __init__(self, project_location: Path, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.__project_location = project_location

        self.project_data = load_sniff(self.__project_location)

        self.live_mode_widget = LiveModeWidget()
        self.live_mode_widget.message_widget.message_filter_widget.btn_add_id_label.clicked.connect(
            self.on_clicked_add_id_label)

        self.live_mode_widget.message_widget.message_filter_widget.btn_add_message.clicked.connect(
            self.on_clicked_add_decoded_message
        )

        self.decoded_messages_widget = DecodedMessagesWidget(self.project_data.decoded_messages)
        self.label_dictionary_widget = LabelDictionaryWidget(self.project_data.label_dict)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.live_mode_widget, "&1 Live Mode")
        self.tab_widget.addTab(QWidget(), "&2 Playback Mode")
        self.tab_widget.addTab(self.decoded_messages_widget, "&3 Decoded Messages")
        self.tab_widget.addTab(self.label_dictionary_widget, "&4 Label Dictionary")
        self.tab_widget.tabBar().setExpanding(True)
        self.tab_widget.tabBar().setDocumentMode(True)

        self.main_layout.addWidget(self.tab_widget)

        self.__load_styles()

    def __load_styles(self):
        self.setStyleSheet(read_file("gui/main_widget/can_sniffer_main_widget.css"))

    def on_clicked_add_id_label(self):
        text = self.live_mode_widget.message_widget.message_filter_widget.line_id.text()
        if text:
            id_ = int(text)
            label = self.live_mode_widget.message_widget.message_filter_widget.line_label.text()
            self.label_dictionary_widget.label_dictionary_view.label_dictionary_model.add_data(id_, label)

    def on_clicked_add_decoded_message(self):
        message = self.live_mode_widget.message_widget.messages_view.get_last_selected_row_message()

        if message:
            decoded_message = DecodedCanMessage(can_message=message.can_message, name="new")
            self.decoded_messages_widget.decoded_messages_table_view.decoded_messages_table_model.add_data(
                decoded_message)
