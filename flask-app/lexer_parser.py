"""Lexer and parser module for pseudo-code"""
# pylint: disable=invalid-name,unused-argument,global-statement,unused-wildcard-import,wildcard-import
import json
import yaml

from control_hub import *
from grid import Grid
from coin_sweeper import CoinSweeper
from languages.english import english_lexer, english_parser
from languages.kannada import kannada_lexer, kannada_parser
from languages.kanglish import kanglish_lexer, kanglish_parser

# utilities
class LexerError(Exception):
    """Lexer error"""
    # pass

def make_command(command, value = None):
    """Wrap command in JSON response format"""
    if command == "get_row()":
        return {
                "python": command,
                "value": bot.my_row()
               }
    elif command == "get_column()":
        return {
                "python": command,
                "value": bot.my_column()
               }
    elif "get_number_of_coins()" in command:
        return {
                "python": command,
                "number of coins": value
               }
    elif '+' in command or '-' in command or '*' in command or '/' in command or '=' in command:
        return {
                "python": command
               }
    elif command == "error()":
        return {
            "error_message": value,
        }
    else:
        return {
            "python": command,
            "stateChanges": [
                bot.get_state()
            ]
        }

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()

def understand(commands):
    """Convert pseudo-code to Python code to execute"""
    # reinitialize response file
    # Opening config to read grid attributes
    with open('../config.yaml') as req_file:
        configs = yaml.load(req_file, Loader=yaml.FullLoader)
        with open(configs["app"]["results"], "w") as results_file:
            results_file.write(json.dumps([]))
        try:
            if configs["app"]["language"] == "english":
                print("English")
                print(commands)
                python_program = english_parser.parse(commands, lexer=english_lexer)
            elif configs["app"]["language"] == "kannada":
                print("Kannada")
                python_program = kannada_parser.parse(commands, lexer=kannada_lexer)
            elif configs["app"]["language"] == "kanglish":
                print("Kanglish")
                python_program = kanglish_parser.parse(commands, lexer=kanglish_lexer)
        except Exception as exception: # pylint: disable=broad-except
            print(exception)
            return []
    print("Python program: ", python_program)
    if python_program is None:
        exception_raised = "Syntax Error (check the selected language and the corresponding syntax)"
    else:
        exception_raised = None
        try:
            exec(python_program)
        except Exception as e: # pylint: disable=broad-except
            exception_raised = e
            print("Exception raised while parsing: ", e)
    with open(config["app"]["results"]) as results_file:
        response = json.loads(results_file.read())
    if exception_raised is not None:
        response.append({
            "error_message": str(exception_raised)
        })
    response_and_python_program = {
        "python": python_program,
        "response": response
    }
    # print("Response and python program:", response_and_python_program)
    return response_and_python_program
