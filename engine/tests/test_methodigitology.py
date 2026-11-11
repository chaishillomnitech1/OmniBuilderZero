import json
import unittest
from pathlib import Path
from methodigitology import validate


def valid_record():
    return {
        "languageVersion":"1.0.0-draft",
        "source":{"expression":"PRESERVE THE ORIGINAL","origin":"human","preserveVerbatim":True},
        "intention":"Preserve the source artifact",
        "purpose":{"statement":"Protect provenance","beneficiary":"archive users","harmBoundary":"Do not mutate originals"},
        "conviction":{"level":"HIGH","statement":"Strong commitment"},
        "impact":{"class":"DRAFT","rationale":"Blueprint only"},
        "constraints":["No writes to production"],
        "execution":{"mode":"BLUEPRINT"}
    }


class MethodigitologyValidationTests(unittest.TestCase):
    def test_machine_readable_artifacts_are_valid_json(self):
        root = Path(__file__).resolve().parents[2]
        for relative in ("methodigitology/ontology.jsonld", "methodigitology/lexicon.json", "methodigitology/intent.schema.json"):
            with self.subTest(artifact=relative):
                json.loads((root / relative).read_text(encoding="utf-8"))

    def test_valid_blueprint_record(self):
        self.assertEqual(validate(valid_record()), [])

    def test_conviction_does_not_authorize_execution(self):
        record = valid_record()
        record["conviction"]["level"] = "DECLARED"
        record["execution"]["mode"] = "EXECUTE"
        self.assertIn("EXECUTE requires a separate GRANTED authorization record", validate(record))

    def test_production_requires_authorization(self):
        record = valid_record()
        record["impact"]["class"] = "PRODUCTION"
        self.assertIn("PRODUCTION impact requires a separate GRANTED authorization record", validate(record))

    def test_verbatim_source_is_required(self):
        record = valid_record()
        record["source"]["preserveVerbatim"] = False
        self.assertIn("source.preserveVerbatim must be true", validate(record))

    def test_four_fields_are_distinct_and_required(self):
        record = valid_record()
        del record["purpose"]
        self.assertTrue(any("purpose" in error for error in validate(record)))


if __name__ == "__main__":
    unittest.main()
