from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTableView, QAbstractScrollArea, QSizePolicy, QAbstractItemView

from gui.components.message_widget.messages_table_model import DecodedMessagesTableModel


class DecodedMessagesTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.decoded_messages_table_model = DecodedMessagesTableModel()
        self.setModel(self.decoded_messages_table_model)

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
