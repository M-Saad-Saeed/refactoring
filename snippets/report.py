"""Generate sales reports with separate calculation, formatting, and delivery."""

import smtplib

SMTP_HOST = "smtp.brunel.ac.uk"
SMTP_PORT = 587
REPORT_SENDER = "reports@brunel.ac.uk"
REPORT_RECIPIENT = "boss@brunel.ac.uk"


def summarize_sales(sales):
    """Return the number of sales and their total in the original order."""
    total = 0
    for sale_amount in sales:
        total = total + sale_amount
    return len(sales), total


def format_sales_report(sales_count, total):
    """Render a sales summary as HTML without sending it."""
    return (
        "<html><body>"
        "<h1>Sales Report</h1>"
        f"<p>Number of sales: {sales_count!s}</p>"
        f"<p>Total: {total!s}</p>"
        "</body></html>"
    )


def send_sales_report(html):
    """Deliver report HTML using the configured SMTP server."""
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.sendmail(REPORT_SENDER, REPORT_RECIPIENT, html)
    server.quit()


# The compatibility coordinator intentionally exposes only generate().
class SalesReport:  # pylint: disable=too-few-public-methods
    """Coordinate sales reporting through the existing public interface."""

    def __init__(self, sales):
        self.sales = sales

    def generate(self):
        """Run the reporting workflow and return the delivered HTML."""
        sales_count, total = summarize_sales(self.sales)
        html = format_sales_report(sales_count, total)
        send_sales_report(html)
        return html


if __name__ == "__main__":
    SalesReport([120, 340, 90, 560]).generate()
