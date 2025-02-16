import random
from typing import Union
from pydantic.dataclasses import dataclass
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from cocpyth.prompts.validation import is_text
from cocpyth.generator.name import generate_name
from cocpyth.dtypes.character import GenderEnum, Character

@dataclass
class CharacterGenerator():
    rstats: bool
    rgender: Union[bool, GenderEnum]
    rname: Union[bool,str]
    seed: Union[bool,int] = False

    def generate(self):

        if self.seed:
            random.seed(self.seed)
            #raise NotImplementedError("Implement seeded version")

        if self.rgender == True:
            self.rgender = random.choice(list(GenderEnum))

        if not self.rname:
            
            name_validator = Validator.from_callable(
                is_text,
                error_message="Name should be atleast two characters long",
                move_cursor_to_end=True
            )
            
            fname = prompt("First name?", validator=name_validator)
            lname = prompt("Last name?", validator=name_validator)
        elif type(self.rname) == str:
            fname, lname = self.rname.split(" ", 1)
        else: 
            fname, lname = generate_name(self.rgender, seed=self.seed)
        if self.rstats:
            character = Character(first_name=fname, last_name=lname, seed=self.seed)
        else:
            # TODO: lookup array spending mode and implement
            raise NotImplementedError
    
        return character