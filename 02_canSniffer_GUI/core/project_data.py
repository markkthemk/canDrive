import csv
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, ValidationError

from core.can_message.can_message import CanMessage
from core.can_message.decoded_can_message import DecodedCanMessage


class ProjectData(BaseModel):
    label_dict: Dict[int, str] = {}
    decoded_messages: List[DecodedCanMessage] = []


def load_sniff(path: Path):
    try:
        with open(path, "r") as f:
            project_data = ProjectData.model_validate_json(f.read())
    except ValidationError:
        return ProjectData()
    return project_data


def save_sniff(path: Path, data: ProjectData):
    with open(path, "w") as f:
        f.write(data.model_dump_json(indent=2))


def load_csv(path: Path):
    container = []
    with open(str(path), "r") as stream:
        for row_data in csv.reader(stream):
            container.append(row_data)
    return container


def load_legacy(path: Path) -> ProjectData:
    label_dict_csv_path = Path(path / "labelDict.csv")
    decoded_packets_csv_path = Path(path / "decodedPackets.csv")

    if not label_dict_csv_path.exists():
        raise FileNotFoundError("no labelDict.csv")

    if not decoded_packets_csv_path.exists():
        raise FileNotFoundError("no decodedPackets.csv")

    label_dict_list = load_csv(label_dict_csv_path)
    decoded_messages = load_csv(decoded_packets_csv_path)

    project_data = ProjectData()

    for item in label_dict_list:
        key = int(item[0], 16)
        project_data.label_dict[key] = item[1]

    for item in decoded_messages:
        name = item[0]
        identifier = int(item[1].split(" ")[0], 16)
        rtr = int(item[2], 16)
        ide = int(item[3], 16)
        dlc = int(item[4])
        data = [int(d, 16) for d in item[5:] if d]
        project_data.decoded_messages.append(DecodedCanMessage(
            name=name, can_message=CanMessage(
                identifier=identifier, rtr=rtr, ide=ide, dlc=dlc, data=data
            )
        ))

    return project_data


def main():
    path = Path(r"C:\Users\mark.klarenbeek\documents\can_sniffer\hoi1.sniff")
    project_data = ProjectData()
    for i in range(5):
        project_data.label_dict[i] = str(i)
        project_data.decoded_messages.append(
            DecodedCanMessage(name=str(i), can_message=CanMessage(
                identifier=10 * i, rtr=11 * i, ide=12 * i, dlc=13 * i,
                data=[14 * i, 15 * i, 16 * i, 17 * i, 18 * i, 19 * i]))
        )

    save_sniff(path, project_data)
    data = load_sniff(path)
    print(data)


def legacy():
    path = Path(r"D:\programming\canDrive\02_canSniffer_GUI\save")
    save_path = Path(r"C:\Users\mark.klarenbeek\documents\can_sniffer\hoi1.sniff")

    project_data = load_legacy(path)
    save_sniff(save_path, project_data)


if __name__ == '__main__':
    # main()
    legacy()
