from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from core.message_table_model.message_table_filter import COLUMN_ID
from gui.components.message_widget.message_filter_widget import MessageFilterWidget
from gui.components.message_widget.message_table_view import MessageTableView


class MessageWidget(QWidget):
    """A Widget with a table view and a filter section for the table"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.messages_view = MessageTableView()
        self.main_layout.addWidget(self.messages_view)

        self.message_filter_widget = MessageFilterWidget(self)
        self.main_layout.addWidget(self.message_filter_widget)

        self.message_filter_widget.btn_clear_table.clicked.connect(self.clear_table)
        self.message_filter_widget.chk_group_packets.clicked.connect(
            self.messages_view.filter_proxy.set_group_packets)
        self.message_filter_widget.chk_highlight_new_packets.stateChanged.connect(
            self.messages_view.messages_model.set_highlight_new_packets)
        self.message_filter_widget.chk_highlight_new_values.stateChanged.connect(
            self.messages_view.messages_model.set_highlight_new_values)
        self.message_filter_widget.chk_hide_packets_older_than.clicked.connect(
            self.messages_view.filter_proxy.set_hide_packets_older_than)
        self.message_filter_widget.spin_hide_packets_older_than.valueChanged.connect(
            self.messages_view.filter_proxy.set_hide_packets_older_than_value)
        self.message_filter_widget.chk_show_packets_with_the_following_id.stateChanged.connect(
            self.messages_view.filter_proxy.set_show_packets_with_id)
        self.message_filter_widget.line_show_packets_with_the_following_ids.textChanged.connect(
            self.messages_view.filter_proxy.set_show_packets_with_id_vales)
        self.message_filter_widget.chk_hide_packets_with_the_following_id.stateChanged.connect(
            self.messages_view.filter_proxy.set_hide_packets_with_id)
        self.message_filter_widget.line_hide_packets_with_the_following_ids.textChanged.connect(
            self.messages_view.filter_proxy.set_hide_packets_with_id_vales)

        self.messages_view.set_show_ids.connect(self.on_set_show_ids)
        self.messages_view.set_hide_ids.connect(self.on_set_hide_ids)

        self.messages_view.clicked.connect(self.on_clicked_message)

    def clear_table(self, *args):
        print("clear_table", args)

    def on_set_show_ids(self, ids):
        str_ids = " ".join([f"{ide}" for ide in ids])
        self.message_filter_widget.line_show_packets_with_the_following_ids.setText(str_ids)
        self.message_filter_widget.chk_show_packets_with_the_following_id.setChecked(True)

    def on_set_hide_ids(self, ids):
        str_ids = " ".join([f"{ide}" for ide in ids])
        self.message_filter_widget.line_hide_packets_with_the_following_ids.setText(str_ids)
        self.message_filter_widget.chk_hide_packets_with_the_following_id.setChecked(True)

    def on_clicked_message(self, value):
        index = self.messages_view.filter_proxy.index(value.row(), COLUMN_ID)
        data = self.messages_view.filter_proxy.data(index, Qt.DisplayRole)
        self.message_filter_widget.line_id.setText(str(data))
