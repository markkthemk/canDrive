from PyQt5.QtCore import QSortFilterProxyModel, Qt, QModelIndex


COLUMN_TIME = 0
COLUMN_ID = 1


class MessageTableFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_packets = False

        self.hide_packets_older_than = False
        self.hide_packets_older_than_value = 0.0
        self.show_packets_with_id = False
        self.show_packets_with_id_list = []
        self.hide_packets_with_id = False
        self.hide_packets_with_id_list = []

    def set_group_packets(self, value):
        self.group_packets = value
        self.invalidateFilter()

    def set_hide_packets_older_than(self, value):
        self.hide_packets_older_than = value
        self.invalidateFilter()

    def set_hide_packets_older_than_value(self, value: float):
        self.hide_packets_older_than_value = value
        self.invalidateFilter()

    def set_show_packets_with_id(self, value):
        self.show_packets_with_id = value
        self.invalidateFilter()

    @staticmethod
    def __list_with_ints_from_string(values) -> list:
        split_ids_strs = values.split(" ")
        split_ids_strs = [s.strip() for s in split_ids_strs]
        split_ids = []
        for s in split_ids_strs:
            try:
                split_ids.append(int(s))
            except ValueError:
                pass
        return split_ids

    def set_show_packets_with_id_vales(self, values):
        self.show_packets_with_id_list = self.__list_with_ints_from_string(values)
        self.invalidateFilter()

    def set_hide_packets_with_id(self, value):
        self.hide_packets_with_id = value
        self.invalidateFilter()

    def set_hide_packets_with_id_vales(self, values):
        self.hide_packets_with_id_list = self.__list_with_ints_from_string(values)
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex):
        if self.hide_packets_older_than and not self.hide_packets_older_than_filter(source_row, source_parent):
            return False
        if self.group_packets and not self.group_messages_filter(source_row):
            return False
        if self.show_packets_with_id and not self.show_packets_with_id_filter(source_row, source_parent):
            return False
        if self.hide_packets_with_id and not self.hide_packets_with_id_filter(source_row, source_parent):
            return False
        return True

    def group_messages_filter(self, source_row: int):
        return self.sourceModel().get_data_in_latest_data(source_row)

    def hide_packets_older_than_filter(self, source_row: int, source_parent: QModelIndex):
        index = self.sourceModel().index(source_row, COLUMN_TIME, source_parent)
        value = self.sourceModel().data(index, Qt.DisplayRole)
        if value >= self.hide_packets_older_than_value:
            return True
        return False

    def show_packets_with_id_filter(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, COLUMN_ID, source_parent)
        value = self.sourceModel().data(index, Qt.DisplayRole)
        if value in self.show_packets_with_id_list:
            return True
        return False

    def hide_packets_with_id_filter(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, COLUMN_ID, source_parent)
        value = self.sourceModel().data(index, Qt.DisplayRole)
        if value not in self.hide_packets_with_id_list:
            return True
        return False
