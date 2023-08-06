"""Main module containing the actual code to run the GUI."""
from file_tree import FileTree
from fsl_pipe import Pipeline
from rich import print

from .all_panes import AllPanes, PipelineSelector
from .placeholder_tab import PlaceholderEditor
from .selector_tab import OutputSelector
from .summary import show_summary


def run_gui(pipeline: Pipeline, tree: FileTree, **kwargs):
    """
    Run terminal-based GUI, so the user can select which output files to produce.

    Returns True if a pipeline actually ran. False if the user exited before running a pipeline.

    :param pipeline: Collection of recipes contained in an `fsl-pipe` Pipeline object.
    :param tree: Description of the directory structure containing the input and output files.
    """
    selector = PipelineSelector(pipeline, tree, **kwargs)
    current = AllPanes.PLACEHOLDER if len(tree.placeholders) > 0 else AllPanes.SELECTOR

    while True:
        if current is None:
            print("Exiting FSL pipeline output selector")
            return False
        elif current == AllPanes.PLACEHOLDER:
            current = PlaceholderEditor(selector).run()
        elif current == AllPanes.SELECTOR:
            current = OutputSelector(selector).run()
        elif current == AllPanes.SUMMARY:
            current = show_summary(selector)
        elif current == AllPanes.RUN:
            selector.run()
            return True
        else:
            raise ValueError(
                f"Unexpected error: next pane is set to unknown value: {current}"
            )
