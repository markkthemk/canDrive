from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QColor

from core.can_message.can_message import CanMessage
from core.can_message.can_message_timestamp import CanMessageTimestamp
from core.message_table_model.base_message_table_model import BaseMessageTableModel
from core.project_data import ProjectData


class MessagesTableModel(BaseMessageTableModel):
    def __init__(self, data: list = None, project_data: ProjectData = ProjectData(), parent=None):
        headers = [
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

        super().__init__(data=data, headers=headers, parent=parent)
        self.__latest_data = {}
        self.highlight_new_packets = False
        self.highlight_new_values = False
        self.project_data = project_data

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

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            message: CanMessageTimestamp = self._data[index.row()]
            value = message.get_value_from_index(index.column())
            if index.column() == 1:
                if value in self.project_data.label_dict:
                    return f"{value} ({self.project_data.label_dict[value]})"
            return value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter | Qt.AlignHCenter

        if role == Qt.BackgroundColorRole:
            message: CanMessageTimestamp = self._data[index.row()]
            if self.highlight_new_values:
                changed_col = index.column() - 5
                if changed_col in message.indexes_changed and message.indexes_changed[changed_col]:
                    return QColor(255, 50, 255)

            if self.highlight_new_packets and message.new_identifier and index.column() in [0, 1]:
                return QColor(150, 150, 255)

        if role == Qt.UserRole:
            message: CanMessage = self._data[index.row()]
            return message

    def get_data_in_latest_data(self, index) -> bool:
        message = self._data[index]
        latest_message = self.__latest_data[message.can_message.identifier]
        return message is latest_message

    def add_data(self, data: CanMessageTimestamp):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._data.insert(0, data)
        if data.can_message.identifier not in self.__latest_data:
            data.new_identifier = True
            data.set_all_data_to_changed()
            self.__latest_data[data.can_message.identifier] = data
        else:
            other_message = self.__latest_data[data.can_message.identifier]
            data.set_data_changed(other_message.can_message)
            self.__latest_data[data.can_message.identifier] = data
        self.endInsertRows()
