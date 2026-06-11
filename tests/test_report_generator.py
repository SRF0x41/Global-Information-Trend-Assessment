import unittest
from analysis.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ReportGenerator()

    def test_generate_zeitgeist_report(self):
        # Create some sample trend data
        trends = [
            {
                "summary": "AI advancements in 2026",
                "sources": ["arxiv.org", "techcrunch.com"],
                "confidence": 0.95,
                "analysis": "Significant breakthroughs in natural language processing and computer vision have been observed this year..."
            },
            {
                "summary": "Quantum computing progress",
                "sources": ["nature.com", "quantum-magazine.org"],
                "confidence": 0.85,
                "analysis": "Several research teams have made notable progress in quantum error correction and qubit stability..."
            }
        ]

        # Generate report
        report = self.generator.generate_zeitgeist_report(trends)

        # Check that the report has the correct structure
        self.assertIn("# Global Information Trend Assessment\n\n", report)
        self.assertIn("## Trend 1: AI advancements in 2026\n", report)
        self.assertIn("**Sources**: arxiv.org, techcrunch.com\n", report)
        self.assertIn("**Confidence**: 0.95/1.0\n", report)