from PyQt5.QtWidgets import QWidget, QVBoxLayout

from gui.components.decoded_messages_widget.decoded_messages_table_view import DecodedMessagesTableView


class DecodedMessagesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.decoded_messages_table_view = DecodedMessagesTableView()
        self.main_layout.addWidget(self.decoded_messages_table_view)
