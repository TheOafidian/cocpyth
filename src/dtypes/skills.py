import yaml
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, PositiveInt, NonNegativeInt
import stats

skills = yaml.safe_load(Path("data/skills.yaml").read_text())
coc_settings = skills.keys()

class Skill(BaseModel):
    name: str
    max: PositiveInt = 100
    min: NonNegativeInt = 20
    current: NonNegativeInt = 20
    half: NonNegativeInt = 10
    fifth: NonNegativeInt = 4
    description: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.half = stats.cthulhu_round(self.current/2)
        self.fifth = stats.cthulhu_round(self.current/5)

def build_skills(setting:str) -> [Skill]:
    setting_skills = skills[setting]
    setting_skills = [Skill(**s) for s in setting_skills]
    return setting_skills

SETTING_SKILLS = {setting:build_skills(setting) for setting in coc_settings}
SKILLS1920 = SETTING_SKILLS["coc1920"]

if __name__ == "__main__":
    investigation = Skill(**{"name":"investigation", "current": 60})
    print(SKILLS1920)