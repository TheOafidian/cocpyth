import unittest
from unittest.mock import patch
from prompt_toolkit.validation import ValidationError

from cocpyth.prompts.generate_character import character_generation_prompts, select_occupation, yes_or_no, gender_or_random
from cocpyth.dtypes.occupation import OCCUPATIONS1920
from cocpyth.generator.character import CharacterGenerator
# Test for criminal, for 4(|||) rule

def test_generate_criminal():
    generator = CharacterGenerator(rstats=True, rgender=True, rname=True, seed=42)
    character = generator.generate()
    character.add_occupation(OCCUPATIONS1920["Criminal"])
    assert character.occupation.specialization_n_choices == 4
    assert character.occupation.specialization_choices == ['Appraise', 'Disguise', 'Fighting', 'Firearms', 'Locksmith', 'Mechanical Repair', 'Sleight of Hand']


class test_select_occupation(unittest.TestCase):

    @patch('cocpyth.prompts.generate_character.prompt', return_value="Criminal\n")
    def test_valid_choice(self, input):
        self.assertEqual(select_occupation("Test"), OCCUPATIONS1920["Criminal"])  

    @patch('cocpyth.prompts.generate_character.prompt', return_value="Murderclown\n")
    def test_invalid_choice(self, input):
        self.assertRaises(ValidationError, select_occupation, "Test")  

class test_generate_random_char(unittest.TestCase):
    @patch('cocpyth.prompts.generate_character.prompt', return_value="Y\n")
    @patch('cocpyth.prompts.generate_character.prompt', return_value="Y\n")
    @patch('cocpyth.prompts.generate_character.prompt', return_value="Y\n")
    def test_all_random(self, input1, input2, input3):
        character = character_generation_prompts(seed=42)
        same_character = character_generation_prompts(seed=42)
        self.assertEqual(character.first_name, same_character.first_name)
        self.assertEqual(character.last_name, same_character.last_name)
        self.assertEqual(character.sanity.current, same_character.sanity.current)
        other_character = character_generation_prompts(seed=43)
        self.assertNotEqual(character.full_name, other_character.full_name)
        self.assertNotEqual(character.sanity.current, other_character.sanity.current)

