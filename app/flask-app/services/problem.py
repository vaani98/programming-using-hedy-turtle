import yaml
import json
import logging

from coin_sweeper import CoinSweeper
from grid import Grid
from utils import get_for_every_position

""" Problem Service """

def get_initial_state(problem):
    """Return intial state of problem"""
    problem_details = problem["problem"]
    grid = Grid.get_instance()
    bot = CoinSweeper.get_instance()
    grid_state = grid.get_state()
    coin_sweeper_state = bot.get_state()
    grid_state.update(coin_sweeper_state)
    problem_type = problem_details["problem_type"]
    grid_state["type"] = problem_type
    if problem_type == "state_match":
        if "coin_sweeper" in problem["answer"]["state"]:
            grid_state["homes"] = [problem["answer"]["state"]["coin_sweeper"]]
    return grid_state

def setup_grid_and_bot(problem):
    """Initialise the state of the grid"""
    state = problem["initial_state"]
    bot = CoinSweeper.get_instance()
    coin_sweeper_state = state["coin_sweeper"]
    if "pen" in coin_sweeper_state:
        bot.configure(coin_sweeper_state["position"]["row"], coin_sweeper_state["position"]["column"], coin_sweeper_state["dir"], coin_sweeper_state["pen"])
    else:
        bot.configure(coin_sweeper_state["position"]["row"], coin_sweeper_state["position"]["column"], coin_sweeper_state["dir"], "down")
    grid = Grid.get_instance()
    grid_state = state["grid"]
    rows = grid_state["dimensions"]["row"]
    columns = grid_state["dimensions"]["column"]
    coins_per_position = obstacles_per_position = None
    if "coins" in grid_state:
        coins_per_position = get_for_every_position(grid_state["coins"], rows, columns)
    else:
        grid_state["coins"] = None
    if "obstacles" in grid_state:
        obstacles_per_position = get_for_every_position(grid_state["obstacles"], rows, columns, False)
    else:
        grid_state["obstacles"] = None
    if not "homes" in grid_state:
        grid_state["homes"] = None
    grid.configure(rows, columns, grid_state["coins"], coins_per_position, grid_state["obstacles"], obstacles_per_position, grid_state["homes"], statement, problem_spec)

def initialise(problem_file_path):
    """Initialises chosen problem"""
    # Read problem
    with open(problem_file_path) as problem_file:
        problem = json.loads(problem_file.read())
    setup_grid_and_bot(problem)
    return get_initial_state(problem)

def render(level):
    """ Renders selected problem grid """
    with open('config.yaml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        problem_file_path = config['levels'][level]['file']
        problem_name = config['levels'][level]['name']
    logging.info(f'Setting problem to {problem_name}')
    return initialise(problem_file_path)

def exists(email):
    """ Does the User exist? """
    if email == "abcd@gmail.com":
        return True
    return False
