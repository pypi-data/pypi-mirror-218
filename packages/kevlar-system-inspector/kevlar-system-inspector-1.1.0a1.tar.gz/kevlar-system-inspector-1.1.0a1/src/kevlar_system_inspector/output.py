"""
Output of reports in various formats, as pytest plugins
"""

import csv
from dataclasses import dataclass
import os
from types import ModuleType, FunctionType
from typing import Dict, Set, List, cast
from collections import defaultdict
import xml.etree.ElementTree as ET

import docutils.core
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from . import templates
from .report import TestReport
from .console import print_document

import pytest


class HtmlReporter:
    def __init__(self, filename: str):
        self.filename = filename

    def pytest_kevlar_report(self, report: TestReport) -> None:
        templates_dir = os.path.dirname(templates.__file__)
        template = os.path.join(templates_dir, "html5-template.txt")
        stylesheet = os.path.join(templates_dir, "starlab.css")

        with open(self.filename, "wb") as fp:
            fp.write(
                docutils.core.publish_from_doctree(
                    report.document,
                    self.filename,
                    writer_name="html5",
                    settings_overrides={
                        "stylesheet_path": stylesheet,
                        "template": template,
                    },
                )
            )

        console = Console()
        console.print(f"Printed detailed report (HTML) to '{self.filename}'")


class RstReporter:
    def __init__(self, filename: str):
        self.filename = filename

    def pytest_kevlar_report(self, report: TestReport) -> None:
        console = Console()
        with open(self.filename, "w") as fp:
            fp.write(report.document_source)
        console.print(
            f"Printed detailed report (reStructuredText) to '{self.filename}'"
        )


class ConsoleReporter:
    def pytest_kevlar_report(self, report: TestReport) -> None:
        print_document(report.document)


class TextReporter:
    def __init__(self, filename: str):
        self.filename = filename

    def pytest_kevlar_report(self, report: TestReport) -> None:
        with open(self.filename, "w") as fp:
            print_document(report.document, file=fp, width=80)
        console = Console()
        console.print(f"Printed detailed report (plain text) to '{self.filename}'")


class SummaryReporter:
    """
    Stuff that gets printed in lieu of the full report, when we write to a file.
    """

    def pytest_kevlar_report(self, report: TestReport) -> None:
        print_document(report.summary)
        print()


@dataclass
class TestItem:
    title: str
    references: Set[str]
    full_version_only: bool


@dataclass
class TestCategory:
    title: str
    items: List[TestItem]


class TestListerBase:
    def pytest_collection_finish(self, session: pytest.Session) -> None:
        # So that we don't have to tag all our tests with additional metadata,
        # we will create a report document with all tests, and then parse the
        # document structure for the info we need.  Any metadata that we do
        # need to tag can be inserted into the documentation along with
        # everything else.

        report = TestReport()

        by_module: Dict[ModuleType, Dict[FunctionType, int]] = defaultdict(dict)
        for item in session.items:
            # Deduplicate paramatrized tests. We use a dictionary like a set
            # because sets don't preseve insertion order.
            by_module[item.module][item.function] = 1  # type: ignore
            report.add_item(cast(pytest.Function, item))
        report.finish()
        root = ET.fromstring(report.document.asdom().toxml())

        listing = []
        for category in root.iterfind(".//section[@classes]"):
            if "test-category" not in category.attrib["classes"].split():
                continue

            items = []

            for test_item in category.iterfind("section[@classes]"):
                classes = test_item.attrib.get("classes", "").split()

                if "test-item" not in classes:
                    continue

                refs = set()
                for meta in test_item.iterfind(".//meta[@name='kevlar-code']"):
                    refs.add(meta.attrib["content"])

                # Note: rst -> xml translation mangles class names, and
                # underscores become dashes.
                full = "full-version-only" in classes

                items.append(
                    TestItem(
                        title=self.get_title(test_item),
                        references=refs,
                        full_version_only=full,
                    )
                )

            listing.append(TestCategory(title=self.get_title(category), items=items))
        self.print_output(listing)

    def print_output(self, listing: List[TestCategory]) -> None:
        raise NotImplementedError

    @staticmethod
    def get_title(node: ET.Element) -> str:
        title = node.find("title")
        if title is None:
            return "<undocumented>"
        return "".join(title.itertext())


class ConsoleTestLister(TestListerBase):
    def print_output(self, listing: List[TestCategory]) -> None:
        console = Console()
        grid = Table.grid()
        grid.add_column()
        grid.add_row(
            Panel(
                Text(
                    "Tests Included with Kevlar System Inspector",
                    justify="center",
                    style="bold",
                )
            )
        )
        grid.add_row("")

        for category in listing:
            table = Table(title=category.title)
            table.add_column("Title")
            table.add_column("References")
            table.add_column("Full Version")

            for test_item in category.items:
                table.add_row(
                    test_item.title,
                    " ".join(sorted(test_item.references)),
                    "*" if test_item.full_version_only else "",
                )
            grid.add_row(table)
        console.print(grid)


class CsvTestLister(TestListerBase):
    def __init__(self, filename: str):
        self.filename = filename

    def print_output(self, listing: List[TestCategory]) -> None:
        with open(self.filename, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Category", "References", "Full Version"])

            for category in listing:
                for test_item in category.items:
                    references = " ".join(sorted(test_item.references))
                    full = "*" if test_item.full_version_only else ""
                    writer.writerow([test_item.title, category.title, references, full])
        console = Console()
        console.print(f"Printed CSV listing to '{self.filename}'")
