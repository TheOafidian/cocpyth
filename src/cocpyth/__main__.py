import os
from prompt_toolkit import prompt, PromptSession, HTML, print_formatted_text as print
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter

from cocpyth.utils.io import save_character, load_character
from cocpyth.generator.character import CharacterGenerator
from cocpyth.dtypes.occupations import OCCUPATIONS1920
from cocpyth.prompts.validation import OccupationValidator, YesNoValidator, GenderOrRandomValidator, gender_or_random, yes_or_no, interpret_occupation

DEFAULT_JSON = "character.json"


def emphasize(pre: str, emphasis: str, post: str):
    return HTML('{}<b>{}</b>{}'.format(pre, emphasis, post))


def default_param(string: str):
    return f'default: [{string}]'


charsheet_prompt_style = Style.from_dict({'': '', 'file': '#884444', 'default': '#00aa00'})

charsheet_message = [
    ("", "Enter a "),
    ("class:file", "filename"),
    ("", " for your charactersheet: "),
]


random_generation_message = [("", "Generate character randomly? ")]

def character_generation_prompts(session: PromptSession):

    random_gender_message = [
        ("", "Which biological gender? [F/M/Random]\n"),
    ]

    random_name_message = [("", "Generate a random name?\n")]

    rgender = session.prompt(random_gender_message, style=charsheet_prompt_style,placeholder="Random", validator=GenderOrRandomValidator())
    rgender = gender_or_random(rgender)

    fname = session.prompt(random_name_message, style=charsheet_prompt_style, validator=YesNoValidator(), placeholder="Y")
    rname = yes_or_no(fname)

    return CharacterGenerator(rstats=True, rgender=rgender, rname=rname).generate()


def select_occupation(session: PromptSession, name:str):

    occupation_message = [
        ("", f"Which occupation does {name} practice?\n"),
    ]
    occupations = list(OCCUPATIONS1920.keys())
    valid_choices = occupations + ["Random",  ""]
    occupation_choices = WordCompleter(valid_choices, ignore_case=True, WORD=True)

    occupation = session.prompt(
        occupation_message,
        style=charsheet_prompt_style,
        completer=occupation_choices,
        placeholder="Random",
        validator=OccupationValidator(),
    )
    occupation = interpret_occupation(occupation)

    return OCCUPATIONS1920[interpret_occupation(occupation)]


if __name__ == "__main__":

    session = PromptSession()
    character_loaded = False

    char_sheet_file = session.prompt(charsheet_message, style=charsheet_prompt_style, placeholder=DEFAULT_JSON)
    if char_sheet_file.lower() in ["y", "", "yes"]:
        char_sheet_file = DEFAULT_JSON

    if os.path.exists(os.path.join(".", char_sheet_file)):
        try:
            character = load_character(char_sheet_file)
            print(emphasize("", char_sheet_file, " found!"))
            print(HTML(f"Loaded <violet>{character.full_name}</violet>"))
            character_loaded = True
        except AttributeError:
            print(emphasize("", char_sheet_file, f" is not a valid character file. Defaulting to {DEFAULT_JSON}."))
            char_sheet_file = DEFAULT_JSON

    if not character_loaded:
        character = character_generation_prompts(session)
        # Add occupation and skill pool
        occupation = select_occupation(session, character.full_name)
        character.add_occupation(occupation)
        save_character(character, char_sheet_file)

    # generation_method = session.prompt(random_generation_message, style=charsheet_prompt_style)
