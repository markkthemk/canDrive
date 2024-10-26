from typing import Any

from PyQt5.QtCore import QModelIndex, QAbstractTableModel, Qt


class LabelDictionaryModel(QAbstractTableModel):

    def __init__(self, data: dict = None, parent=None):
        super().__init__(parent=parent)
        if data is None:
            data = {}
        self.__data = data
        self.__horizontal_headers = [
            "ID (hex)",
            "Label"
        ]

    def rowCount(self, parent=None):
        return len(self.__data)

    def columnCount(self, parent=None):
        return len(self.__horizontal_headers)

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            key = [d for d in self.__data.keys()][index.row()]
            if index.column() == 0:
                return key
            elif index.column() == 1:
                return self.__data[key]
            else:
                print("index is not 0 or 1")

        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter | Qt.AlignHCenter

    def headerData(self, section: int, orientation: Any, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and section < len(self.__horizontal_headers):
            if role == Qt.DisplayRole:
                return self.__horizontal_headers[section]

    def add_data(self, key, value):
        self.beginInsertRows(QModelIndex(), 0, 0)
        if key not in self.__data:
            self.__data[key] = value

        sorted_dict = dict(sorted(self.__data.items()))
        self.__data = sorted_dict

        self.endInsertRows()

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            key = [d for d in self.__data.keys()][index.row()]
            self.__data[key] = value
            return True
