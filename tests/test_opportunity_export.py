import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('export_opportunities',ROOT/'scripts/export_opportunities.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class ExportTests(unittest.TestCase):
    def test_historical_age_and_stable_identity_not_export_time(self):
        path=ROOT/'ideas/2026/W40/candidates-3.md'
        a=mod.export(path,ROOT);b=mod.export(path,ROOT)
        self.assertEqual(a,b);self.assertEqual(len(a),3)
        self.assertTrue(a[0]['origin']['observed_at'].startswith('2026-10-02'))
        self.assertEqual(a[0]['origin']['classification'],'hypothesis')
        self.assertEqual(a[0]['evidence'],[]);self.assertEqual(a[0]['build']['acceptance'],[])
    def test_source_outside_repo_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):mod.export(Path(d)/'x.md',ROOT)
    def test_missing_timestamp_does_not_claim_freshness(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.md';p.write_text('## 1. idea\n')
            with self.assertRaises(ValueError):mod.export(p,Path(d))
    def test_contract_copies_are_identical(self):
        own=(ROOT/'contracts/opportunity-v1.schema.json').read_bytes()
        for repo in ['pain-collector','signal-lab']:
            other=ROOT.parent/repo/'contracts/opportunity-v1.schema.json'
            if other.exists():self.assertEqual(own,other.read_bytes())
        self.assertEqual(json.loads(own)['properties']['schema_version']['const'],1)

if __name__=='__main__':unittest.main()
