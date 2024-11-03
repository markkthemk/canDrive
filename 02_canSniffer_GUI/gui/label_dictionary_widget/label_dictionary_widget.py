from PyQt5.QtWidgets import QWidget, QVBoxLayout

from core.project_data import ProjectData
from gui.label_dictionary_widget.label_dictionary_view import LabelDictionaryView


class LabelDictionaryWidget(QWidget):
    def __init__(self, project_data: ProjectData, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.label_dictionary_view = LabelDictionaryView(project_data)
        self.main_layout.addWidget(self.label_dictionary_view)

    def add_id_label(self, key, value):
        self.label_dictionary_view.label_dictionary_model.add_data(key, value)