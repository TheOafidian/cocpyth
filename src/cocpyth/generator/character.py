import random
from typing import Union
from pydantic.dataclasses import dataclass
from click import prompt
from cocpyth.generator.name import generate_name
from cocpyth.dtypes.character import GenderEnum, Character

@dataclass
class CharacterGenerator():
    rstats: bool
    rgender: Union[bool, GenderEnum]
    rname: Union[bool,str]

    def generate(self):

        if self.rgender == True:
            self.rgender = random.choice(list(GenderEnum))

        if not self.rname:
            fname = prompt("First name?", type=str)
            lname = prompt("Last name?", type=str)
        elif type(self.rname) == str:
            fname, lname = self.rname.split(" ", 1)
        else: 
            fname, lname = generate_name(self.rgender)
        if self.rstats:
            character = Character(first_name=fname, last_name=lname)
        else:
            # TODO: lookup array spending mode and implement
            raise NotImplementedError
    
        return character