from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class StatusBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.__package_count = 0

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Package count:"))
        self.lbl_package_count = QLabel()
        layout.addWidget(self.lbl_package_count)

        self.reset_package_count()

    def reset_package_count(self):
        self.__package_count = 0
        self.__update_package_count_label()

    def package_count_inc(self):
        self.__package_count += 1
        self.__update_package_count_label()

    def __update_package_count_label(self):
        self.lbl_package_count.setText(str(self.__package_count))
