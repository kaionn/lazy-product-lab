import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('reconcile', Path(__file__).resolve().parents[1]/'scripts/slack-reconcile.py')
module=importlib.util.module_from_spec(spec)
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
spec.loader.exec_module(module)

class ReconcileTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.cwd=os.getcwd(); os.chdir(self.tmp.name); self.addCleanup(os.chdir,self.cwd)
        self.env=patch.dict(os.environ,{'GITHUB_REPOSITORY':'kaionn/lazy-product-lab','GITHUB_RUN_ATTEMPT':'1','SLACK_REPORT_CHANNEL_ID':module.CHANNEL,'SLACK_BOT_TOKEN':'FAKE'},clear=True)
        self.env.start(); self.addCleanup(self.env.stop)
        Path('.original-receipts').mkdir()
        Path('.original-receipts/result.json').write_text(json.dumps({'test_id':module.TEST_ID,'status':'needs_review'}))
        Path('.original-receipts/event.json').write_text(json.dumps({'parts':[module.PARENT],'status':'needs_reconciliation','key':'original'}))
        self.identity=patch.object(module.smoke,'identity',return_value={'status':'verified'}); self.identity.start(); self.addCleanup(self.identity.stop)

    def test_resume_posts_only_file_and_alert_then_checks_duplicates(self):
        with patch.object(module,'classified_api',side_effect=[{'file_id':'F1','upload_url':'https://files.slack.com/upload/test'}, {'ok':True}]) as api, patch.object(module,'request',return_value=b'OK'), patch.object(module,'mirror',side_effect=[{'status':'already_sent'},{'status':'sent'},{'status':'already_sent'}]) as mirror:
            self.assertEqual(module.main(),0)
            self.assertEqual([x.args[0] for x in api.call_args_list],['files.getUploadURLExternal','files.completeUploadExternal'])
            self.assertEqual(api.call_args_list[1].args[1]['thread_ts'], module.PARENT)
            self.assertEqual([x.args[1] for x in mirror.call_args_list],['reports','alerts','alerts'])
            self.assertEqual(json.loads(Path('.reconcile-state/original.json').read_text())['file_id'],'F1')

    def test_unknown_error_text_is_never_recorded(self):
        with patch.object(module,'classified_api',side_effect=RuntimeError('FAKE PRIVATE RESPONSE')):
            self.assertEqual(module.main(),1)
        text=Path('.reconcile-state/reconcile-result.json').read_text()
        self.assertNotIn('FAKE',text)
        self.assertEqual(json.loads(text)['stage'],'get_upload_url')

    def test_allocated_file_id_saved_before_uncertain_transfer(self):
        with patch.object(module,'classified_api',return_value={'file_id':'F1','upload_url':'https://files.slack.com/upload/test'}), patch.object(module,'request',side_effect=TimeoutError):
            self.assertEqual(module.main(),1)
        receipt=json.loads(Path('.reconcile-state/reconcile-result.json').read_text())
        self.assertEqual(receipt['file_id'],'F1'); self.assertEqual(receipt['stage'],'upload_bytes')
        with patch.object(module,'classified_api') as api:
            self.assertEqual(module.main(),1); api.assert_not_called()

    def test_rerun_and_wrong_parent_stop_before_api(self):
        Path('.original-receipts/event.json').write_text(json.dumps({'parts':['wrong'],'status':'needs_reconciliation','key':'original'}))
        with patch.object(module,'classified_api') as api:
            self.assertEqual(module.main(),1); api.assert_not_called()
        os.environ['GITHUB_RUN_ATTEMPT']='2'
        with patch.object(module,'classified_api') as api:
            self.assertEqual(module.main(),1); api.assert_not_called()

if __name__=='__main__': unittest.main()
