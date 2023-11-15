import os
from prompt_toolkit import prompt, PromptSession, HTML, print_formatted_text as print
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter

from cocpyth.utils.io import save_character, load_character
from cocpyth.generator.character import CharacterGenerator


DEFAULT_JSON = "character.json"

def emphasize(pre:str, emphasis:str, post:str):
    return HTML('{}<b>{}</b>{}'.format(pre, emphasis, post))

def default_param(string:str):
    return f'default: [{string}]'

charsheet_prompt_style = Style.from_dict({
    '' : '',
    'file' : '#884444',
    'default' : '#00aa00'
})

charsheet_message = [
    ("","Enter a "),
    ("class:file", "filename"),
    ("", " for your charactersheet "),
    ("class:default", default_param(DEFAULT_JSON)),
    ("", ": ")
]


random_generation_message = [
    ("","Generate character randomly? "),
    ("class:default", default_param("Y")),
    ("", ": ")
]



def character_generation_prompts(session:PromptSession):
    
    random_gender_message = [
        ("","Which biological gender? [F/M/Random]"),
        ("class:default", default_param("Random")),
        ("", ": ")
    ]

    random_name_message = [
        ("","Generate a random name? "),
        ("class:default", default_param("Y")),
        ("", ": ")
    ]

    rchoice = WordCompleter(["Random", "random"])
    rgender = session.prompt(random_gender_message, style=charsheet_prompt_style, completer=rchoice)
    if rgender.upper() not in ["M", "F"]:
        rgender = True
    else: rgender = rgender.upper()
    fname = session.prompt(random_name_message, style=charsheet_prompt_style, completer=rchoice)
    rname = True
    if fname.upper() not in ["Y","YES", ""]:
        rname=False

    return CharacterGenerator(rstats=True, rgender=rgender, rname=rname).generate()


if __name__ == "__main__":
    

    session = PromptSession()
    character_loaded = False

    char_sheet_file = session.prompt(charsheet_message, style=charsheet_prompt_style)
    if char_sheet_file.lower() in ["y","","yes"]:
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
        save_character(character, char_sheet_file)



    #generation_method = session.prompt(random_generation_message, style=charsheet_prompt_style)
