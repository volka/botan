#!/usr/bin/env python3

"""
Unittests for Botan Python scripts.

Requires Python 3.

(C) 2017 Simon Warta (Kullo GmbH)

Botan is released under the Simplified BSD License (see license.txt)
"""

import sys
import unittest

sys.path.append("../..") # Botan repo root
from configure import ModulesChooser # pylint: disable=wrong-import-position


class ModulesChooserResolveDependencies(unittest.TestCase):
    def test_base(self):
        available_modules = set(["A", "B"])
        table = {
            "A": [],
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A"]))

    def test_no_dependencies_defined(self):
        available_modules = set(["A", "B"])
        table = {
            "A": [],
        }
        with self.assertRaises(KeyError):
            ModulesChooser.resolve_dependencies(available_modules, table, "B")

        available_modules = set(["A", "B"])
        table = {
            "A": ["B"],
        }
        with self.assertRaises(KeyError):
            ModulesChooser.resolve_dependencies(available_modules, table, "A")

    def test_add_dependency(self):
        available_modules = set(["A", "B"])
        table = {
            "A": ["B"],
            "B": []
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A", "B"]))

    def test_add_dependencies_two_levels(self):
        available_modules = set(["A", "B", "C"])
        table = {
            "A": ["B"],
            "B": ["C"],
            "C": []
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A", "B", "C"]))

    def test_circular(self):
        available_modules = set(["A", "B", "C"])
        table = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A", "B", "C"]))

    def test_not_available(self):
        available_modules = set(["A", "C"])
        table = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }
        ok, _ = ModulesChooser.resolve_dependencies(available_modules, table, "B")
        self.assertFalse(ok)

    def test_dependency_not_available(self):
        available_modules = set(["A", "C"])
        table = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }
        ok, _ = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertFalse(ok)

    def test_dependency2_not_available(self):
        available_modules = set(["A", "B"])
        table = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }
        ok, _ = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertFalse(ok)

    def test_dependency_choices(self):
        available_modules = set(["A", "B", "C"])
        table = {
            "A": ["B|C"],
            "B": [],
            "C": []
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertTrue(modules == set(["A", "B"]) or modules == set(["A", "C"]))

    def test_dependency_prefer_existing(self):
        available_modules = set(["A", "B", "C"])
        table = {
            "A": ["C", "B|C"],
            "B": [],
            "C": []
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A", "C"]))

    def test_dependency_prefer_existing2(self):
        available_modules = set(["A", "B", "C"])
        table = {
            "A": ["B", "B|C"],
            "B": [],
            "C": []
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A", "B"]))

    def test_dependency_choices_impossible(self):
        available_modules = set(["A", "C"])
        table = {
            "A": ["B|C"],
            "B": [],
            "C": []
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A", "C"]))

    def test_dependency_choices_impossible2(self):
        available_modules = set(["A", "B"])
        table = {
            "A": ["B|C"],
            "B": [],
            "C": []
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "A")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["A", "B"]))

    def test_deep(self):
        available_modules = set(["A", "B", "C", "E", "G"])
        table = {
            "A": ["B|C"],
            "B": ["D"],
            "C": ["E"],
            "D": [],
            "E": ["F|G"],
            "F": ["A", "B"],
            "G": ["A", "G"]
        }
        ok, modules = ModulesChooser.resolve_dependencies(available_modules, table, "G")
        self.assertTrue(ok)
        self.assertEqual(modules, set(["G", "A", "C", "E"]))


if __name__ == '__main__':
    unittest.TestCase.longMessage = True
    unittest.main()
