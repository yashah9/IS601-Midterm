"""

This module contains the implementation of the MeanCommand class,
which calculates the mean of a given set of numbers.
"""

from statistics import mean
from app.command import Command

class MeanCommand(Command):
    """Command class to calculate the mean of a set of numbers."""

    def execute(self, *args):
        if not args:
            return "Please provide at least one number to calculate the mean."

        numbers = [float(num) for num in args]  # Ensure args are converted to floats
        return f"The mean of {', '.join(map(str, numbers))} is {mean(numbers)}."