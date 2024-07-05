from typing import Any

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QColor

from gui.components.live_mode_widget.can_message import CanMessage, DataChanged


class MessagesTableModel(QAbstractTableModel):
    def __init__(self, data: list = None, parent=None):
        super().__init__(parent=parent)
        if data is None:
            data = list()
        self.__data = data
        self.__latest_data = {}
        self.__horizontal_headers = [
            "Timestamp (s)",
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
        self.highlight_new_packets = False
        self.highlight_new_values = False

    def rowCount(self, parent=None):
        return len(self.__data)

    def columnCount(self, parent=None):
        return len(self.__horizontal_headers)

    def set_highlight_new_packets(self, value):
        self.highlight_new_packets = value
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), 2),
            [Qt.BackgroundColorRole])
        # self.invalidateFilter()

    def set_highlight_new_values(self, value):
        self.highlight_new_values = value
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()),
            [Qt.BackgroundColorRole])

    def get_data_in_latest_data(self, index) -> bool:
        message = self.__data[index]
        latest_message = self.__latest_data[message.identifier]
        return message is latest_message

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            message: CanMessage = self.__data[index.row()]
            value = message.get_value_from_index(index.column())
            if isinstance(value, DataChanged):
                return value.value
            return value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter | Qt.AlignHCenter

        if role == Qt.BackgroundColorRole:
            message: CanMessage = self.__data[index.row()]
            if self.highlight_new_values:
                value = message.get_value_from_index(index.column())
                if isinstance(value, DataChanged) and value.changed:
                    return QColor(255, 50, 255)

            if self.highlight_new_packets and message.new_identifier and index.column() in [0, 1]:
                return QColor(150, 150, 255)

        if role == Qt.UserRole:
            message: CanMessage = self.__data[index.row()]
            return message

    def headerData(self, section: int, orientation: Any, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and section < len(self.__horizontal_headers):
            if role == Qt.DisplayRole:
                return self.__horizontal_headers[section]

    def add_data(self, data: CanMessage):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.__data.insert(0, data)
        if data.identifier not in self.__latest_data:
            data.new_identifier = True
            data.set_all_data_to_changed()
            self.__latest_data[data.identifier] = data
        else:
            other_message = self.__latest_data[data.identifier]
            data.set_data_changed(other_message)
            self.__latest_data[data.identifier] = data
        self.endInsertRows()
