"""Regression tests for sales reporting without sending real emails."""

import unittest
from unittest.mock import call, patch

from snippets.report import SalesReport, format_sales_report, summarize_sales


class SalesReportTests(unittest.TestCase):
    """Check report contents, calculation order, and delivery behaviour."""

    def test_summary_handles_empty_and_populated_sales(self):
        """Summaries retain the sale count and numeric total."""
        for sales, expected in [([], (0, 0)), ([120, 340, 90, 560], (4, 1110))]:
            with self.subTest(sales=sales):
                self.assertEqual(summarize_sales(sales), expected)

    def test_summary_preserves_floating_point_addition_order(self):
        """Sequential addition preserves the original rounding behaviour."""
        self.assertEqual(summarize_sales([1e16, 1.0, -1e16]), (3, 0.0))

    @patch("snippets.report.smtplib.SMTP")
    def test_formatting_has_no_delivery_side_effect(self, smtp):
        """Rendering a summary produces the original HTML without emailing."""
        self.assertEqual(
            format_sales_report(2, 30),
            "<html><body><h1>Sales Report</h1>"
            "<p>Number of sales: 2</p><p>Total: 30</p></body></html>",
        )
        smtp.assert_not_called()

    @patch("snippets.report.smtplib.SMTP")
    def test_generate_returns_and_delivers_the_same_html(self, smtp):
        """The existing interface sends one report and closes SMTP in order."""
        expected_html = (
            "<html><body><h1>Sales Report</h1>"
            "<p>Number of sales: 4</p><p>Total: 1110</p></body></html>"
        )
        self.assertEqual(SalesReport([120, 340, 90, 560]).generate(), expected_html)
        self.assertEqual(
            smtp.mock_calls,
            [
                call("smtp.brunel.ac.uk", 587),
                call().sendmail("reports@brunel.ac.uk", "boss@brunel.ac.uk", expected_html),
                call().quit(),
            ],
        )

    @patch("snippets.report.smtplib.SMTP")
    def test_generate_propagates_delivery_failure(self, smtp):
        """A failed delivery remains visible to the caller."""
        smtp.return_value.sendmail.side_effect = OSError("Delivery failed")
        with self.assertRaisesRegex(OSError, "Delivery failed"):
            SalesReport([120]).generate()


if __name__ == "__main__":
    unittest.main()
