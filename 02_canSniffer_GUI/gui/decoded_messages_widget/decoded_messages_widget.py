from PyQt5.QtWidgets import QWidget, QVBoxLayout

from gui.decoded_messages_widget.decoded_messages_table_view import DecodedMessagesTableView


class DecodedMessagesWidget(QWidget):
    def __init__(self, decoded_messages_list, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.decoded_messages_table_view = DecodedMessagesTableView(decoded_messages_list)
        self.main_layout.addWidget(self.decoded_messages_table_view)
