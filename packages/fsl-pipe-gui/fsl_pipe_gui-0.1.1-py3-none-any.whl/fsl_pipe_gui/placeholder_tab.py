"""
Textual tab allowing the editing of placeholder values.

The main goal of this tab is to allow the placeholder values
to be changed from that included within the user-provied `FileTree`.
These changes are immediately made into the `FileTree`.
"""
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label

from .all_panes import AllPanes, PipelineSelector


class PlaceholderEditor(App):
    """
    GUI to view pipeline.

    There are two separate pages (visiblity set by `show_page`):
    - `placeholder_tab` allows the user to change the placeholder values.
    - `output_tab` allows the user to select the requested output files.
    """

    TITLE = "FSL pipeline"

    def __init__(self, selector: PipelineSelector):
        """Create the pipeline GUI."""
        super().__init__()
        self.selector = selector
        file_tree = selector.file_tree
        self.keys = [Label(k) for k in file_tree.placeholders.keys()]
        self.values = [
            Input(", ".join(v) if isinstance(v, list) else v)
            for v in file_tree.placeholders.values()
        ]

    def compose(self) -> ComposeResult:
        """Build the pipeline GUI."""
        yield Header()
        yield Vertical(
            Label("step 1: optionally edit placeholder values"),
            Horizontal(
                Vertical(Label("Placeholders"), *self.keys),
                Vertical(Label("Values"), *self.values),
            ),
            Button("Continue"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        """Continue to the next app."""
        new_placeholders = {}
        for key, value in zip(self.keys, self.values):
            text = value.value
            if "," in text:
                new_value = [elem.strip() for elem in text.split(",")]
            else:
                new_value = text.strip()
            new_placeholders[str(key.renderable)] = new_value

        self.selector.update_placeholders(**new_placeholders)
        self.exit(AllPanes.SELECTOR)
