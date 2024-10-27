import os
from pathlib import Path
from typing import List, Optional, Any
from pydantic import BaseModel
from pydantic_yaml import to_yaml_file, parse_yaml_raw_as

SAVE_LOCATION = Path(
    Path(os.getenv("LOCALAPPDATA")) / "can_sniffer" / "user_preferences.yaml"
)


class UserPreferences(BaseModel):
    default_project_location: Optional[Path] = Path(
        Path(os.path.join(os.environ["USERPROFILE"], "Documents")) / "can_sniffer")
    recent_projects: Optional[List[Path]] = []

    def model_post_init(self, __context: Any) -> None:
        self.default_project_location.mkdir(parents=True, exist_ok=True)

    def add_recent_project(self, path):
        self.recent_projects.insert(0, path)
        if len(self.recent_projects) > 10:
            self.recent_projects.pop()

    def save(self):
        if not SAVE_LOCATION.parent.exists():
            SAVE_LOCATION.parent.mkdir(parents=True, exist_ok=True)
        to_yaml_file(SAVE_LOCATION, self)

    @staticmethod
    def load():
        if not SAVE_LOCATION.exists():
            UserPreferences().save()
        with open(SAVE_LOCATION, "r") as f:
            prefs = UserPreferences.model_validate(parse_yaml_raw_as(UserPreferences, f.read()))
            prefs.recent_projects[:] = [p for p in prefs.recent_projects if p.exists()]
            return prefs

    @staticmethod
    def reset_user_prefs():
        if SAVE_LOCATION.exists():
            SAVE_LOCATION.unlink()
        UserPreferences().save()


if __name__ == '__main__':
    u = UserPreferences()
    u.reset_user_prefs()
