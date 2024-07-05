from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QTableView, QSizePolicy, QAbstractScrollArea, QAbstractItemView, QMenu

from gui.components.live_mode_widget.can_message import CanMessage, DataChanged
from gui.components.message_widget.message_table_filter import (
    MessageTableFilterProxyModel,
)
from gui.components.message_widget.messages_table_model import MessagesTableModel


class MessageTableView(QTableView):
    set_show_ids = pyqtSignal(list)
    set_hide_ids = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.messages_model = MessagesTableModel()

        messages = [
            CanMessage(
                timestamp=4,
                identifier=13,
                rtr=0,
                ide=0,
                dlc=8,
                data=[
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0x11),
                ],
            ),
            CanMessage(
                timestamp=5,
                identifier=11,
                rtr=0,
                ide=0,
                dlc=5,
                data=[
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                ],
            ),
            CanMessage(
                timestamp=6,
                identifier=12,
                rtr=0,
                ide=0,
                dlc=8,
                data=[
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                ],
            ),
            CanMessage(
                timestamp=7,
                identifier=13,
                rtr=0,
                ide=0,
                dlc=8,
                data=[
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0x00),
                    DataChanged(value=0xFF),
                    DataChanged(value=0xFF),
                    DataChanged(value=0x11),
                ],
            ),
        ]

        for message in messages:
            self.messages_model.add_data(message)

        self.filter_proxy = MessageTableFilterProxyModel(self)
        self.filter_proxy.setSourceModel(self.messages_model)
        self.setModel(self.filter_proxy)

        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QSize(0, 0))
        self.setAlternatingRowColors(True)
        self.setShowGrid(True)
        self.verticalHeader().setStretchLastSection(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        for i in range(5, self.model().columnCount()):
            self.setColumnWidth(i, 32)

    def contextMenuEvent(self, event):
        menu = QMenu()

        selected_ids = []
        selection = self.selectionModel()
        for item in selection.selectedRows(1):
            selected_id = self.model().data(item, Qt.DisplayRole)
            if selected_id not in selected_ids:
                selected_ids.append(selected_id)

        selected_ids = sorted(selected_ids)

        if selected_ids:
            set_selection_to_show_action = menu.addAction(f'Set {selected_ids} as show ids')
            set_selection_to_hide_action = menu.addAction(f'Set {selected_ids} as hide ids')

            res = menu.exec_(event.globalPos())

            if res == set_selection_to_show_action:
                self.set_show_ids.emit(selected_ids)
            if res == set_selection_to_hide_action:
                self.set_hide_ids.emit(selected_ids)

            selection.clearSelection()
