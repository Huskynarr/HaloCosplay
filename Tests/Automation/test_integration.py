"""Equipment selection must produce complete, separate and unapproved plans."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tools import suit_engineering, suit_fit, suit_integration, suit_project, suit_thermal

ROOT = Path(__file__).resolve().parents[2]


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ROOT / 'Design/Parametric/Profiles/Demo.json').read_text())

    def test_highpower_without_fog_includes_control_rail_and_open_thermal_inputs(self):
        fit = suit_fit.derive(self.profile, True)
        plan = suit_integration.plan(fit, suit_integration.configure(fit))
        electrical = suit_integration.engineering_inputs(plan)
        rails = {r['id']: r for r in electrical['rails']}
        self.assertEqual(rails['EFFECT_15V']['voltage_v'], 15)
        self.assertEqual(rails['EFFECT_5V']['voltage_v'], 5)
        self.assertEqual(rails['EFFECT_15V']['battery_id'], rails['EFFECT_5V']['battery_id'])
        self.assertNotEqual(rails['COMFORT_5V']['battery_id'], rails['EFFECT_5V']['battery_id'])
        self.assertIn('EFFECT_CONTROL', {c['id'] for c in rails['EFFECT_5V']['consumers']})
        report = suit_engineering.calculate(electrical)
        self.assertIsNone(report['estimated_system_runtime_h'])
        self.assertFalse(report['hardware_approved'])
        thermal = suit_integration.thermal_inputs(plan)
        self.assertEqual(len(thermal['modules']), 2)
        self.assertTrue(all(len(m['junction_paths']) == 3 and m['heat_load_w'] is None for m in thermal['modules']))
        self.assertFalse(suit_thermal.calculate(thermal)['hardware_approved'])

    def test_optional_systems_have_hosts_and_fog_keeps_oem_supply(self):
        self.profile['build']['features'].update(hud=True, audio=True)
        self.profile['build']['fog_system'] = 'pmi-cloud'
        fit = suit_fit.derive(self.profile, True)
        cfg = suit_integration.configure(fit); cfg['camera'] = 'usb-uvc'
        plan = suit_integration.plan(fit, cfg)
        mounts = {m['id']: m for m in plan['mounts']}
        for ident in ('HUD', 'HUD_HOST', 'CAMERA', 'RECORDER', 'MIC', 'AUDIO', 'FOG', 'NOZZLE_FANS'):
            self.assertIn(ident, mounts)
        self.assertEqual(mounts['FOG']['circuit'], 'FOG_OEM')
        self.assertEqual(mounts['NOZZLE_FANS']['circuit'], 'EFFECT_5V')
        self.assertTrue(all(m['measured_mass_g'] is None and not m['installed_and_tested'] for m in mounts.values()))
        self.assertFalse(plan['solo_donning_verified'])
        self.assertEqual(len(suit_integration.thermal_inputs(plan)['modules']), 4)

    def test_passive_plan_has_no_invented_consumers(self):
        self.profile['build']['features'].update(lighting=False, hud=False, audio=False)
        fit = suit_fit.derive(self.profile, True)
        cfg = suit_integration.configure(fit)
        cfg.update(helmet_ventilation='passive', torso_ventilation='passive')
        plan = suit_integration.plan(fit, cfg)
        self.assertEqual(plan['mounts'], [])
        electrical = suit_integration.engineering_inputs(plan)
        self.assertEqual(electrical['rails'], [])
        self.assertIsNone(suit_engineering.calculate(electrical)['estimated_system_runtime_h'])
        thermal = suit_integration.thermal_inputs(plan)
        self.assertEqual(thermal['modules'], [])
        self.assertEqual(thermal['vents'], [])

    def test_invalid_selection_fails_before_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = root / 'profile.json'
            profile.write_text(json.dumps(self.profile))
            cfg = root / 'options.json'
            for data in ({'hud': 'combiner'}, {'camera': 'magic'}, {'unknown': True}, []):
                cfg.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    suit_project.generate(profile, root / 'out', True, cfg)
                self.assertFalse((root / 'out').exists())
            with self.assertRaises(ValueError):
                suit_project.generate(profile, root / 'out')
            self.assertFalse((root / 'out').exists())


if __name__ == '__main__':
    unittest.main()
