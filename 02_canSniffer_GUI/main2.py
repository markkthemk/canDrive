import sys

from PyQt5.QtWidgets import QApplication

from gui.can_sniffer_main_window import CanSnifferMainWindow


def main2():
    app = QApplication(sys.argv)
    gui = CanSnifferMainWindow()
    gui.show()
    app.exec_()


if __name__ == "__main__":
    main2()
