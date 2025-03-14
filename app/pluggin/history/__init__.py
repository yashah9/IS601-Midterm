"""
This module contains the implementation of the HistoryCommand class,
which retrieves and displays the history of executed commands.
"""

import os
import pandas as pd
from tabulate import tabulate
from app.command import Command

class HistoryCommand(Command):
    """Command class to manage and display history of past commands."""

    def __init__(self, history_df):
        """Initialize with a DataFrame to store the command history."""
        self.history_df = history_df

    def execute(self, *args):
        """Execute the command based on user input (show, save, load, clear, delete)."""
        if not args:
            return self.show_history()

        command = args[0].lower()

        if command == "save":
            return self.save_history(args[1] if len(args) > 1 else "history.csv")
        if command == "load":
            return self.load_history(args[1] if len(args) > 1 else "history.csv")
        if command == "clear":
            return self.clear_history()
        if command == "delete":
            return self.delete_history(args[1] if len(args) > 1 else "history.csv")  # Pass filename if provided

        return "Invalid history command. Available commands: show, save, load, clear, delete."

    def show_history(self):
        """Display the history of commands using tabulate for a table-like format."""
        if self.history_df.empty:
            return "No command history available."

        # Format the DataFrame as a table using tabulate
        return tabulate(self.history_df.values, headers=["Command"], tablefmt="fancy_grid")

    def add_to_history(self, command_str):
        """Add a new command to the history, except for history management commands."""
        if command_str.startswith("history"):
            return

        # Update the DataFrame in place by adding a new row
        self.history_df.loc[len(self.history_df)] = command_str

    def save_history(self, filename="history.csv"):
        """Save the history to a CSV file."""
        if self.history_df.empty:
            return "No command history to save."
        self.history_df.to_csv(filename, index=False)
        return f"History saved to {filename}."

    def load_history(self, filename="history.csv"):
        """Load the history from a CSV file, updating the DataFrame in place."""
        if os.path.exists(filename):
            loaded_df = pd.read_csv(filename)
            # Clear the existing DataFrame while keeping its reference intact
            self.history_df.drop(self.history_df.index, inplace=True)
            # Append each command from the loaded DataFrame
            for command in loaded_df["Command"]:
                self.history_df.loc[len(self.history_df)] = command
            return f"History loaded from {filename}."

        return f"History file '{filename}' not found."

    def clear_history(self):
        """Clear the in-memory history while preserving the DataFrame reference."""
        self.history_df.drop(self.history_df.index, inplace=True)
        return "History cleared."

    def delete_history(self, filename="history.csv"):
        """Delete the history CSV file."""
        if os.path.exists(filename):
            os.remove(filename)
            return f"History file '{filename}' deleted."

        return f"No history file found at '{filename}'."