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

        # Use tabulate to format the DataFrame as a table
        return tabulate(self.history_df.values, headers=["Command"], tablefmt="fancy_grid")

    def add_to_history(self, command_str):
        """Add a new command to the history, except for history management commands."""
        # Exclude history commands (save, load, clear, delete) from being added to the history
        if command_str.startswith("history"):
            return

        # Add the command to the DataFrame
        new_entry = pd.DataFrame([[command_str]], columns=["Command"])
        self.history_df = pd.concat([self.history_df, new_entry], ignore_index=True)

    def save_history(self, filename="history.csv"):
        """Save the history to a CSV file."""
        if self.history_df.empty:
            return "No command history to save."
        self.history_df.to_csv(filename, index=False)
        return f"History saved to {filename}."

    def load_history(self, filename="history.csv"):
        """Load the history from a CSV file."""
        if os.path.exists(filename):
            self.history_df = pd.read_csv(filename)
            return f"History loaded from {filename}."

        return f"History file '{filename}' not found."

    def clear_history(self):
        """Clear the in-memory history."""
        self.history_df = pd.DataFrame(columns=["Command"])
        return "History cleared."

    def delete_history(self, filename="history.csv"):
        """Delete the history CSV file."""
        if os.path.exists(filename):
            os.remove(filename)
            return f"History file '{filename}' deleted."

        return f"No history file found at '{filename}'."