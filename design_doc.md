# Design Patterns Documentation for Python Calculator

## Introduction
This document provides a detailed explanation of the design patterns used in the Python Calculator project. It outlines the rationale for selecting specific patterns and provides implementation details, demonstrating how these patterns contribute to the overall functionality and maintainability of the application.

## Design Patterns Used

### 1. Command Pattern
The Command Pattern is employed to encapsulate requests as objects, allowing for parameterization and queuing of requests. In this project, each mathematical operation (e.g., addition, subtraction) is represented as a command.

#### Advantages:
- **Decouples** the sender (user input) from the receiver (command execution).
- Facilitates the implementation of features like **command history**, **save/load/delete command history in CSV file**  functionalities.

### 2. Factory Pattern
The Factory Pattern is utilized to create command instances dynamically. This allows for better management of command creation and registration.

#### Advantages:
- Simplifies **object creation** by encapsulating the instantiation logic.
- Supports the addition of new command types without modifying existing code.

### 3. Singleton Pattern
The Singleton Pattern is used to ensure that the application has a single instance of the CommandHandler throughout its lifecycle.

#### Advantages:
- Prevents multiple instances of the CommandHandler, maintaining a **consistent state**.
- Simplifies **global access** to the command management system.

## Rationale for Choosing Design Patterns

- **Command Pattern**: Given the nature of the application, which performs various mathematical operations, the Command Pattern provides a clean way to encapsulate each operation as an object, making it easier to manage and extend.
  
- **Factory Pattern**: As new commands are added (like statistical functions), the Factory Pattern simplifies the process of instantiating these commands, promoting code reuse and reducing duplication.
  
- **Singleton Pattern**: The CommandHandler acts as the central hub for executing commands, so ensuring a single instance helps maintain a clear flow of command processing.

## Implementation Details

### 1. Command Pattern Implementation
In the `app/command/__init__.py`, the Command abstract class defines the interface for all commands. Each command (e.g., AddCommand, SubtractCommand) inherits from this class and implements the execute method.

```python
class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        pass
```

### 2. Factory Pattern Implementation
The command instances are registered in the App class using a method that creates and adds commands to the CommandHandler. This encapsulates the command instantiation logic.

```python
    def register_command(self, name, command):
        self.commands[name] = command
```

### 3. Singleton Pattern Implementation
The CommandHandler instance is created once in the App class, ensuring that all commands are managed through a single object throughout the application lifecycle.

```python
class CommandHandler:
    def __init__(self):
        self.commands = {}
```
