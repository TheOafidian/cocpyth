import click
from dtypes.character import Character

def print_yellow(string):
    click.echo(click.style(string, fg="yellow"))

@click.command()
@click.option("--fname", prompt="First name", help="The character's first name.")
@click.option("--lname", prompt="Last name", help="The character's last name.")
@click.option("--rstats", default=True, prompt="Roll random stats?", help="Wether to randomly roll for the character's stats.")
def generate_character(fname, lname, rstats):
    if rstats:
        character = Character(first_name=fname, last_name=lname)
        print_yellow(character)
        
    else:
        character = None
        raise NotImplementedError
    


if __name__ == "__main__":
    character = generate_character()
