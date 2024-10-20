from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGroupBox, QCheckBox, QHBoxLayout, QSpinBox, QLineEdit, \
    QSpacerItem, QSizePolicy, QGridLayout


class MessageFilterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        # size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        self.setSizePolicy(size_policy)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.btn_clear_table = QPushButton("Clear table")
        self.main_layout.addWidget(self.btn_clear_table)

        self.__create_filter_groupbox()
        self.__create_decoder_groupbox()

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)

    def __create_filter_groupbox(self):
        self.hex_validator = QRegExpValidator(QRegExp(
            r'\b[1-9A-Fa-f][A-Fa-f0-9]*\b(?: \b[1-9A-Fa-f][A-Fa-f0-9]*\b)*( )?'
        ))

        filters_groupbox = QGroupBox("Filters")
        filters_groupbox_layout = QVBoxLayout()
        filters_groupbox.setLayout(filters_groupbox_layout)
        self.main_layout.addWidget(filters_groupbox)

        self.chk_group_packets = QCheckBox("Group packets")
        filters_groupbox_layout.addWidget(self.chk_group_packets)
        self.chk_highlight_new_packets = QCheckBox("Highlight new packets")
        filters_groupbox_layout.addWidget(self.chk_highlight_new_packets)
        self.chk_highlight_new_values = QCheckBox("Highlight new values")
        filters_groupbox_layout.addWidget(self.chk_highlight_new_values)
        package_age_layout = QHBoxLayout()
        self.chk_hide_packets_older_than = QCheckBox("Hide packets older than (s):")
        package_age_layout.addWidget(self.chk_hide_packets_older_than)
        self.spin_hide_packets_older_than = QSpinBox()
        package_age_layout.addWidget(self.spin_hide_packets_older_than)
        filters_groupbox_layout.addLayout(package_age_layout)
        self.chk_show_packets_with_the_following_id = QCheckBox("Show packets with the following IDS:")
        filters_groupbox_layout.addWidget(self.chk_show_packets_with_the_following_id)
        self.line_show_packets_with_the_following_ids = QLineEdit()
        self.line_show_packets_with_the_following_ids.setPlaceholderText("ID1 ID2 ...")
        self.line_show_packets_with_the_following_ids.setValidator(self.hex_validator)
        filters_groupbox_layout.addWidget(self.line_show_packets_with_the_following_ids)
        self.chk_hide_packets_with_the_following_id = QCheckBox("Hide packets with the following IDS:")
        filters_groupbox_layout.addWidget(self.chk_hide_packets_with_the_following_id)
        self.line_hide_packets_with_the_following_ids = QLineEdit()
        self.line_hide_packets_with_the_following_ids.setPlaceholderText("ID1 ID2 ...")
        self.line_hide_packets_with_the_following_ids.setValidator(self.hex_validator)
        filters_groupbox_layout.addWidget(self.line_hide_packets_with_the_following_ids)

    def __create_decoder_groupbox(self):
        decoding_groupbox = QGroupBox("Decoding")
        decoding_layout = QGridLayout()
        decoding_groupbox.setLayout(decoding_layout)
        self.main_layout.addWidget(decoding_groupbox)

        self.line_id = QLineEdit()
        self.line_id.setPlaceholderText("ID")
        self.line_label = QLineEdit()
        self.line_label.setPlaceholderText("LABEL")
        self.btn_add_id_label = QPushButton("Add ID to label dictionary")
        self.btn_add_message = QPushButton("Add Message to decoded messages")

        decoding_layout.addWidget(self.line_id, 0, 0, 1, 1)
        decoding_layout.addWidget(self.line_label, 0, 1, 1, 1)
        decoding_layout.addWidget(self.btn_add_id_label, 1, 0, 1, 2)
        decoding_layout.addWidget(self.btn_add_message, 2, 0, 1, 2)

