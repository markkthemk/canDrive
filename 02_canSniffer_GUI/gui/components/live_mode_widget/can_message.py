import time
from typing import List

from pydantic import BaseModel


class DataChanged(BaseModel):
    value: int
    changed: bool = False


class CanMessage(BaseModel):
    timestamp: float  # time the message was received
    identifier: int  # message identifier
    rtr: int  # remote transmission request
    ide: int  # identifier extension bit
    dlc: int  # data length code
    data: List[DataChanged] = []  # max 8 bytes of value
    new_identifier: bool = False

    def get_value_from_index(self, index):
        match index:
            case 0:
                return self.timestamp
            case 1:
                return self.identifier
            case 2:
                return self.rtr
            case 3:
                return self.ide
            case 4:
                return self.dlc
            case 5:
                return self.data[0]
            case 6:
                if len(self.data) >= 2:
                    return self.data[1]
            case 7:
                if len(self.data) >= 3:
                    return self.data[2]
            case 8:
                if len(self.data) >= 4:
                    return self.data[3]
            case 9:
                if len(self.data) >= 5:
                    return self.data[4]
            case 10:
                if len(self.data) >= 6:
                    return self.data[5]
            case 11:
                if len(self.data) >= 7:
                    return self.data[6]
            case 12:
                if len(self.data) >= 8:
                    return self.data[7]
            case _:
                return None

    def set_data_changed(self, other):
        for index, d in enumerate(self.data):
            if index <= len(other.data) and d.value != other.data[index].value:
                d.changed = True

    def set_all_data_to_changed(self):
        for d in self.data:
            d.changed = True

    @staticmethod
    def message_from_csv(csv_message):
        split = csv_message.split(",")

        message = CanMessage(
            timestamp=time.time(),
            identifier=split[0],
            rtr=split[1],
            ide=split[2],
            dlc=split[3],
            data=[DataChanged(value=int(item))for item in split[4:]],
        )
        return message

    def message_to_csv(self, with_terminator=False):
        csv_msg = f"{self.identifier},{self.rtr},{self.ide},{self.dlc}"
        for data in self.data:
            csv_msg += f",{data}"
        if with_terminator:
            csv_msg += ";"
        return csv_msg


if __name__ == "__main__":
    m = CanMessage(timestamp=1.01, identifier=1, rtr=2, ide=3, dlc=4)
    print(m)

    m2 = CanMessage.message_from_csv("1,2,3,4,5,6,7,8")
    print(m2)

    csv = m2.message_to_csv(with_terminator=True)
    print(csv)
