from PyQt5.QtCore import QAbstractTableModel, Qt

from typing import Any


class BaseMessageTableModel(QAbstractTableModel):
    def __init__(self, data: list = None, headers=None, parent=None):
        super().__init__(parent=parent)
        if headers is None:
            headers = []
        if data is None:
            data = list()
        self._data = data
        self.__horizontal_headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self.__horizontal_headers)

    def headerData(self, section: int, orientation: Any, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and section < len(self.__horizontal_headers):
            if role == Qt.DisplayRole:
                return self.__horizontal_headers[section]
