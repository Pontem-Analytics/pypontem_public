def pytest_addoption(parser):
    """
    Function to add command line arguments
    """
    parser.addoption(
        "--filepath",
        action="store",
        default="C:/Users/HP/Desktop/Pontem Analytics/tpl/new tpl/generic_test.tpl"
    )
    parser.addoption("--variable", action="store", default="PT")
    parser.addoption("--branch", action="store")
    parser.addoption("--pipe", action="store")
    parser.addoption("--index", action="store", type=int, help="Index to compare")
    parser.addoption("--value", action="store")