from typing import List, Any, Dict

from pydantic import BaseModel


class CanMessage(BaseModel):
    identifier: int  # message identifier
    rtr: int  # remote transmission request
    ide: int  # identifier extension bit
    dlc: int  # data length code
    data: List[int] = []  # max 8 bytes of value

    def get_value_from_index(self, index):
        match index:
            case 0:
                return self.identifier
            case 1:
                return self.rtr
            case 2:
                return self.ide
            case 3:
                return self.dlc
            case 4:
                return self.data[0]
            case 5:
                if len(self.data) >= 2:
                    return self.data[1]
            case 6:
                if len(self.data) >= 3:
                    return self.data[2]
            case 7:
                if len(self.data) >= 4:
                    return self.data[3]
            case 8:
                if len(self.data) >= 5:
                    return self.data[4]
            case 9:
                if len(self.data) >= 6:
                    return self.data[5]
            case 10:
                if len(self.data) >= 7:
                    return self.data[6]
            case 11:
                if len(self.data) >= 8:
                    return self.data[7]
            case _:
                return None

    @staticmethod
    def message_from_csv(csv_message):
        split = csv_message.split(",")

        message = CanMessage(
            identifier=split[0],
            rtr=split[1],
            ide=split[2],
            dlc=split[3],
            data=[int(item) for item in split[4:]]
        )
        return message

    def message_to_csv(self, with_terminator=False):
        csv_msg = f"{self.identifier},{self.rtr},{self.ide},{self.dlc}"
        for data in self.data:
            csv_msg += f",{data}"
        if with_terminator:
            csv_msg += ";"
        return csv_msg





def main():
    c1 = CanMessage(identifier=1, rtr=2, ide=3, dlc=4, data=[5, 6, 7, 8, 9, 10, 11, 12])
    c2 = CanMessage(identifier=1, rtr=2, ide=3, dlc=4, data=[5, 6, 7, 8, 9, 10, 11, 12])

    print(c1 == c2)
    print(c1 is c2)
    lst = [c2]

    print(c1 in lst)
    print(c2 in lst)


if __name__ == '__main__':
    main()
