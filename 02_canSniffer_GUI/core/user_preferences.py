import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
from pydantic_core import from_json

SAVE_LOCATION = Path(
    Path(os.getenv("LOCALAPPDATA")) / "can_sniffer" / "user_preferences.json"
)


class UserPreferences(BaseModel):
    default_project_location: Optional[Path] = Path(
        os.path.join(os.environ["USERPROFILE"], "Documents")
    )
    recent_projects: Optional[List[Path]] = []

    def add_recent_project(self, path):
        self.recent_projects.insert(0, path)
        if len(self.recent_projects) > 10:
            self.recent_projects.pop()

    def save(self):
        if not SAVE_LOCATION.parent.exists():
            SAVE_LOCATION.parent.mkdir(parents=True, exist_ok=True)

        with open(SAVE_LOCATION, "w") as f:
            f.write(self.model_dump_json())

    @staticmethod
    def load():
        if not SAVE_LOCATION.exists():
            UserPreferences().save()
        with open(SAVE_LOCATION, "r") as f:
            return UserPreferences.model_validate(from_json(f.read()))

    @staticmethod
    def reset_user_prefs():
        if SAVE_LOCATION.exists():
            SAVE_LOCATION.unlink()
        UserPreferences().save()


if __name__ == "__main__":
    # d = UserPreferences()
    # d.save()
    loaded = UserPreferences.reset_user_prefs()
    print(loaded)
