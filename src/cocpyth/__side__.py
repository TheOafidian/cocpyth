import click
from cocpyth.utils.io import save_character, load_character
from cocpyth.generator.character import CharacterGenerator


def print_yellow(string):
    click.echo(click.style(string, fg="yellow"))


@click.group("cocpyth")
@click.argument("filename")
@click.pass_context
def cocpyth(ctx, filename):
   # Translate to boolean if needed
   ctx.obj = dict(
       filename = filename
   )


@cocpyth.command()
@click.option(
    "-r",
    "--rstats",
    default=True,
    prompt="Roll random stats?",
    help="Wether to randomly roll for the character's stats.",
    type=bool,
)
@click.option("-n", "--rname", default=False, prompt="Roll random name?", help="Wether to randomly roll for the character's name.", type=bool)
@click.option("-g", "--rgender", type=click.Choice(["M","F","True"], case_sensitive=False) ,default="True", prompt="Pick random biological gender?", help="Wether to pick a random biological gender.")
@click.pass_obj
def generate_character(ctx, rstats, rname, rgender):
    if rgender == "True":
       rgender = True
   
    generator = CharacterGenerator(rstats, rgender, rname)
    character = generator.generate()
    print_yellow(character)
    save_character(character, ctx["filename"])

def main():
    cocpyth(prog_name="cocpyth")

if __name__ == "__main__":
    main()
