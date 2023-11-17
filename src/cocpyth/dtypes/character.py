from shutil import get_terminal_size
from enum import Enum
from typing import Optional
from pydantic.dataclasses import dataclass
import pandas as pd
from tabulate import tabulate
from cocpyth.dtypes.dice import d4, d6
from cocpyth.dtypes.skill import SKILLS1920
from cocpyth.dtypes.occupation import Occupation
from cocpyth.utils.weird_math import cthulhu_round
import cocpyth.dtypes.stat as stat


@dataclass
class Character:
    first_name: str
    last_name: str
    sanity: stat.Sanity = stat.Sanity()
    strength: stat.Strength = stat.Strength()
    dexterity: stat.Dexterity = stat.Dexterity()
    size: stat.Size = stat.Size()
    constitution: stat.Constitution = stat.Constitution()
    intelligence: stat.Intelligence = stat.Intelligence()
    education: stat.Education = stat.Education()
    power: stat.Power = stat.Power()
    appearance: stat.Appearance = stat.Appearance()
    luck: stat.Luck = stat.Luck()
    hp: stat.Hitpoints = stat.Hitpoints()
    mp: stat.Magicpoints = stat.Magicpoints()
    occupation : Optional[Occupation] = None
    occupational_skill_points: int = 0
    personal_skill_points: int = 0

    def __post_init__(self):
        self.full_name = self.first_name + " " + self.last_name
        self.sanity.current = self.power.current
        self.hp.current = cthulhu_round((self.constitution.current + self.size.current) / 10)
        self.mp.current = self.power.current / 5
        self.skills = SKILLS1920
        self.skills.dodge.set(self.dexterity.current/2)
        self.damage_bonus, self.build = self._determine_build_db()
        self.moverate = self._determine_move_rate()

    def _determine_build_db(self):
        physique = self.strength.current + self.size.current

        if physique < 65:
            return -2, -2
        elif physique < 85:
            return -1, -1
        elif physique < 125:
            return 0, 0
        elif physique < 165:
            return d4, 1
        else: return d6, 2

    def _determine_move_rate(self):

        STR = self.strength.current
        DEX = self.dexterity.current
        SIZ = self.size.current

        if STR < SIZ and DEX < SIZ:
            return 7
        if STR > SIZ and DEX > SIZ:
            return 9
        return 8

    
    def add_occupation(self, occupation: Occupation):
        self.occupation = occupation
        parts= occupation.points_rule.split(",")
        total_skill_points = 0
        for part in parts:
            skill, modifier = part.split("*")
            skill = getattr(self, skill.lower())
            total_skill_points += (skill.current * int(modifier))    
        
        self.occupational_skill_points = total_skill_points


    def stats_to_record(self):
        """Return the current base stats of the character as a single dictionary item"""
        settings = [ k for k in stat.__dict__.keys() if k.endswith("_settings")]
        stats = [setting.split("_")[0] for setting in settings]
        # Abbreviated hp and mp
        stats = list(map(lambda x: x.replace("hitpoints", "hp"), stats))
        stats = list(map(lambda x: x.replace("magicpoints", "mp"), stats))
        return {s:getattr(self, s).current for s in stats}
        

    def format_stats(self):
        
        stats = self.stats_to_record()
        stats_table = pd.DataFrame(stats, index=[0])
        stats_table.columns = [c.capitalize() for c in stats_table.columns]
        
        print(get_terminal_size())
        if get_terminal_size()[0] < 150:
            return tabulate(stats_table.T, headers=["Stat","Value"], tablefmt='psql')
        else: return tabulate(stats_table, headers="keys", showindex=False, tablefmt='psql')



class GenderEnum(str, Enum):
    M = "male"
    F = "female"


if __name__ == "__main__":

    steve = Character("Steve", "Minecraft")
    print(steve.skills.jump)
    print(steve.skills.jump + 10)
    print(steve.skills.jump)
    # for skills with spaces
    print(steve.skills.arts_and_crafts)
