"""Accessory exports preserve inputs and distinguish source from mesh checks."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from tools import suit_hardware


class HardwarePackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_custom_dimensions_are_preserved_without_body_scaling(self):
        defaults, _ = suit_hardware.configuration()
        key = next(iter(defaults))
        config = self.root/'config.json'
        config.write_text(json.dumps({key: defaults[key]+1}))
        before = config.read_bytes()
        out = self.root/'revision with spaces'
        report = suit_hardware.export(out, config)
        self.assertEqual(report['parameters'][key], defaults[key]+1)
        self.assertEqual(report['parameter_origin'][key], 'explicit_config')
        self.assertEqual(config.read_bytes(), before)
        self.assertFalse(report['hardware_approved'])
        self.assertEqual(report['geometry_check'], 'not_run')
        self.assertTrue(all(p['mesh_check'] is None for p in report['parts']))
        self.assertTrue((out/'CAD/HardwareKit.scad').is_file())
        self.assertTrue((out/'Electrical/README.md').is_file())
        self.assertIn('CAD/Parameters.scad', report['outputs_sha256'])
        self.assertFalse((out/'CAD/GeometryCheck.json').exists())
        baseline = json.loads((out/'CAD/BaselineGeometryCheck.json').read_text())
        self.assertEqual(baseline['status'], 'BASELINE_ONLY_NOT_THIS_EXPORT')
        self.assertIn('gelten nicht', (out/'CAD/README.md').read_text())

    def test_bad_configuration_never_creates_output(self):
        defaults, _ = suit_hardware.configuration()
        key = next(iter(defaults))
        for value in ({'invented_key': 2}, {key: '1; cube(999);'},
                      {key: float('nan')}, {key: True}, {key: float('inf')}, []):
            with self.subTest(value=value):
                config = self.root/'input.json'; config.write_text(json.dumps(value))
                out = self.root/'invalid'
                with self.assertRaises(ValueError):
                    suit_hardware.export(out, config)
                self.assertFalse(out.exists())

    def test_existing_revision_and_source_tree_are_preserved(self):
        out = self.root/'existing'; out.mkdir()
        sentinel = out/'keep.json'; sentinel.write_text('do not touch')
        with self.assertRaises(ValueError):
            suit_hardware.export(out)
        self.assertEqual(sentinel.read_text(), 'do not touch')
        with self.assertRaises(ValueError):
            suit_hardware.export(suit_hardware.CAD_SOURCE/'DoNotCreate')
        link = self.root/'alias'; link.symlink_to(out, target_is_directory=True)
        with self.assertRaises(ValueError):
            suit_hardware.export(link)

    def test_missing_renderer_does_not_create_false_success(self):
        out = self.root/'no-renderer'
        with mock.patch.object(suit_hardware.shutil, 'which', return_value=None):
            with self.assertRaises(ValueError):
                suit_hardware.export(out, render_stl=True)
        self.assertFalse(out.exists())

    def test_failed_mesh_marks_package_incomplete(self):
        out = self.root/'failed-mesh'
        result = mock.Mock(returncode=0, stdout='', stderr='ERROR: geometric assertion')
        with mock.patch.object(suit_hardware.shutil, 'which', return_value='/fake/openscad'), \
                mock.patch.object(suit_hardware.subprocess, 'run', return_value=result):
            with self.assertRaises(ValueError):
                suit_hardware.export(out, render_stl=True)
        self.assertTrue((out/'BUILD_INCOMPLETE.md').is_file())
        self.assertFalse((out/'HardwarePackage.json').exists())


if __name__ == '__main__':
    unittest.main()
