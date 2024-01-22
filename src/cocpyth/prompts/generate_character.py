import random

from prompt_toolkit import prompt, print_formatted_text as print
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

from cocpyth.generator.character import CharacterGenerator
from cocpyth.dtypes.character import Character
from cocpyth.dtypes.occupation import Occupation, OCCUPATIONS1920
from cocpyth.dtypes.skill import SKILLS1920
from cocpyth.utils.io import save_character

from cocpyth.prompts.validation import ( 
    MaxNumberValidator, 
    OccupationValidator, 
    SkillValidator, 
    YesNoValidator, 
    GenderOrRandomValidator, 
    gender_or_random, 
    yes_or_no, 
    interpret_occupation, 
    interpret_skill,
)

charsheet_prompt_style = Style.from_dict({'': '', 'file': '#884444', 'name': '#00aa00', 'number' : 'red'})

charsheet_message = [
    ("", "Enter a "),
    ("class:file", "filename"),
    ("", " for your charactersheet: "),
]

def character_generation_prompts(seed=False):

    random_gender_message = [
        ("", "Which biological gender? "),
    ]

    random_name_message = [("", "Generate a random name? ")]

    rgender = prompt(random_gender_message, style=charsheet_prompt_style,placeholder="Random", validator=GenderOrRandomValidator())
    rgender = gender_or_random(rgender)

    fname = prompt(random_name_message, style=charsheet_prompt_style, validator=YesNoValidator(), placeholder="Y")
    rname = yes_or_no(fname)

    random_stats_message = [("", "Generate character's stats randomly? ")]
    rstats = prompt(random_stats_message, style=charsheet_prompt_style, validator=YesNoValidator(), placeholder="Y")
    rstats = yes_or_no(rstats)

    return CharacterGenerator(rstats=rstats, rgender=rgender, rname=rname, seed=seed).generate()


def select_occupation(name:str):

    occupation_message = [
        ("", "Which occupation does "),
        ("class:name", name),
        ("",  " practice? ")
    ]
    occupations = list(OCCUPATIONS1920.keys())
    valid_choices = occupations + ["Random",  ""]
    occupation_choices = WordCompleter(valid_choices, ignore_case=True)

    occupation = prompt(
        occupation_message,
        style=charsheet_prompt_style,
        completer=occupation_choices,
        placeholder="Random",
        validator=OccupationValidator(),
    )
    occupation = interpret_occupation(occupation)

    return OCCUPATIONS1920[interpret_occupation(occupation)]

def _prompt_for_skill(message: str, skills:list):
    FORBIDDEN_SKILLS = {"Cthulhu Mythos", "Credit Rating"}
    skills = [s for s in skills if s not in FORBIDDEN_SKILLS]
    skills.append("Random")
    skills.append("")
    skill_choices = WordCompleter(skills)

    skill = prompt(
        message,
        style=charsheet_prompt_style,
        completer=skill_choices,
        validator=SkillValidator(skills),
        placeholder="Random"
    )
    if skill == "Random" or skill == "":
        skills.remove("Random")
        skills.remove("")
        skill = random.choice(skills)
        print(f"\nPicked {skill}")

    return interpret_skill(skill, skills)


def pick_skills(occupation: Occupation, options:list, counts_as_skill_choice=True):

    pick_message = [
        ("", "You still have "),
        ("class:number", str(occupation.skill_choices)),
    ]
    
    if occupation.skill_choices > 1:
        pick_message.append(("", " skills"))
    else: pick_message.append(("", " skill"))
    
    pick_message.append(("", " to pick you've trained in your occupation.\nWhat skill do you choose? "))
    options = [option for option in options if option not in occupation.skills]
    
    if not counts_as_skill_choice:
        pick_message = "Choose from the following skills: "
    
    skill = _prompt_for_skill(pick_message, options)
    occupation.skills.append(skill)
    if counts_as_skill_choice:
        occupation.skill_choices -= 1
    return skill

def spend_occupational_sp(character: Character, occupation: Occupation):

    spend_message = [
        ("", "You have "),
        ("class:number", str(character.occupational_skill_points)),
        ("", " occupational skill points left. What will you spend them on? ")
    ]
    skill_choices = occupation.skills
    skill = _prompt_for_skill(spend_message, skill_choices)
    improvement_possible = character.skills[skill].max - character.skills[skill].current
    max_points_to_spend = min(character.occupational_skill_points, improvement_possible)
    # Then ask for skillpoints to spend
    amount_sp = prompt(
        f"How many points? You can spend {max_points_to_spend}. ",
        validator=MaxNumberValidator(min(character.occupational_skill_points, improvement_possible)),
        validate_while_typing=False,
    )
    character.spend_occupational_skill_points(skill, int(amount_sp))


def spend_personal_sp(character: Character):

    spend_message = [
        ("", "You have "),
        ("class:number", str(character.personal_skill_points)),
        ("", " personal skill points left. What will you spend them on? ")
    ]
    skill_choices = list(character.skills.keys())
    skill = _prompt_for_skill(spend_message, skill_choices)
    improvement_possible = character.skills[skill].max - character.skills[skill].current
    max_points_to_spend = min(character.personal_skill_points, improvement_possible)
    # Then ask for skillpoints to spend
    amount_sp = prompt(
        f"How many points? You can spend {max_points_to_spend}. ",
        validator=MaxNumberValidator(min(character.personal_skill_points, improvement_possible)),
        validate_while_typing=False,
    )
    if amount_sp != "":
        character.spend_personal_skill_points(skill, int(amount_sp))


def create_new_character(char_sheet_file) -> Character:
    """Create a new character"""
    character = character_generation_prompts()
    print("\n", character.format_stats())
    
    # Add occupation and skill pool
    occupation = select_occupation(character.full_name)
    character.add_occupation(occupation)

    if len(occupation.specialization_choices) > 0:
        specializations = occupation.specialization_choices
        for i in range(occupation.specialization_n_choices):
            chosen_skill = pick_skills(occupation, specializations, counts_as_skill_choice=False)
            specializations.remove(chosen_skill)

    if len(occupation.specific_skill_choices) > 0:
        for choice in occupation.specific_skill_choices:
            pick_skills(occupation, choice, counts_as_skill_choice=False)

    while occupation.skill_choices > 0:
        pick_skills(occupation, list(SKILLS1920.keys()))

    while character.occupational_skill_points > 0:
        spend_occupational_sp(character, occupation)

    while character.personal_skill_points > 0:
        spend_personal_sp(character)

    save_character(character, char_sheet_file)
    return character
