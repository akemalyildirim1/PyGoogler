"""Project main file."""

from pathlib import Path
from typing import Annotated

import typer

from .cli import ItemsList, print_error_message, print_message, print_success_message
from .configuration import ConfigurationModel
from .exceptions import ApplicationClosedError, InvalidAPIKeyError, NotFoundError
from .models import SearchResponse, SearchResponses
from .search_api import GoogleSearchAPI
from .service import ConfigurationService, SearchService, ServiceFactory

app: typer.Typer = typer.Typer(help="Google search CLI.")

CONFIGURATION_FILE_PATH: Annotated[Path, "The configuration file path."] = Path(
    "./config.json"
)

configuration_service: ConfigurationService = (
    ServiceFactory.create_configuration_service()
)
search_service: SearchService = ServiceFactory.create_search_service(
    search_api=GoogleSearchAPI()
)


@app.command("init")
@app.command("start")
def start() -> None:
    """Create an initial configuration file.

    This will create an initial configuration file with the default values.
    """
    print_success_message("Welcome to the Google search CLI setup.")
    print_message("Creating an initial configuration file.")
    configuration_service.reset_config(configuration_file_path=CONFIGURATION_FILE_PATH)
    print_success_message("Configuration file created successfully.")


@app.command("reset")
def reset() -> None:
    """Reset the configuration file.

    This will reset the configuration file to the initial state.
    """
    if not typer.confirm("Are you sure you want to reset the configuration file?"):
        print_error_message("Resetting the configuration file aborted.")
        raise typer.Abort()
    print_message("Resetting the configuration file.")
    configuration_service.reset_config(configuration_file_path=CONFIGURATION_FILE_PATH)
    print_success_message("Configuration file reset successfully.")


@app.command("configure")
def update_config() -> None:
    """Update the configuration file.

    This will update the configuration file with your custom search
    API key and the programmable search engine ID.
    """
    custom_search_api_key: str = typer.prompt("Enter your Google Search API key")
    programmable_search_engine_id: str = typer.prompt(
        "Enter your Programmable Search Engine ID"
    )

    configuration: ConfigurationModel = ConfigurationModel(
        custom_search_api_key=custom_search_api_key,
        programmable_search_engine_id=programmable_search_engine_id,
    )
    print_message("Updating the configuration file.")
    configuration_service.update_config(
        configuration_file_path=CONFIGURATION_FILE_PATH, configuration=configuration
    )
    print_success_message("Configuration file updated successfully.")


@app.command("search")
def search(
    query: Annotated[list[str], typer.Argument()],
    detail: Annotated[
        bool,
        typer.Option(
            help="""
        Show the details of the search results.

        By default, it will show the details of the
        search results.
        """
        ),
    ] = True,
) -> None:
    """Search for the given query.

    This will search for the given query and display the results.
    """
    query_str: str = " ".join(query)
    try:
        items: SearchResponses = search_service.main(query=query_str)
        selected_item: SearchResponse = ItemsList(items=items, show_details=detail)()
        if not selected_item:
            raise ApplicationClosedError("Application closed.")
        typer.launch(selected_item.link)
    except ValueError as e:
        exception_to_message = {
            InvalidAPIKeyError: "Your credentials are invalid. "
            "Please update the configuration.",
            NotFoundError: "No search results found.",
            ApplicationClosedError: str(e),
        }
        error_message: str = exception_to_message.get(type(e), "An error occurred.")
        print_error_message(error_message)
        raise typer.Abort()
