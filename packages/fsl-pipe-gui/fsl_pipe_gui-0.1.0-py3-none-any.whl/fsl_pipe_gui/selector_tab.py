"""Visualise the output selection part of the FSL pipeline GUI."""
import itertools
import os.path as op
from functools import lru_cache

from file_tree import FileTree, Template
from fsl_pipe.job import RunMethod
from rich.style import Style
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, Checkbox, DataTable, Footer, Header, Select, Tree
from textual.widgets.tree import TreeNode

from .all_panes import AllPanes, PipelineSelector


class TemplateSelect(Message, bubble=True):
    """Message sent when a template in the sidebar gets selected."""

    def __init__(self, sender, template: Template):
        """Create template selector."""
        self.template = template
        super().__init__(sender)


class OutputSelector(App):
    """Textual application to select pipeline output templates/files."""

    TITLE = "FSL pipeline"
    CSS_PATH = "css/selector.css"

    BINDINGS = [
        Binding("r", "run", "Run pipeline", show=True),
        Binding("a", "select_all", "Select all for this template", show=True),
    ]

    def __init__(self, selector: PipelineSelector):
        """Create pipeline output selector."""
        super().__init__()
        self.selector = selector

    @property
    def file_tree(
        self,
    ):
        """Input/output file structure."""
        return self.selector.file_tree

    @property
    def pipeline(
        self,
    ):
        """Set of pipeline recipes."""
        return self.selector.pipeline

    def compose(self) -> ComposeResult:
        """Create basic layout."""
        yield Header()
        self.template_renderer = TemplateRenderer(self.selector)
        yield Vertical(
            Horizontal(
                TemplateTreeControl(self.selector.partial_tree, self.template_renderer),
                self.template_renderer,
            ),
            Horizontal(
                Button("Back", name="back"),
                Button("Run pipeline", name="run"),
                Select(
                    [(e.name, e) for e in RunMethod], value=self.selector.run_method
                ),
                Checkbox(
                    "Overwrite dependencies", value=self.selector.overwrite_dependencies
                ),
                id="control-bar",
            ),
        )
        yield Footer()

    async def handle_template_select(self, message: TemplateSelect):
        """User has selected a template."""
        template = message.template
        self.app.sub_title = template.as_string
        await self.body.update(TemplateRenderer(template, self.file_tree))

    def on_button_pressed(self, event: Button.Pressed):
        """Continue to the next app."""
        if event.button.name == "back":
            self.exit(AllPanes.PLACEHOLDER)
        elif event.button.name == "run":
            self.action_run()

    def on_checkbox_changed(self, event: Checkbox.Changed):
        """Update overwrite dependencies."""
        self.selector.overwrite_dependencies = event.checkbox.value

    def on_select_changed(self, event: Select.Changed):
        """Update run method."""
        self.selector.run_method = event.select.value

    def action_run(
        self,
    ):
        """Run the pipeline."""
        self.exit(AllPanes.SUMMARY)

    def action_select_all(self):
        """Select all files matching this template."""
        self.template_renderer.select_all()


class TemplateTreeControl(Tree):
    """Sidebar containing all template definitions in FileTree."""

    current_node = None
    BINDINGS = [
        Binding("space", "toggle_node", "Collapse/Expand Node", show=True),
        Binding("up", "cursor_up", "Move Up", show=True),
        Binding("down", "cursor_down", "Move Down", show=True),
    ]

    def __init__(self, file_tree: FileTree, renderer, name: str = None):
        """
        Create a new template sidebar based on given FileTree.

        :param file_tree: FileTree to interact with
        :param renderer: Panel showing the files corresponding to selected template.
        :param name: name of the sidebar within textual.
        """
        self.file_tree = file_tree
        super().__init__("-", name=name)
        self.show_root = False
        self.find_children(self.root, self.file_tree.get_template(""))
        self.root.expand_all()
        self.renderer = renderer
        self.select_node(self.get_node_at_line(0))

    def on_mount(
        self,
    ):
        """Take focus on mount."""
        self.focus()

    def find_children(self, parent_node: TreeNode, template: Template):
        """
        Find all the children of a template and add them to the node.

        Calls itself recursively.
        """
        all_children = template.children(self.file_tree._templates.values())
        if len(all_children) == 0:
            parent_node.add_leaf(template.unique_part, template)
        else:
            this_node = parent_node.add(template.unique_part, template)
        children = set()
        for child in all_children:
            if child not in children:
                self.find_children(this_node, child)
                children.add(child)

    def render_label(self, node: TreeNode[Template], base_style, style):
        """Render line in tree."""
        if node.data is None:
            return node.label
        label = _render_node_helper(self.file_tree, node).copy()
        if node is self.cursor_node:
            label.stylize("reverse")
        if not node.is_expanded and len(node.children) > 0:
            label = Text("📁 ") + label
        return label

    def on_tree_node_highlighted(self):
        """Inform other panel if template is selected."""
        if self.current_node is not self.cursor_node:
            self.current_node = self.cursor_node
            self.renderer.render_template(self.current_node.data)


