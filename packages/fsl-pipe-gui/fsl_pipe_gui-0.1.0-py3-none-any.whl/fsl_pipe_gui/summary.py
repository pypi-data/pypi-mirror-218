"""Displays summary of what will be run using Rich."""
from rich import print
from rich.columns import Columns
from rich.prompt import Confirm

from .all_panes import AllPanes, PipelineSelector


def show_summary(selector: PipelineSelector):
    """
    Display summary of what will be run using Rich.

    Will ask confirmation of whether to continue.
    """
    if len(selector.all_jobs[0]) == 0:
        if len(selector.selected_files) == 0:
            print("No output files were selected, so the pipeline cannot be run.\n")
        else:
            print("All output files for selected templates already exists.\n")
        if Confirm.ask(
            "Do you want to return to the selector pane to select output files?"
        ):
            return AllPanes.SELECTOR
        return None

    print("[b]Selected output files[/b]")
    print(Columns(sorted(selector.selected_files)))

    print("")
    print("[b]Pipeline report[/b]")
    selector.job_list.report()

    print("")
    print("[b]Jobs[/b]")
    print(Columns(sorted([str(job) for job in selector.all_jobs[0]])))
    if Confirm.ask("Do you want to run this pipeline?"):
        return AllPanes.RUN
    return AllPanes.SELECTOR
