from pydantic.dataclasses import dataclass
from cocpyth.dtypes.skills import SKILLS1920
from cocpyth.utils.weird_math import cthulhu_round
import cocpyth.dtypes.stats as stats

@dataclass
class Character():
    first_name: str
    last_name: str
    sanity: stats.Sanity = stats.Sanity()
    strength: stats.Strength = stats.Strength()
    dexterity: stats.Dexterity = stats.Dexterity()
    size: stats.Size = stats.Size()
    constitution: stats.Constitution = stats.Constitution()
    intelligence: stats.Intelligence = stats.Intelligence()
    education: stats.Education = stats.Education()
    power: stats.Power = stats.Power()
    appearance: stats.Appearance = stats.Appearance()
    luck: stats.Luck = stats.Luck()
    hp: stats.HitPoints = stats.HitPoints()

    def __post_init__(self):
        self.full_name = self.first_name + " " + self.last_name
        self.sanity.current = self.power.current
        self.hp.current = cthulhu_round((self.constitution.current + self.size.current)/10)
        self.skills = SKILLS1920


if __name__ == "__main__":

    steve = Character("Steve", "Minecraft")
    print(steve.skills.Jump)
    print(steve.skills.Jump + 10)
    print(steve.skills.Jump)
    # for skills with spaces
    #print(steve.skills.__dict__["Arts and Craft"])