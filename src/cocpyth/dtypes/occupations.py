import yaml
import importlib.resources
from typing import Optional, List
from pydantic import BaseModel, computed_field, TypeAdapter
from cocpyth.dtypes.skills import Skill, SkillDict, SETTING_SKILLS
from cocpyth.utils.weird_math import cthulhu_round


occupations = yaml.safe_load(importlib.resources.open_text("cocpyth.data", "occupations.yaml"))
coc_settings = occupations.keys()

class Occupation(BaseModel):
    name: str
    skill_choices: List[str]
    points: str
    description: Optional[str] = None

    @computed_field
    @property
    def skill_choices(self) -> int:
        return self.skills.count("Any")
    
    
    @computed_field
    @property
    def social_choices(self) -> int:
        return self.skills.count("Interpersonal")
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skills = [sk for sk in self.skills if sk not in ["Any","Interpersonal"]]
        
        
class OccupationDict(dict):
    def __init__(self, *args, **kwargs):
        super(OccupationDict, self).__init__(*args, **kwargs)
        safe_keys = {k.lower().replace(" ", "_"): v for k, v in self.items()}
        self.__dict__ = safe_keys


def build_occupations(setting: str) -> [Occupation]:
    setting_occupations = occupations[setting]
    setting_occupations = {o["name"]: Occupation(**o) for o in setting_occupations}
    return OccupationDict(setting_occupations)


SETTING_OCCUPATIONS = {setting: build_occupations(setting) for setting in coc_settings}
OCCUPATIONS1920 = SETTING_OCCUPATIONS["coc1920"]

if __name__ == "__main__":
    skills = OCCUPATIONS1920.antiquarian.skills
    print(skills)