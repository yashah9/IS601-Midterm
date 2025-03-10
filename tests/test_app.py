'''test_app.py'''
from unittest.mock import MagicMock
import pytest
from app import App, CommandHandler

@pytest.fixture
def app():
    """Create an instance of the App class for testing."""
    return App()

@pytest.fixture
def command_handler():
    """Create an instance of the CommandHandler class for testing."""
    return CommandHandler()

def test_app_get_environment_variable(app, monkeypatch):
    """Test that the application retrieves the correct environment variable."""
    monkeypatch.setenv('ENVIRONMENT', 'DEVELOPMENT')  # Set environment variable
    app.load_environment_variables()  # Load the environment variables
    current_env = app.get_environment_variable('ENVIRONMENT')  # Use the correct method to get the variable
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

def test_app_start_exit_command(monkeypatch, app):
    """Test that the REPL exits correctly on 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    with pytest.raises(SystemExit):
        app.start()  # Ensure the start method raises SystemExit on exit command

def test_app_start_unknown_command(monkeypatch, capfd, app):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with pytest.raises(SystemExit):
        app.start()  # Ensure the start method raises SystemExit after handling an unknown command

    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out

def test_command_handler_register_command(command_handler):
    """Test command registration."""
    mock_command = MagicMock()

    command_handler.register_command("mock", mock_command)
    assert "mock" in command_handler.commands
    assert command_handler.commands["mock"] == mock_command

def test_command_handler_execute_command_valid(command_handler):
    """Test executing a valid command."""
    mock_command = MagicMock()
    mock_command.execute.return_value = "Executed"

    command_handler.register_command("mock", mock_command)
    result = command_handler.execute_command("mock")

    assert result == "Executed"
    mock_command.execute.assert_called_once()

def test_command_handler_execute_command_invalid(command_handler):
    """Test executing an invalid command."""
    with pytest.raises(KeyError):
        command_handler.execute_command("invalid_command")