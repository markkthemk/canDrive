from functools import partial
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QFileDialog, QMessageBox

from core.project_data import load_legacy, save_sniff
from core.user_preferences import UserPreferences
from core.utils import read_file
from gui.main_widget.can_sniffer_main_widget import CanSnifferMainWidget
from gui.components.status_bar_widget.status_bar_widget import StatusBarWidget

CONVERT_STR = "Open and Convert Legacy Project"


class CanSnifferMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = None
        # self.__load_styles()

        self.user_prefs = UserPreferences.load()

        self.create_menu_bar()
        self.create_status_bar()

        self.setMinimumSize(1500, 800)

        self.set_window_title()

        # if len(self.user_prefs.recent_projects) >= 1:
        #     self.open_project(self.user_prefs.recent_projects[0])

    def set_window_title(self, project=None):
        s = "Can Sniffer"
        if project:
            s += " - "
            s += str(project)
        self.setWindowTitle(s)

    # region menu bar
    # noinspection PyAttributeOutsideInit
    def create_menu_bar(self):
        self.create_file_menu_actions()
        self.create_view_menu_actions()
        self.menu_bar = self.menuBar()
        self.create_file_menu()
        self.create_view_menu()

    # noinspection PyAttributeOutsideInit
    def create_file_menu(self):
        self.file_menu = self.menu_bar.addMenu("&File")
        self.file_menu.addAction(self.act_new)

        self.file_menu.addAction(self.act_open)
        self.file_menu.addAction(self.act_open_legacy)

        self.recent_project_menu = self.file_menu.addMenu("&Open recent project...")
        for path in self.user_prefs.recent_projects:
            self.add_recent_project(path, append=True)

        self.file_menu.addAction(self.act_close)

    # noinspection PyAttributeOutsideInit
    def create_view_menu(self):
        self.view_menu = self.menu_bar.addMenu("&View")
        self.view_menu.addAction(self.act_1_live_mode_tab)
        self.view_menu.addAction(self.act_2_playback_mode_tab)
        self.view_menu.addAction(self.act_3_decoded_messages_tab)
        self.view_menu.addAction(self.act_4_label_dictionary_tab)

    # noinspection PyAttributeOutsideInit
    # noinspection PyUnresolvedReferences
    def create_file_menu_actions(self):
        self.act_new = QAction("&New Project", self)
        self.act_new.setShortcut("Ctrl+N")
        self.act_new.setStatusTip("Create new project")
        self.act_new.triggered.connect(self.on_new_project)

        self.act_open = QAction("&Open Project", self)
        self.act_open.setShortcut("Ctrl+O")
        self.act_open.setStatusTip("Open project")
        self.act_open.triggered.connect(self.on_open_project)

        self.act_open_legacy = QAction(f"&{CONVERT_STR}", self)
        self.act_open_legacy.setShortcut("Ctrl+L")
        self.act_open_legacy.setStatusTip(CONVERT_STR)
        self.act_open_legacy.triggered.connect(self.on_open_and_covert_legacy_project)

        self.act_close = QAction("&Close Project", self)
        self.act_close.setShortcut("Ctrl+C")
        self.act_close.setStatusTip("Close project")
        self.act_close.triggered.connect(self.on_project_close)
        self.act_close.setEnabled(False)

    def add_recent_project(self, path, append=False):
        name = str(path.name)
        action = QAction(name, self)
        action.triggered.connect(partial(self.open_project, path))
        if append:
            self.recent_project_menu.addAction(action)
        else:
            before_action = self.recent_project_menu.actions()[0] if self.recent_project_menu.actions() else None
            self.recent_project_menu.insertAction(before_action, action)

    # noinspection PyAttributeOutsideInit
    # noinspection PyUnresolvedReferences
    def create_view_menu_actions(self):
        self.act_1_live_mode_tab = QAction("&1 Live Mode", self)
        self.act_1_live_mode_tab.setShortcut("Ctrl+1")
        self.act_1_live_mode_tab.setStatusTip("Show Live Mode Tab")
        self.act_1_live_mode_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(0))

        self.act_2_playback_mode_tab = QAction("&2 Playback Mode", self)
        self.act_2_playback_mode_tab.setShortcut("Ctrl+2")
        self.act_2_playback_mode_tab.setStatusTip("Show Playback Mode Tab")
        self.act_2_playback_mode_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(1))

        self.act_3_decoded_messages_tab = QAction("&3 Decoded Messages", self)
        self.act_3_decoded_messages_tab.setShortcut("Ctrl+3")
        self.act_3_decoded_messages_tab.setStatusTip("Show Decoded Messages Tab")
        self.act_3_decoded_messages_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(2))

        self.act_4_label_dictionary_tab = QAction("&4 Label Dictionary", self)
        self.act_4_label_dictionary_tab.setShortcut("Ctrl+4")
        self.act_4_label_dictionary_tab.setStatusTip("Show Label Dictionary Tab")
        self.act_4_label_dictionary_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(3))

    def new_project_dialog(self) -> Path:
        path, _ = QFileDialog.getSaveFileName(
            self, "New project", f"{self.user_prefs.default_project_location}", "*.sniff")

        if not path:
            return

        project_path = Path(path)
        project_path.unlink(missing_ok=True)

        if project_path not in self.user_prefs.recent_projects:
            self.user_prefs.add_recent_project(project_path)
            self.add_recent_project(project_path)
        return project_path

    # noinspection PyAttributeOutsideInit
    def on_new_project(self):
        project_path = self.new_project_dialog()
        if not project_path:
            return
        self.open_project(project_path)

    def on_open_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open project", f"{self.user_prefs.default_project_location}", "*.sniff")
        if not path:
            return

        project_path = Path(path)
        self.open_project(project_path)

    def on_open_and_covert_legacy_project(self):
        d = QFileDialog.getExistingDirectory(
            self, CONVERT_STR, f"{self.user_prefs.default_project_location}", QFileDialog.ShowDirsOnly
        )

        try:
            project_data = load_legacy(Path(d))
            project_path = self.new_project_dialog()
            if not project_path:
                return

            save_sniff(project_path, project_data)

        except FileNotFoundError as e:
            QMessageBox.warning(self, "Warning", str(e))
            return

        self.open_project(project_path)

    def open_project(self, project_path: Path):
        self.main_widget = CanSnifferMainWidget(project_path)
        self.setCentralWidget(self.main_widget)

        self.act_new.setEnabled(False)
        self.act_open.setEnabled(False)
        self.act_open_legacy.setEnabled(False)
        self.recent_project_menu.setEnabled(False)
        self.act_close.setEnabled(True)

        self.act_1_live_mode_tab.setEnabled(True)
        self.act_2_playback_mode_tab.setEnabled(True)
        self.act_3_decoded_messages_tab.setEnabled(True)
        self.act_4_label_dictionary_tab.setEnabled(True)

        self.set_window_title(project_path)

    def on_project_close(self):
        self.main_widget = None
        self.setCentralWidget(QWidget())

        self.act_new.setEnabled(True)
        self.act_open.setEnabled(True)
        self.act_open_legacy.setEnabled(True)
        self.recent_project_menu.setEnabled(True)
        self.act_close.setEnabled(False)

        self.act_1_live_mode_tab.setEnabled(False)
        self.act_2_playback_mode_tab.setEnabled(False)
        self.act_3_decoded_messages_tab.setEnabled(False)
        self.act_4_label_dictionary_tab.setEnabled(False)

        self.set_window_title()

    # endregion
    # noinspection PyAttributeOutsideInit
    def create_status_bar(self):
        self.status_bar_widget = StatusBarWidget()
        self.statusBar().addPermanentWidget(self.status_bar_widget)

    def closeEvent(self, event):
        self.user_prefs.save()
        event.accept()

    def __load_styles(self):
        self.setStyleSheet(
            read_file(
                "styles/dark.css"
            )
        )
