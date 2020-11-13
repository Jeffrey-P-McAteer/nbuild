
"""
The test module holds the Test class
"""


class Test:
    """
    Defines metadata for a test. The most important thing here is
    the "task" and "tests" parameters: task defined what needs to occur
    (physical inspection, run a specific function, etc.)
    and tests lets project authors make groups of tests.
    If any child test fails the parent test fails as well.
    """
    def __init__(self, name=None, description="", task=None, tests=None):
        if not name:
            raise Exception('Error: Test was not given a name!')
        if (not task) and (not tests):
            raise Exception('Error: Test was not given a task or sub-tests; either a task or a list of tests must be given.')
        if tests is None:
            tests = []
        self.name = name
        self.description = description
        self.task = task
        self.tests = tests
        # Data set by the project during initialization
        self.project = None
        # Data set during testing
        self.passed = False

    def set_project(self, project):
        """Save a reference to the project, which is used to communicate data across different tests should it be needed"""
        self.project = project
        if self.task:
            self.task.set_project(project)
        elif self.tests:
            for t in self.tests:
                t.set_project(project)

    def evaluate(self):
        """
        Run the task or all the child tests specified when this was constructed.
        Returns true if this test case passed.
        """
        if self.task:
            self.passed = self.task.evaluate()
        elif self.tests:
            all_passed = True
            for t in self.tests:
                p = t.evaluate()
                if not p:
                    all_passed = False
            # If even a single sub-test is wrong, the entire group is wrong
            self.passed = all_passed

        return self.passed


