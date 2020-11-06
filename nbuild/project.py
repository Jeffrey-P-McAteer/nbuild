
import os

from nbuild.deliverable import Deliverable
from nbuild.build import BuildSystem
from nbuild.test import TestSystem

class Project:
    def __init__(
        self,
        name="Unnamed Project",
        deliverables_in=None,
        build_system=None,
        deliverables_out=None,
        test_system=None,
    ):
        self.name = name
        
        if not isinstance(deliverables_in, (Deliverable)):
            raise Exception("deliverables_in must be a Deliverable")
        self.deliverables_in = deliverables_in

        if not isinstance(build_system, (BuildSystem)):
            raise Exception("build_system must be a BuildSystem")
        self.build_system = build_system
        self.build_system.project = self

        if deliverables_out is None:
            deliverables_out = self.deliverables_in
        if not isinstance(deliverables_out, (Deliverable)):
            raise Exception("deliverables_out must be a Deliverable")
        self.deliverables_out = deliverables_out

        if not isinstance(test_system, (TestSystem)):
            raise Exception("test_system must be a TestSystem")
        self.test_system = test_system
        self.test_system.project = self
      

    def build(self):
        self.build_system.build(self)

    def test(self):
        self.test_system.test(self)
    
    def write_reports_to(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.test_system.write_reports_to(self, directory)

    def open_reports(self):
        self.test_system.open_reports()

    # Utilities for build + test systems to use,
    # answers common questions about projects.

    def get_cwd(self):
        return self.deliverables_in.get_cwd()

