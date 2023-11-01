import yaml
import re
from yaml import Loader
from cocpyth.dtypes.character import Character
from cocpyth.dtypes.skills import Skill, SkillDict
from cocpyth.dtypes.stats import Strength, Sanity, Dexterity, Constitution, HitPoints, Appearance, Intelligence, Education, Size, Luck, Power

def skill_representer(dumper, data):
    return dumper.represent_scalar(u'!Skill', f'({data.current}|{data.half}|{data.fifth})')

yaml.add_implicit_resolver(u'!Skill', re.compile(r"^(\d+|\d+|\d+)$"))

def skill_constructor(loader, node):
    value = loader.construct_scalar(node)
    current = value.strip("()").split("|")[0]
    return Skill(name="testing", current=current)

def stat_representer(dumper, data):
    return dumper.represent_scalar(f'!{data.name}', f'({data.current})')

#yaml.add_representer(SkillDict, skillset_representer)
yaml.add_representer(Skill, skill_representer)
yaml.add_constructor(u'!Skill', skill_constructor)
#for stat in [Strength, Sanity, Dexterity, Constitution, HitPoints, Appearance, Intelligence, Education, Size, Luck, Power]:
#    yaml.add_representer(stat, stat_representer)

def save_character(char: Character, file):
    with open(file, "w") as f:
        yaml.dump(char, f)
    return file

def load_character(file):
    with open(file, "r") as f:
        return yaml.load(f, Loader)
    
if __name__ == "__main__":
    strength = Strength()
    print(yaml.dump(strength))