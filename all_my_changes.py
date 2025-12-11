#!/usr/bin/env python3
"""
A simple Hello World program to test the PR AI Assistant bot.
"""


def greet(name: str = "World") -> str:
    """
    Returns a greeting message.
    
    Args:
        name: The name to greet. Defaults to "World".
    
    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"


def main() -> None:
    """Main entry point for the hello world program."""
    message = greet()
    print(message)
    
    # Greet some specific people
    for person in ["Alice", "Bob", "Charlie"]:
        print(greet(person))


if __name__ == "__main__":
    main()
