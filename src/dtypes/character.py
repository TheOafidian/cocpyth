from pydantic.dataclasses import dataclass
import stats

@dataclass
class Character():
    first_name: str
    last_name: str
    strength: stats.Strength = stats.Strength()
    dexterity: stats.Dexterity = stats.Dexterity()
    size: stats.Size = stats.Size()
    constitution: stats.Constitution = stats.Constitution()
    intelligence: stats.Intelligence = stats.Intelligence()
    education: stats.Education = stats.Education()
    power: stats.Power = stats.Power()
    appearance: stats.Appearance = stats.Appearance()
    luck: stats.Luck = stats.Luck()


if __name__ == "__main__":

    steve = Character("Steve", "Minecraft")
    print(steve)