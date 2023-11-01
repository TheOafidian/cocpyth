import click
from enum import Enum
from typing import Union
from pydantic import BaseModel
from cocpyth.dtypes.character import Character
from cocpyth.utils.io import save_character, load_character


class GenderEnum(str, Enum):
    M = "male"
    F = "female"


class CharacterGenerator(BaseModel):
    rstats: bool
    rgender: Union[bool, GenderEnum]
    rname: bool


def print_yellow(string):
    click.echo(click.style(string, fg="yellow"))


# @click.group()
# @click.option("-n", "--rname", default=False, prompt="Roll random stats?", help="Wether to randomly roll for the character's stats.", type=bool)
# @click.option("-g", "--rgender", type=click.Choice(["M","F","False"], case_sensitive=False) ,default=False, prompt="Pick random biological gender?", help="Wether to pick a random biological gender.")
# @click.pass_context
# def cli(ctx, rstats, rname, rgender):
#    ctx.obj = CharacterGenerator(rstats,rgender,rname)


@click.command()
@click.option("--fname", prompt="First name", help="The character's first name.")
@click.option("--lname", prompt="Last name", help="The character's last name.")
@click.option(
    "-r",
    "--rstats",
    default=True,
    prompt="Roll random stats?",
    help="Wether to randomly roll for the character's stats.",
    type=bool,
)
# @click.pass_obj
def generate_character(fname, lname, rstats):
    if rstats:
        character = Character(first_name=fname, last_name=lname)
        print_yellow(character)
        save_character(character, f"{fname}_{lname}.yaml")
        ld = load_character(f"{fname}_{lname}.yaml")
        print(ld.skills)
        # pick_occupation()

    else:
        character = None
        raise NotImplementedError


if __name__ == "__main__":
    character = generate_character()
