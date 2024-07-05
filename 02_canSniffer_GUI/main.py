# canDrive @ 2020
# To create a one-file executable, call: pyinstaller -F main.spec
# ----------------------------------------------------------------
import sys
import qtmodern
from qtmodern import styles
from qtmodern import windows

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout, QSizeGrip
from PyQt5.QtCore import Qt

from gui.can_sniffer_gui import CanSnifferGUI

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


def main():
    # excepthook redirect
    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    # creating app
    app = QApplication(sys.argv)
    gui = CanSnifferGUI()

    # applying dark theme
    qtmodern.styles.dark(app)
    darked_gui = qtmodern.windows.ModernWindow(gui)

    # adding a grip to the top left corner to make the frameless window resizable
    layout = QVBoxLayout()
    sizegrip = QSizeGrip(darked_gui)
    sizegrip.setMaximumSize(30, 30)
    layout.addWidget(sizegrip, 50, Qt.AlignBottom | Qt.AlignRight)
    darked_gui.setLayout(layout)

    # starting the app
    darked_gui.show()
    app.exec_()


if __name__ == "__main__":
    main()
