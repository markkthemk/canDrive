from typing import Dict, Any

from pydantic import BaseModel

from core.can_message.can_message import CanMessage


class CanMessageTimestamp(BaseModel):
    can_message: CanMessage
    timestamp: float  # time the message was received
    new_identifier: bool = False
    indexes_changed: Dict[int, bool] = {}

    def model_post_init(self, __context: Any) -> None:
        for index, _ in enumerate(self.can_message.data):
            self.indexes_changed[index] = False

    def get_value_from_index(self, index):
        if index == 0:
            return self.timestamp
        else:
            return self.can_message.get_value_from_index(index - 1)

    def set_data_changed(self, other):
        for index, d in enumerate(self.can_message.data):
            if index <= len(other.data) and d != other.data[index]:
                self.indexes_changed[index] = True

    def set_all_data_to_changed(self):
        for i in self.indexes_changed:
            self.indexes_changed[i] = True
