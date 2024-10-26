from typing import Any

from PyQt5.QtCore import Qt, QModelIndex

from core.can_message.decoded_can_message import DecodedCanMessage
from core.message_table_model.base_message_table_model import BaseMessageTableModel


class DecodedMessagesTableModel(BaseMessageTableModel):
    def __init__(self, data: list = None, parent=None):
        headers = [
            "Name",
            "ID (hex)",
            "RTR (hex)",
            "IDE (hex)",
            "DLC (hex)",
            "D0",
            "D1",
            "D2",
            "D3",
            "D4",
            "D5",
            "D6",
            "D7",
        ]

        super().__init__(data=data, headers=headers, parent=parent)

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            message: DecodedCanMessage = self._data[index.row()]
            value = message.get_value_from_index(index.column())
            return value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter | Qt.AlignHCenter

        if role == Qt.UserRole:
            message: DecodedCanMessage = self._data[index.row()]
            return message

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()].name = value
            return True

    def add_data(self, data: DecodedCanMessage):
        for message in self._data:
            if message.can_message == data.can_message:
                return

        self.beginInsertRows(QModelIndex(), 0, 0)
        self._data.insert(0, data)
        self.endInsertRows()
