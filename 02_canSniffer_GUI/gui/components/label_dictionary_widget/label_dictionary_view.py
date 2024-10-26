from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTableView, QAbstractScrollArea, QSizePolicy, QAbstractItemView

from gui.components.label_dictionary_widget.label_dictionary_model import LabelDictionaryModel


class LabelDictionaryView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.label_dictionary_model = LabelDictionaryModel()

        labels = [
            [3, "hoi_3"],
            [2, "hoi_2"],
            [0, "hoi"],
            [1, "hoi_1"],
            [2, "hoi_22rwefsdf"],
        ]

        for label in labels:
            self.label_dictionary_model.add_data(label[0], label[1])

        self.setModel(self.label_dictionary_model)

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
