# tests/mocks/test_action.py

def test_action_invalid_params_type(action_command):
    with pytest.raises(
        TypeError
    ):  # Or a more specific custom exception, if you define one
        action_command("SomeAction", params="invalid")  # params should be a dict


# Similar tests for invalid action name types, etc.
