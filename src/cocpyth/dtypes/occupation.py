import yaml
import importlib.resources
from typing import Optional, List
from pydantic import BaseModel
from cocpyth.utils.weird_math import cthulhu_round


occupations = yaml.safe_load(importlib.resources.open_text("cocpyth.data", "occupations.yaml"))
coc_settings = occupations.keys()

class OccupationConstructor(BaseModel):
    name: str
    points: str
    skills: List[str]
    description: Optional[str] = None

class Occupation(BaseModel):
    name: str
    points_rule: str
    skill_choices: int
    social_choices: int
    skills: List[str]
    description: Optional[str] = None


    def __init__(self, constructor: OccupationConstructor):
        
        skills = [sk.strip().capitalize() for sk in constructor.skills if sk.strip().capitalize() not in ["Any", "Interpersonal"]]
        super().__init__(
            name=constructor.name.strip().capitalize(),
            points_rule=constructor.points.strip(),
            skills=skills,
            skill_choices=constructor.skills.count("Any"),
            social_choices=constructor.skills.count("Interpersonal"),
            description=constructor.description,
        )           
        

class OccupationDict(dict):
    def __init__(self, *args, **kwargs):
        super(OccupationDict, self).__init__(*args, **kwargs)
        safe_keys = {k.lower().replace(" ", "_"): v for k, v in self.items()}
        self.__dict__ = safe_keys


def build_occupations(setting: str) -> [Occupation]:
    setting_occupations = occupations[setting]
    setting_occupations = {o["name"]: OccupationConstructor(**o) for o in setting_occupations}
    for k, constructor in setting_occupations.items():
        setting_occupations[k] = Occupation(constructor)
    return OccupationDict(setting_occupations)


SETTING_OCCUPATIONS = {setting: build_occupations(setting) for setting in coc_settings}
OCCUPATIONS1920 = SETTING_OCCUPATIONS["coc1920"]

if __name__ == "__main__":
    skills = OCCUPATIONS1920.antiquarian.skills
    print(skills)