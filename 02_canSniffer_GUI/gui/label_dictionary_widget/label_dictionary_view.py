from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTableView, QAbstractScrollArea, QSizePolicy, QAbstractItemView, QHeaderView

from core.label_dictionary_model.label_dictionary_model import LabelDictionaryModel
from core.project_data import ProjectData


class LabelDictionaryView(QTableView):
    def __init__(self, project_data: ProjectData, parent=None):
        super().__init__(parent=parent)

        self.label_dictionary_model = LabelDictionaryModel(project_data)
        self.label_dictionary_model.dataChanged.connect(self.resizeColumnsToContents)
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

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
