import copy
import datetime as dt
import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.suit_readiness import GATES, evaluate


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.report = self.root / 'test.md'
        self.report.write_text('Actual test observations for unit fixture')
        self.data = {'schema_version': 1, 'revision': 'test-r1', 'gates': [
            {'id': g, 'status': 'passed', 'reviewer': 'Test fixture', 'summary': 'Recorded observations',
             'revision': 'test-r1', 'date': dt.date.today().isoformat(),
             'evidence': [{'path': 'test.md', 'sha256': hashlib.sha256(self.report.read_bytes()).hexdigest()}]}
            for g in GATES]}

    def test_complete_evidence(self):
        self.assertTrue(evaluate(self.data, self.root)['scopes']['exhibition'])

    def test_open_gate_blocks_scope(self):
        self.data['gates'][0]['status'] = 'open'
        self.assertFalse(evaluate(self.data, self.root)['scopes']['wearable'])

    def test_modified_evidence_blocks(self):
        self.report.write_text('Changed after review')
        self.assertFalse(evaluate(self.data, self.root)['scopes']['exhibition'])

    def test_template_status_without_evidence_blocks(self):
        self.data['gates'][0]['evidence'] = []
        self.assertFalse(evaluate(self.data, self.root)['scopes']['wearable'])

    def test_revision_invalidates_all_reviews(self):
        self.data['revision'] = 'test-r2'
        self.assertFalse(any(g['complete'] for g in evaluate(self.data, self.root)['gates']))

    def test_paths_cannot_escape_root(self):
        for path in ('../outside.md', str(self.report)):
            data = copy.deepcopy(self.data)
            data['gates'][0]['evidence'][0]['path'] = path
            self.assertFalse(evaluate(data, self.root)['scopes']['wearable'])

    def test_missing_and_duplicate_gates_rejected(self):
        data = copy.deepcopy(self.data)
        data['gates'].pop()
        with self.assertRaises(ValueError):
            evaluate(data, self.root)
        self.data['gates'][-1] = self.data['gates'][0]
        with self.assertRaises(ValueError):
            evaluate(self.data, self.root)

    def test_event_gate_separate_from_wearable(self):
        self.data['gates'][-1]['status'] = 'open'
        result = evaluate(self.data, self.root)
        self.assertTrue(result['scopes']['wearable'])
        self.assertFalse(result['scopes']['exhibition'])

    def test_future_review_rejected(self):
        self.data['gates'][0]['date'] = '2999-01-01'
        self.assertFalse(evaluate(self.data, self.root)['scopes']['wearable'])