@lru_cache(None)
def _render_node_helper(tree: FileTree, node: TreeNode[Template]):
    meta = {
        "@click": f"click_label({node.id})",
        "tree_node": node.id,
        # "cursor": node.is_cursor,
    }
    paths = tree.get_mult(
        _get_template_key(tree, node.data), filter=True
    ).data.flatten()
    existing = [p for p in paths if p != ""]
    color = "blue" if len(existing) == len(paths) else "yellow"
    if len(existing) == 0:
        color = "red"
    counter = f" [{color}][{len(existing)}/{len(paths)}][/{color}]"
    res = Text.from_markup(
        node.data.rich_line(tree._templates) + counter, overflow="ellipsis"
    )
    res.apply_meta(meta)
    return res


def _get_template_key(tree, template):
    """Get key representing template with file-tree."""
    keys = {k for k, t in tree._templates.items() if t is template}
    return next(iter(keys))


class TemplateRenderer(DataTable):
    """
    Helper class to create a Rich rendering of a template.

    There are two parts:

        - a text file with the template
        - a table with the possible placeholder value combinations
          (shaded red for non-existing files)
    """

    def __init__(self, selector: PipelineSelector):
        """Create new renderer for template."""
        super().__init__()
        self.selector = selector
        self.cursor_type = "row"

    @property
    def file_tree(
        self,
    ):
        """Input/output file structure."""
        return self.selector.file_tree

    def on_mount(self):
        """Render upper-level template on mount."""
        self.render_template(self.file_tree.get_template(""))

    def render_template(self, template: Template):
        """Render the template as rich text."""
        self.current_template = template
        self.clear(columns=True)
        xr = self.file_tree.get_mult(
            _get_template_key(self.file_tree, template), filter=False
        )
        coords = sorted(xr.coords.keys())
        self.add_column("", key="checkboxes")
        self.add_columns("", *coords, "filename")
        for values in itertools.product(*[xr.coords[c].data for c in coords]):
            path = xr.sel(**{c: v for c, v in zip(coords, values)}).item()
            style = Style(bgcolor="blue" if op.exists(path) else None)
            self.add_row(
                self.get_checkbox(path),
                *[Text(v, style=style) for v in values],
                Text(path, style=style),
                key=path,
            )

    def on_data_table_row_selected(self, message: DataTable.RowSelected):
        """Add or remove selected row from pipeline run."""
        self.toggle_checkbox(message.row_key)

    def select_all(
        self,
    ):
        """Add or remove selected row from pipeline run."""
        for row in self.rows:
            self.toggle_checkbox(row, True)

    def toggle_checkbox(self, row_key, new_value=None):
        """Toggles the checkbox in given row."""
        current_checkbox = self.get_cell(row_key, "checkboxes")
        if current_checkbox == "☑" and new_value is not True:
            self.selector.remove_selected_file(row_key.value)
            self.update_cell(row_key, "checkboxes", self.get_checkbox(row_key.value))
        elif current_checkbox in "☐⊡" and new_value is not False:
            self.selector.add_selected_file(row_key.value)
            self.update_cell(row_key, "checkboxes", "☑")

    def get_checkbox(self, filename):
        """Return checkbox corresponding to filename."""
        if filename in self.selector.selected_files:
            return "☑"
        target = self.selector.get_file_targets(filename)
        if target.producer is None:
            return ""
        elif target.producer in self.selector.all_jobs[1]:
            return "⊡"
        elif target.producer.expected():
            return "☐"
        else:
            return "M"
