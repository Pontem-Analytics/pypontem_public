import sys
import os
import pandas as pd

sys.path.append("../src/")
import pytest
from src.tpl import tplparser


@pytest.fixture
def command_line_args(request):
    """
    A common fixture which could be passed to all tests in the test script
    """
    args = {}
    args["filepath"] = request.config.getoption("--filepath")
    args["variable"] = request.config.getoption("--variable")
    args["branch"] = request.config.getoption("--branch")
    args["pipe"] = request.config.getoption("--pipe")
    args["index"] = request.config.getoption("--index")
    args["value"] = request.config.getoption("--value")
    return args


def test_invalid_variable_input(command_line_args):
    """
    A test to check if a ValueError is raised if an incorrect variable name is specified
    when the user inputs an extract_trend method
    """
    filepath = command_line_args["filepath"]
    parse = tplparser.tplParser(filepath)
    var = "variable"
    with pytest.raises(ValueError) as excinfo:
        # If ValueError is raised, test passes
        parse.search_catalog(var)
        parse.extract_trend(var)


# def test_valid_variable_input(command_line_args):
#     filepath = command_line_args["filepath"]
#     parse = parser.tplParser(filepath)
#     var = command_line_args["variable"]
#     branch = command_line_args["branch"]
#     pipe = command_line_args["pipe"]
#     parse.search_catalog(var)
#     trend = parse.extract_trend(var, branch, pipe)
#     assert trend is not None


# def test_variable_input(command_line_args):
#     filepath = command_line_args["filepath"]
#     parse = parser.tplParser(filepath)
#     var = command_line_args["variable"]
#     branch = command_line_args["branch"]
#     pipe = command_line_args["pipe"]
#     parse.search_catalog(var)
#     try:
#         trend = parse.extract_trend(var, branch, pipe)
#     except ValueError:
#         with pytest.raises(ValueError):
#             parse.extract_trend(var, branch, pipe)


def test_invalid_branch_input(command_line_args):
    """
    A test to check if a ValueError is raised if an incorrect branch name is specified
    when the user inputs an _extract_branch_profiles method
    """
    parse = tplparser.tplParser(command_line_args["filepath"])
    branch = "branch"
    with pytest.raises(ValueError) as excinfo:
        # If ValueError is raised, test passes
        parse._extract_branch_profiles(branch)


def test_invalid_file_specified(command_line_args):
    """
    A test to check if a file exists
    """
    with pytest.raises(FileNotFoundError) as excinfo:
        parse = tplparser.tplParser(command_line_args["filepath"])
