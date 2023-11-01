from cocpyth.dtypes.character import GenderEnum

# TODO: implement a random name generator (from 1920 names lists?)
def generate_name(gender:GenderEnum):
    if gender == GenderEnum.F:
        return "Alex", "Minecraft"
    else:
        return "Steve", "Minecraft"