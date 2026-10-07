"""
SNIPPET 1 — Single Responsibility Principle (SRP)

Smell: this ONE class gathers data, formats it as HTML, AND emails it.
Three reasons to change = three responsibilities crammed together.

Your job (via the AI harness):
  Split into focused pieces so that changing the email provider does NOT
  force you to touch the formatting or the data-gathering code.
"""

import smtplib


class SalesReport:
    def __init__(self, sales):
        self.sales = sales

    def generate(self):
        # data + formatting + delivery all tangled together
        total = 0
        for s in self.sales:
            total = total + s
        html = "<html><body>"
        html += "<h1>Sales Report</h1>"
        html += "<p>Number of sales: " + str(len(self.sales)) + "</p>"
        html += "<p>Total: " + str(total) + "</p>"
        html += "</body></html>"

        server = smtplib.SMTP("smtp.brunel.ac.uk", 587)
        server.sendmail("reports@brunel.ac.uk", "boss@brunel.ac.uk", html)
        server.quit()
        return html


if __name__ == "__main__":
    SalesReport([120, 340, 90, 560]).generate()
