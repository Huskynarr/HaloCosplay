"""Verify that complete workshop exports preserve provenance and stay unapproved."""
import csv
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from tools import suit_assets, suit_engineering, suit_project, suit_thermal

ROOT = Path(__file__).resolve().parents[2]


class ProjectPackageTests(unittest.TestCase):
    def test_complete_package_and_non_destructive_reexport(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'Workshop with spaces'
            profile = ROOT / 'Design/Parametric/Profiles/Demo.json'
            suit_project.generate(profile, out, concept=True)
            raw = (out / 'profile.local.json').read_bytes()
            self.assertEqual(raw, profile.read_bytes())
            package = json.loads((out / 'Package.json').read_text())
            self.assertEqual(package['profile_sha256'], hashlib.sha256(raw).hexdigest())
            self.assertFalse(package['fabrication_approved'])
            reference = json.loads((out / 'Reference.json').read_text())
            with (out / 'Parts.csv').open(newline='') as f:
                parts = list(csv.DictReader(f))
            self.assertEqual({p['part_id'] for p in parts}, {p['id'] for p in reference['parts']})
            self.assertEqual(len(parts), 23)
            self.assertTrue(all(p['status'] == 'open' and not p['measured_mass_g'] for p in parts))
            readiness = json.loads((out / 'readiness.local.json').read_text())
            self.assertEqual(readiness['profile_binding']['sha256'], package['profile_sha256'])
            self.assertTrue(all(g['status'] == 'open' for g in readiness['gates']))
            engineering = json.loads((out / 'Engineering/EngineeringReport.json').read_text())
            self.assertFalse(engineering['hardware_approved'])
            with redirect_stdout(io.StringIO()):
                self.assertEqual(suit_engineering.main(['--input', str(out / 'engineering.local.json'),
                                                       '--out', str(out / 'Engineering'), '--check']), 0)
            self.assertTrue((out / 'Components/ComponentKit.scad').is_file())
            self.assertTrue((out / 'Hardware/CAD/HardwareKit.scad').is_file())
            hardware = json.loads((out / 'Hardware/HardwarePackage.json').read_text())
            self.assertFalse(hardware['hardware_approved'])
            self.assertEqual(hardware['geometry_check'], 'not_run')
            self.assertTrue((out / 'Fit/MjolnirEntry.scad').is_file())
            self.assertTrue((out / 'Clamshell/LimbClamshell.scad').is_file())
            self.assertTrue((out / 'Integration.md').is_file())
            integration = json.loads((out / 'Integration.json').read_text())
            self.assertEqual(integration['profile_sha256'], package['profile_sha256'])
            self.assertEqual(integration['configuration_sha256'], hashlib.sha256((out / 'integration.local.json').read_bytes()).hexdigest())
            suit_thermal.export(out / 'thermal.local.json', out / 'Thermal', check=True)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(suit_assets.main(['--manifest', str(out / 'assets.local.json'),
                                                  '--report', str(out / 'AssetReport.json')]), 2)
            with self.assertRaises(FileExistsError):
                suit_project.generate(profile, out, concept=True)
            self.assertEqual(raw, (out / 'profile.local.json').read_bytes())
            self.assertFalse((out / 'BUILD_INCOMPLETE.md').exists())

    def test_missing_measurements_do_not_create_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'No guessed measurements'
            with self.assertRaises(ValueError):
                suit_project.generate(ROOT / 'Design/Parametric/Profiles/Template.json', out)
            self.assertFalse(out.exists())

    def test_fog_selection_adds_only_selected_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = json.loads((ROOT / 'Design/Parametric/Profiles/Demo.json').read_text())
            profile['build']['fog_system'] = 'pmi-cloud'
            path = root / 'profile.json'
            path.write_text(json.dumps(profile))
            suit_project.generate(path, root / 'Fog', concept=True)
            bom = json.loads((root / 'Fog/BOM.local.json').read_text())
            ids = [p['id'] for p in bom['items']]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(len([key for key in ids if key.startswith('FOG')]), 6)


if __name__ == '__main__':
    unittest.main()
