import random
from importlib.resources import open_text
from cocpyth.dtypes.character import GenderEnum

# TODO: implement a random name generator (from 1920 names lists?)
def generate_name(gender:GenderEnum):
    namesf = "male_names.tsv"    
    lnamesf = "lnames.txt"

    if gender == GenderEnum.F:
        namesf = "fe" + namesf

    with open_text("cocpyth.data", namesf) as f:
        names = f.readlines()
    with open_text("cocpyth.data", lnamesf) as f:
        lnames = f.readlines()

    names = [n.strip() for n in names]
    lnames = [n.strip() for n in lnames]
    return random.choice(names), random.choice(lnames)