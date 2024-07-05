import os
from functools import partial

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QFileDialog

from core.user_preferences import UserPreferences
from core.utils import read_file
from gui.components.can_sniffer_main_widget.can_sniffer_main_widget import (
    CanSnifferMainWidget,
)
from gui.components.status_bar_widget import StatusBarWidget


class CanSnifferMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = None
        # self.__load_styles()

        self.user_prefs = UserPreferences.load()

        self.create_menu_bar()
        self.create_status_bar()

        self.setMinimumSize(600, 400)

        if len(self.user_prefs.recent_projects) >= 1:
            self.open_project(self.user_prefs.recent_projects[0])

    # region menu bar
    # noinspection PyAttributeOutsideInit
    def create_menu_bar(self):
        self.create_menu_bar_actions()
        self.create_tab_actions()
        self.menu_bar = self.menuBar()
        self.create_file_menu()
        self.create_view_menu()

    # noinspection PyAttributeOutsideInit
    def create_file_menu(self):
        self.file_menu = self.menu_bar.addMenu("&File")
        self.file_menu.addAction(self.act_new)

        self.recent_project_menu = self.file_menu.addMenu("&Open recent project...")
        self.recent_project_menu.addActions(self.recent_projects_actions)

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
    def create_menu_bar_actions(self):
        self.act_new = QAction("&New Project", self)
        self.act_new.setShortcut("Ctrl+N")
        self.act_new.setStatusTip("Create new project")
        self.act_new.triggered.connect(self.on_new_project)

        self.recent_projects_actions = []
        for path in self.user_prefs.recent_projects:
            name = str(path.stem)
            action = QAction(name, self)
            action.triggered.connect(partial(self.open_project, path))
            self.recent_projects_actions.append(action)

        self.act_close = QAction("&Close Project", self)
        self.act_close.setShortcut("Ctrl+C")
        self.act_close.setStatusTip("Close project")
        self.act_close.triggered.connect(self.on_project_close)
        self.act_close.setEnabled(False)

    # noinspection PyAttributeOutsideInit
    # noinspection PyUnresolvedReferences
    def create_tab_actions(self):
        self.act_1_live_mode_tab = QAction("&1 Live Mode", self)
        self.act_1_live_mode_tab.setShortcut("Ctrl+1")
        self.act_1_live_mode_tab.setStatusTip("Show Live Mode Tab")
        self.act_1_live_mode_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(0))
        self.act_1_live_mode_tab.setEnabled(True)

        self.act_2_playback_mode_tab = QAction("&2 Playback Mode", self)
        self.act_2_playback_mode_tab.setShortcut("Ctrl+2")
        self.act_2_playback_mode_tab.setStatusTip("Show Playback Mode Tab")
        self.act_2_playback_mode_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(1))
        self.act_2_playback_mode_tab.setEnabled(True)

        self.act_3_decoded_messages_tab = QAction("&3 Decoded Messages", self)
        self.act_3_decoded_messages_tab.setShortcut("Ctrl+3")
        self.act_3_decoded_messages_tab.setStatusTip("Show Decoded Messages Tab")
        self.act_3_decoded_messages_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(2))
        self.act_3_decoded_messages_tab.setEnabled(True)

        self.act_4_label_dictionary_tab = QAction("&4 Label Dictionary", self)
        self.act_4_label_dictionary_tab.setShortcut("Ctrl+4")
        self.act_4_label_dictionary_tab.setStatusTip("Show Label Dictionary Tab")
        self.act_4_label_dictionary_tab.triggered.connect(lambda: self.main_widget.tab_widget.setCurrentIndex(3))
        self.act_4_label_dictionary_tab.setEnabled(True)

    # noinspection PyAttributeOutsideInit
    def on_new_project(self):
        doc = os.path.join(os.environ["USERPROFILE"], "Documents")
        d = QFileDialog.getExistingDirectory(
            self, "New project save location", f"{doc}", QFileDialog.ShowDirsOnly
        )
        self.user_prefs.add_recent_project(d)
        self.open_project(d)

    def open_project(self, project_path):
        self.main_widget = CanSnifferMainWidget(project_path)
        self.setCentralWidget(self.main_widget)

        self.act_new.setEnabled(False)
        self.act_close.setEnabled(True)

    def on_project_close(self):
        self.main_widget = None
        self.setCentralWidget(QWidget())

        self.act_new.setEnabled(True)
        self.act_close.setEnabled(False)

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
