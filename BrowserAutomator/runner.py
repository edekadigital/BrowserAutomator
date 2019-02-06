from BrowserAutomator.file_reader import read_actions


def get_actions(filename, types):
    """reads actions from a yaml and returns the corresponding functions"""
    actions = read_actions(filename)
    return get_action_functions(actions, types)


def get_action_functions(actions: list, types: dict):
    """given a list of actions and a dictionary of action names mapped to the corresponding functions
       returns a list of tuples with the function and parameters"""
    all_actions = []
    for action in actions:
        for action_type, content in action.items():
            f = types[action_type]
            all_actions.append((f, content))
    return all_actions
