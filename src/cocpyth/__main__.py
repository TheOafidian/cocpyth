import os
from prompt_toolkit import prompt, HTML, print_formatted_text as print
from prompt_toolkit.completion import WordCompleter

from cocpyth import POSSIBLE_COMMANDS, DEFAULT_JSON, DEFAULT_PDF
from cocpyth.utils.io import load_character
from cocpyth.dtypes.character import Character

from cocpyth.prompts.validation import (
    CommandValidator, 
    YesNoValidator, 
    yes_or_no,  
    interpret_skill,
    interpret_command
)
from cocpyth.utils.sheet import download_charactersheet, fill_in_charactersheet
from cocpyth.prompts.generate_character import create_new_character, charsheet_prompt_style, charsheet_message, _prompt_for_skill


def emphasize(pre: str, emphasis: str, post: str):
    return HTML('{}<b>{}</b>{}'.format(pre, emphasis, post))


def default_param(string: str):
    return f'default: [{string}]'


def command_switch(cmd:str, character:Character):
    if cmd == "EXIT":
        exit(1)
    if cmd == "ROLL":
        msg = "Which skill to roll? "
        skill = _prompt_for_skill(msg, character.list_skills())
        interpret_skill(skill, character.list_skills())
        result = character.skills[skill].roll()
        print(result)
    if cmd == "SAVE_SHEET":
        char_sheet_file = prompt(charsheet_message, style=charsheet_prompt_style, placeholder=DEFAULT_PDF)
        if char_sheet_file.lower() in ["y", "", "yes"]:
            char_sheet_file = DEFAULT_PDF

        color = prompt("Would you like a colored character sheet?", style=charsheet_prompt_style, validator=YesNoValidator(), placeholder="Y")
        color = yes_or_no(color)

        sheet = download_charactersheet(char_sheet_file, color=color)
        fill_in_charactersheet(sheet, character)
        print("Saved charactersheet!")

def prompt_for_command(character:Character):

    completer = WordCompleter(POSSIBLE_COMMANDS, ignore_case=True)

    command = prompt(
        "",
        completer=completer,
        placeholder="roll",
        validator=CommandValidator(),
        validate_while_typing=False
    )
    command = interpret_command(command)
    command_switch(command, character)

def cli():

    character_loaded = False

    char_sheet_file = prompt(charsheet_message, style=charsheet_prompt_style, placeholder=DEFAULT_JSON)
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
        character = create_new_character(char_sheet_file) 
    else:
        print("\n", character.format_stats())
    
    command = prompt_for_command(character)
    while command != "exit":
        command = prompt_for_command(character)


if __name__ == "__main__":
    cli()