"""Items list module."""

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

from pygoogler.models import SearchResponse, SearchResponses


class ItemsList:
    """List all given items."""

    def __init__(self, items: SearchResponses, show_details: bool = True):
        """Initialize the class."""
        self.items: SearchResponses = items

        self.show_details: bool = show_details
        self.selected_index: int = 0

    def __call__(self) -> SearchResponse:
        """Call the application.

        Returns:
            The selected search response.

        Raises:
            ApplicationClosedError: If the application is closed.
        """
        self.selected_index = 0
        app: Application = self.generate_application()
        return app.run()

    def generate_application(self) -> Application:
        """Generate application."""
        style: Style = Style.from_dict(
            {
                "selected": "fg:ansiyellow bg:black bold underline",
                "unselected": "bg:ansiblack fg:ansiwhite",
                "detail": "fg:ansiblue italic",
            }
        )

        # Application layout
        result_control: FormattedTextControl = FormattedTextControl(
            text=self.get_result_text, show_cursor=False
        )
        result_window: Window = Window(
            content=result_control,
            wrap_lines=True,
        )
        layout: Layout = Layout(HSplit([result_window]))
        return Application(
            layout=layout,
            key_bindings=self.generate_key_bindings(),
            full_screen=False,
            style=style,
        )

    def generate_key_bindings(self) -> KeyBindings:
        """Generate key bindings for the application."""
        kb: KeyBindings = KeyBindings()

        @kb.add("c-c")
        def _(_):
            """Close the application."""
            self.close(result=None)

        @kb.add("up")
        def _(event):
            """Go up in the list of results."""
            self.selected_index = (self.selected_index - 1) % len(self.items)
            event.app.invalidate()

        @kb.add("down")
        def _(event):
            """Go down in the list of results."""
            self.selected_index = (self.selected_index + 1) % len(self.items)
            event.app.invalidate()

        @kb.add("enter")
        def _(_):
            """Select the current result and display it.

            Returns:
                The selected search response.
            """
            self.close(result=self.items[self.selected_index])

        @kb.add("i")
        def _(event):
            """Toggle the current result's details."""
            self.show_details = not self.show_details
            event.app.invalidate()

        return kb

    def get_result_text(self) -> list[tuple[str, str]]:
        """Get the result text to display."""
        result_text: list[tuple[str, str]] = []
        for i, item in enumerate(self.items):
            if i == self.selected_index:
                result_text.append(
                    ("class:selected", f"{i + 1}. {item.title} {item.link}\n")
                )
                if self.show_details:
                    result_text.append(
                        ("class:detail", f"Detail {i + 1}: {item.snippet}\n")
                    )
            else:
                result_text.append(
                    ("class:unselected", f"{i + 1}. {item.title} {item.link}\n")
                )
        return result_text

    def close(self, result: SearchResponse | None) -> None:
        """Close the application.

        Arguments:
            result: Result of the application if any.

        Returns:
            None.
        """
        get_app().exit(result=result)
