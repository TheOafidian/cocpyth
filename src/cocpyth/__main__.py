import os
from prompt_toolkit import PromptSession, HTML, print_formatted_text as print
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter

from cocpyth.utils.io import save_character, load_character
from cocpyth.generator.character import CharacterGenerator
from cocpyth.dtypes.occupation import OCCUPATIONS1920
from cocpyth.dtypes.skill import SKILLS1920
from cocpyth.dtypes.character import Character
from cocpyth.dtypes.occupation import Occupation
from cocpyth.prompts.validation import OccupationValidator, SkillValidator, YesNoValidator, GenderOrRandomValidator, gender_or_random, yes_or_no, interpret_occupation, interpret_skill

DEFAULT_JSON = "character.json"


def emphasize(pre: str, emphasis: str, post: str):
    return HTML('{}<b>{}</b>{}'.format(pre, emphasis, post))


def default_param(string: str):
    return f'default: [{string}]'


charsheet_prompt_style = Style.from_dict({'': '', 'file': '#884444', 'name': '#00aa00', 'number' : 'red'})

charsheet_message = [
    ("", "Enter a "),
    ("class:file", "filename"),
    ("", " for your charactersheet: "),
]



def character_generation_prompts(session: PromptSession):

    random_gender_message = [
        ("", "Which biological gender? "),
    ]

    random_name_message = [("", "Generate a random name? ")]

    rgender = session.prompt(random_gender_message, style=charsheet_prompt_style,placeholder="Random", validator=GenderOrRandomValidator())
    rgender = gender_or_random(rgender)

    fname = session.prompt(random_name_message, style=charsheet_prompt_style, validator=YesNoValidator(), placeholder="Y")
    rname = yes_or_no(fname)

    random_stats_message = [("", "Generate character's stats randomly? ")]
    rstats = session.prompt(random_stats_message, style=charsheet_prompt_style, validator=YesNoValidator(), placeholder="Y")
    rstats = yes_or_no(rstats)

    return CharacterGenerator(rstats=rstats, rgender=rgender, rname=rname).generate()


def select_occupation(session: PromptSession, name:str):

    occupation_message = [
        ("", "Which occupation does "),
        ("class:name", name),
        ("",  " practice? ")
    ]
    occupations = list(OCCUPATIONS1920.keys())
    valid_choices = occupations + ["Random",  ""]
    occupation_choices = WordCompleter(valid_choices, ignore_case=True)

    occupation = session.prompt(
        occupation_message,
        style=charsheet_prompt_style,
        completer=occupation_choices,
        placeholder="Random",
        validator=OccupationValidator(),
    )
    occupation = interpret_occupation(occupation)

    return OCCUPATIONS1920[interpret_occupation(occupation)]

def _prompt_for_skill(session: PromptSession, message: str, skills:list):
    skill_choices = WordCompleter(skills, ignore_case=True)

    skill = session.prompt(
        message,
        style=charsheet_prompt_style,
        completer=skill_choices,
        validator=SkillValidator(skills),
    )
    return interpret_skill(skill, skills)



def pick_skills(occupation: Occupation, options:list):

    pick_message = [
        ("", "You still have "),
        ("class:number", str(occupation.skill_choices)),
    ]
    
    if occupation.skill_choices > 1:
        pick_message.append(("", " skills"))
    else: pick_message.append(("", " skill"))
    
    pick_message.append(("", " to pick you've trained in your occupation.\nWhat skill do you choose? "))
    skill = _prompt_for_skill(session, pick_message, options)
    occupation.skills.append(skill)
    occupation.skill_choices -= 1

def spend_occupational_sp(session: PromptSession, character: Character, occupation: Occupation):

    spend_message = [
        ("", "You have "),
        ("class:number", str(character.occupational_skill_points)),
        ("", " occupational skill points left. What will you spend them on? ")
    ]
    skill_choices = occupation.skills
    skill = _prompt_for_skill(session, spend_message, skill_choices)
    
    # Then ask for skillpoints to spend
    raise NotImplementedError


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
        print("\n", character.format_stats())
        
        # Add occupation and skill pool
        occupation = select_occupation(session, character.full_name)
        character.add_occupation(occupation)

        while occupation.skill_choices > 0:
            pick_skills(occupation, list(SKILLS1920.keys()))

        while character.occupational_skill_points > 0:
            spend_occupational_sp(session, character, occupation)

        save_character(character, char_sheet_file)
    
    if character_loaded:
        print("\n", character.format_stats())
        # TODO: implement different commands: roll, improve, exit
        raise NotImplementedError
