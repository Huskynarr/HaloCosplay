"""Catalog source integrity and regression checks for generated deliverables."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('suit_catalog', ROOT / 'tools/suit_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)

class ProductCatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'Materials/ProductCatalog.json').read_text())

    def test_generated_files_match_and_all_sources_validate(self):
        catalog.validate(self.data)
        for path, content in catalog.outputs(self.data).items():
            self.assertEqual(path.read_text(), content)

    def test_duplicate_and_missing_references_rejected(self):
        self.data['products'].append(copy.deepcopy(self.data['products'][0]))
        with self.assertRaises(ValueError): catalog.validate(self.data)
        self.data['products'].pop()
        self.data['products'][0]['guides'] = ['../not-a-guide.md']
        with self.assertRaises(ValueError): catalog.validate(self.data)

    def test_unknown_prices_not_silently_replaced_with_zero(self):
        self.data['products'][0]['price_eur'] = 0
        with self.assertRaises(ValueError): catalog.validate(self.data)

    def test_amazon_search_not_promoted_to_unverified_direct_offer(self):
        link = next(l for p in self.data['products'] for l in p['links'] if l['affiliate'])
        link['url'] = 'https://www.amazon.de/dp/B012345678?tag=huskynarr-21'
        with self.assertRaises(ValueError): catalog.validate(self.data)

    def test_source_dates_and_affiliate_host_checked(self):
        link = next(l for p in self.data['products'] for l in p['links'] if l['affiliate'])
        link['url'] = link['url'].replace('amazon.de', 'amazon.de.example.org')
        with self.assertRaises(ValueError): catalog.validate(self.data)

    def test_all_body_parts_and_major_technical_domains_covered(self):
        self.assertEqual(set().union(*(set(p['parts']) for p in self.data['products'])), catalog.PARTS)
        self.assertEqual({p['category'] for p in self.data['products']}, {c['id'] for c in self.data['categories']})
        self.assertNotIn('amazon.de/dp/', (ROOT / 'web/app.js').read_text())

if __name__ == '__main__':
    unittest.main()
