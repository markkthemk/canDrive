from pydantic import BaseModel

from core.can_message.can_message import CanMessage


class DecodedCanMessage(BaseModel):
    can_message: CanMessage
    name: str

    def get_value_from_index(self, index):
        if index == 0:
            return self.name
        else:
            return self.can_message.get_value_from_index(index - 1)
