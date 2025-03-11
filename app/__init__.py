"""
Main application module for executing various mathematical commands.

This module initializes the application, configures logging,
loads environment variables, and registers commands.
"""

import os
import sys
import logging
import logging.config
import pandas as pd
from dotenv import load_dotenv
from tabulate import tabulate
from app.command import CommandHandler
from app.pluggin.add import AddCommand
from app.pluggin.subtract import SubtractCommand
from app.pluggin.multiply import MultiplyCommand
from app.pluggin.divide import DivideCommand
from app.pluggin.mean import MeanCommand



class App:
    """Main application class to manage command execution."""

    def __init__(self):
        """Initialize the application, configure logging, and load environment variables."""
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = dict(os.environ)
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()
        self.history_df = pd.DataFrame(columns=["Command"])  # Initialize an empty DataFrame for history
        self.register_commands()
        self.load_startup_history()

    def load_startup_history(self):
        """Optionally load history at startup from a CSV file."""
        history_command = self.command_handler.commands.get("history")
        if history_command:
            print(history_command.load_history("history.csv"))  # Load history automatically on startup

    def configure_logging(self):
        """Configure logging for the application from a config file."""
        logging_conf_path = 'logging.conf'  # Path to your logging config file

        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
            logging.info("Logging configured from file: %s", logging_conf_path)
        else:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('logs/app.log'),  # Fallback if config file does not exist
                    logging.StreamHandler()
                ]
            )
            logging.info("Default logging configuration applied.")

    def load_environment_variables(self):
        """Load environment variables into the application's settings."""
        settings = dict(os.environ)  # This method is no longer needed since it's already done in __init__
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, key):
        """Get a specific environment variable from the settings."""
        return self.settings.get(key)

    def register_commands(self):
        """Register all command classes with the command handler."""
        self.command_handler.register_command("add", AddCommand())
        self.command_handler.register_command("subtract", SubtractCommand())
        self.command_handler.register_command("multiply", MultiplyCommand())
        self.command_handler.register_command("divide", DivideCommand())
        self.command_handler.register_command("mean", MeanCommand())
        self.command_handler.register_command("history", HistoryCommand(self.history_df))


    def display_menu(self):
        """Display available commands in the menu."""
        print("Available Commands:")
        print("1. add                        - Add two numbers")
        print("2. subtract                   - Subtract two numbers")
        print("3. multiply                   - Multiply two numbers")
        print("4. divide                     - Divide two numbers")
        print("5. mean                       - Calculate mean of provided numbers")
        print("6. history                    - History of maximum 10 commands")
        print("Type 'exit' to exit the application.")
        print("Dummy Format: add 3 4")

    def handle_command_input(self, cmd_input):
        """Handle the execution of commands based on user input."""
        parts = cmd_input.split()
        command = parts[0]
        args = parts[1:]

        # pylint: disable=unnecessary-dunder-call, invalid-name
        if command in self.command_handler.commands:
            try:
                result = self.command_handler.execute_command(command, *args)
                print(result)
                history_command = self.command_handler.commands.get("history")
                history_command.add_to_history(cmd_input)

            # pylint: disable=broad-exception-caught
            except Exception as e:
                logging.error("Error executing command: %s", e)
                print(f"Error: {e}")
        else:
            logging.error("Unknown command: %s", command)
            print(f"No such command: {command}")

    def get_float_input(self, prompt, is_multiple=False):
        """Get float input from the user."""
        while True:
            try:
                if is_multiple:
                    numbers = input(prompt).strip().split()
                    return [float(num) for num in numbers]  # Convert to float
            except ValueError:
                logging.error("Invalid input for numbers.")
                print("Please enter valid numbers.")
    
    def show_history(self):
        """Display the history of commands using tabulate for a table-like format."""
        if self.history_df.empty:
            print("No command history available.")
        else:
            # Use tabulate to create a nicely formatted table
            print("\nCommand History:")
            print(tabulate(self.history_df.values, headers=["Command"], tablefmt="fancy_grid"))


    def start(self):
        """Start the REPL for command input."""
        self.display_menu()  # Show the command menu at startup
        logging.info("Application started.")

        try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    print("Exiting...")
                    logging.info("Application exit.")
                    sys.exit()  # This will raise SystemExit

                self.handle_command_input(cmd_input)

        except KeyboardInterrupt:
            logging.info("Application interrupted and exiting gracefully.")
        finally:
            logging.info("Application shutdown.")

if __name__ == "__main__":
    app = App()
    app.start()