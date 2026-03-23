from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import run_pipeline


class PipelineTest(unittest.TestCase):
    def test_pipeline_generates_requests_and_matches(self):
        summary = run_pipeline()
        self.assertGreaterEqual(summary["request_documents"], 3)
        self.assertGreaterEqual(summary["reference_documents"], 4)
        self.assertGreater(summary["requests_extracted"], 0)
        self.assertGreater(summary["reference_matches"], 0)


if __name__ == "__main__":
    unittest.main()

