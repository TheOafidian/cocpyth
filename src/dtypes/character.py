from pydantic.dataclasses import dataclass
import stats

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
        self.sanity.current = self.power.current
        self.hp.current = stats.cthulhu_round((self.constitution.current + self.size.current)/10)

if __name__ == "__main__":

    steve = Character("Steve", "Minecraft")
    print(steve)