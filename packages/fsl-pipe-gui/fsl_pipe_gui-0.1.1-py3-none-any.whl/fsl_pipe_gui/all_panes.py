"""Defines enumeration of all available panes for user to select the next one."""
from enum import Enum

from file_tree import FileTree
from fsl_pipe import Pipeline
from fsl_pipe.job import FileTarget, JobList, RunMethod, get_target


class AllPanes(Enum):
    """
    Enumeration of all the possible GUI panes.

    Panes should return one of these to indicate what the next pane will be.
    If None is returned by a pane instead, the application will quit.
    """

    PLACEHOLDER = 1
    SELECTOR = 2
    SUMMARY = 3
    RUN = 4


class PipelineSelector:
    """
    Define which parts of the pipeline will be run.

    This information will be updated by each pane in the pipeline.
    """

    def __init__(
        self,
        pipeline: Pipeline,
        file_tree: FileTree,
        overwrite_dependencies=False,
        run_method=None,
    ):
        """Create new pipeline selector to be edited in GUI."""
        self.file_tree = file_tree
        all_templates = file_tree.template_keys()
        templates = {
            elem
            for piped_function in pipeline.scripts
            for elem in set.union(
                piped_function.filter_templates(False, all_templates),
                piped_function.filter_templates(True, all_templates),
            )
        }
        self.partial_tree = file_tree.filter_templates(templates)
        self.pipeline = pipeline
        self.full_job_list = self.pipeline.generate_jobs(self.file_tree)
        self.selected_files = set()
        self.all_jobs = ([], set())

        self._overwrite_dependencies = overwrite_dependencies
        if run_method is None:
            run_method = RunMethod.default()
        self.run_method = run_method

    @property
    def overwrite_dependencies(
        self,
    ):
        """Whether to override any already existing dependencies."""
        return self._overwrite_dependencies

    @overwrite_dependencies.setter
    def overwrite_dependencies(self, value):
        """Ensure jobs are reset when overwrite_dependencies is updated."""
        self._overwrite_dependencies = value
        self.reset_all_jobs()

    def get_file_targets(self, path) -> FileTarget:
        """Return file target corresponding to path."""
        return get_target(path, self.full_job_list.targets)

    def update_placeholders(self, **new_placeholders):
        """Update full job list for if placeholder values got changed."""
        self.file_tree.placeholders.update(**new_placeholders)
        self.partial_tree.placeholders.update(**new_placeholders)
        self.full_job_list = self.pipeline.generate_jobs(self.file_tree)
        self.reset_all_jobs()

    def add_selected_file(self, file):
        """Add a specific file to the list to be produced."""
        self.selected_files.add(file)
        target = self.get_file_targets(file)
        target.producer.add_to_jobs(
            self.all_jobs,
            overwrite=True,
            overwrite_dependencies=self.overwrite_dependencies,
        )

    def remove_selected_file(self, file):
        """Add a specific file to the list to be produced."""
        self.selected_files.remove(file)
        self.reset_all_jobs()

    def reset_all_jobs(
        self,
    ):
        """Force a recalculation of all_jobs."""
        self.all_jobs = ([], set())
        for file in self.selected_files:
            if (
                self.get_file_targets(file).producer is not None
                and self.get_file_targets(file).producer.expected()
            ):
                self.add_selected_file(file)

    @property
    def job_list(
        self,
    ) -> JobList:
        """Collection of jobs that will be run."""
        return JobList(self.file_tree, self.all_jobs[0], self.full_job_list.targets)

    def run(self):
        """Run the pipeline."""
        return self.job_list.run(self.run_method)
