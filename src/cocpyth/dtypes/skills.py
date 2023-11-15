import yaml
import importlib.resources
from typing import Optional
from pydantic import BaseModel, PositiveInt, NonNegativeInt
from cocpyth.utils.weird_math import cthulhu_round

skills = yaml.safe_load(importlib.resources.open_text("cocpyth.data", "skills.yaml"))
coc_settings = skills.keys()


class Skill(BaseModel):
    name: str
    specialization: bool = False
    uncommon: bool = False
    max: PositiveInt = 100
    min: NonNegativeInt = 20
    current: NonNegativeInt = 20
    half: NonNegativeInt = 10
    fifth: NonNegativeInt = 4
    description: Optional[str] = None

    def _set_half_and_fifth(self):
        self.half = cthulhu_round(self.current / 2)
        self.fifth = cthulhu_round(self.current / 5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_half_and_fifth()

    def set(self, new: PositiveInt):
        self.current = cthulhu_round(new)
        self._set_half_and_fifth()

    def __add__(self, x):
        temp = self.copy()
        temp.current += x
        temp.half = cthulhu_round(temp.current / 2)
        temp.fifth = cthulhu_round(temp.current / 5)
        return temp

    def __iadd__(self, x):
        self.current += x
        self._set_half_and_fifth()
        return self

    def __sub__(self, x):
        temp = self.copy()
        temp.current -= x
        temp.half = cthulhu_round(temp.current / 2)
        temp.fifth = cthulhu_round(temp.current / 5)
        return temp

    def __isub__(self, x):
        self.current -= x
        self._set_half_and_fifth()
        return self
    
    def __truediv__(self, x):
        temp = self.copy()
        temp.current = cthulhu_round(temp.current / x) 
        return temp

    def __idiv__(self, x):
        self.current = cthulhu_round(self.current / x)
        return self

class SkillDict(dict):
    def __init__(self, *args, **kwargs):
        super(SkillDict, self).__init__(*args, **kwargs)
        safe_keys = {k.lower().replace(" ", "_"): v for k, v in self.items()}
        self.__dict__ = safe_keys


def build_skills(setting: str) -> [Skill]:
    setting_skills = skills[setting]
    setting_skills = {s["name"]: Skill(**s) for s in setting_skills}
    return SkillDict(setting_skills)


SETTING_SKILLS = {setting: build_skills(setting) for setting in coc_settings}
SKILLS1920 = SETTING_SKILLS["coc1920"]

if __name__ == "__main__":
    print(SKILLS1920)
