import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('validate_evidence.py')
spec = importlib.util.spec_from_file_location('evidence_validator', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.source = {'turns': [
            dict(id='T1', participant_id='P1', speaker='participant', verbatim=True,
                 locator='one.txt:L1', text='我没换牌。\n只是买了小瓶🙂。'),
            dict(id='T2', participant_id='P2', speaker='participant', verbatim=True,
                 locator='two.txt:L4', text='这次因为缺货才换。'),
            dict(id='T3', participant_id='P1', speaker='interviewer', verbatim=True,
                 locator='one.txt:L2', text='是不是包装不好？')]}
        self.quote = dict(id='Q1', participant_id='P1', turn_id='T1', start=0, end=5, quote='我没换牌。')

    def payload(self, quotes=None):
        source = json.dumps(self.source, ensure_ascii=False).encode()
        ledger = {'source_sha256': hashlib.sha256(source).hexdigest(),
                  'quotes': [self.quote] if quotes is None else quotes}
        return source, ledger

    def result(self, quotes=None):
        source, ledger = self.payload(quotes)
        return module.validate(source, json.dumps(ledger, ensure_ascii=False).encode())

    def test_valid_chinese(self):
        self.assertEqual(self.result()['status'], 'matched')

    def test_multiline_emoji(self):
        text = self.source['turns'][0]['text']
        self.quote.update(quote=text, start=0, end=len(text))
        self.assertEqual(self.result()['status'], 'matched')

    def test_wrong_person_even_when_text_exists(self):
        self.quote.update(participant_id='P1', turn_id='T2', quote='这次因为缺货才换。', end=9)
        self.assertEqual(self.result()['status'], 'failed')

    def test_interviewer_is_not_consumer_evidence(self):
        self.quote.update(turn_id='T3', quote='是不是包装不好？', end=8)
        self.assertEqual(self.result()['status'], 'failed')

    def test_paraphrase_cannot_be_verbatim(self):
        self.source['turns'][0]['verbatim'] = False
        self.assertEqual(self.result()['status'], 'failed')

    def test_drop_negation(self):
        self.quote.update(quote='我换牌。')
        self.assertEqual(self.result()['status'], 'failed')

    def test_cross_turn_splice(self):
        self.quote.update(quote='我没换牌。这次因为缺货才换。', end=14)
        self.assertEqual(self.result()['status'], 'failed')

    def test_invalid_offset(self):
        self.quote['start'] = -1
        self.assertEqual(self.result()['status'], 'failed')

    def test_byte_offsets_for_chinese_rejected(self):
        self.quote['end'] = len(self.quote['quote'].encode('utf-8'))
        self.assertEqual(self.result()['status'], 'failed')

    def test_changed_source(self):
        source, ledger = self.payload()
        self.assertEqual(module.validate(source + b' ', json.dumps(ledger).encode())['status'], 'failed')

    def test_missing_turn(self):
        self.quote['turn_id'] = 'T404'
        self.assertEqual(self.result()['status'], 'failed')

    def test_duplicate_turn(self):
        self.source['turns'].append(copy.deepcopy(self.source['turns'][0]))
        with self.assertRaises(ValueError):
            self.result()

    def test_duplicate_quote(self):
        with self.assertRaises(ValueError):
            self.result([self.quote, copy.deepcopy(self.quote)])

    def test_empty_ledger(self):
        with self.assertRaises(ValueError):
            self.result([])

    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):
            module.validate(b'{"turns": [], "turns": []}', b'{}')

    def test_cli_exit_codes(self):
        root = Path(tempfile.mkdtemp(prefix='consumer-evidence-'))
        self.addCleanup(shutil.rmtree, root)
        source, ledger = self.payload()
        (root/'source.json').write_bytes(source)
        for expected in (0, 1, 2):
            if expected == 1:
                ledger['quotes'][0]['participant_id'] = 'P99'
            if expected == 2:
                ledger['quotes'] = []
            (root/'evidence.json').write_text(json.dumps(ledger))
            run = subprocess.run([sys.executable, str(SCRIPT), str(root/'source.json'), str(root/'evidence.json')],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, expected, run.stdout + run.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)

