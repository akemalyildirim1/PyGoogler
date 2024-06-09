"""Print module for pygoogler CLI."""

import typer


def print_message(message: str) -> None:
    """Print a normal message.

    Arguments:
        message: The message to print.

    Returns:
        None.
    """
    typer.echo(message)


def print_success_message(message: str) -> None:
    """Print a success message.

    Arguments:
        message: The message to print.

    Returns:
        None.
    """
    typer.echo(typer.style(message, fg=typer.colors.GREEN, bold=True))


def print_error_message(message: str) -> None:
    """Print an error message.

    Arguments:
        message: The message to print.

    Returns:
        None.
    """
    typer.echo(typer.style(message, fg=typer.colors.RED, bold=True))
