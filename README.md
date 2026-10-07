# CS3616 Lab Week 2: Refactoring

This lab improves `snippets/checkout.py` and `snippets/report.py` through clean-code refactoring and the Single Responsibility Principle (SRP). The changes preserve the tested calculations, report output, and delivery workflow.

## Clean-code improvements

| Area | Checkout | Sales report |
| --- | --- | --- |
| Meaningful names | `unit_price`, `quantity`, `subtotal`, and `discount_rate` explain the calculations. | `sale_amount`, `sales_count`, and focused function names explain the reporting steps. |
| Named constants | Membership levels, discount rates, loyalty threshold, and loyalty discount are named constants. | SMTP host, port, sender, and recipient are named constants. |
| Guard clauses | Missing and empty carts return zero immediately; unmatched membership levels return the unchanged subtotal. | The workflow is straight-line orchestration; no unnecessary guards were added. |
| Less nesting | Membership selection uses `if`/`elif`; the zero minimum uses `max(total, 0)`. | Calculation, HTML formatting, and SMTP delivery are separate functions. |
| Less duplication | Membership discount arithmetic appears once in a helper. | The coordinator calls each reporting function once. |
| Documentation | Calculation and discount functions have docstrings. | Every reporting function and the coordinator class have docstrings. |

## One function, one responsibility

### Checkout

- `_apply_membership_discount()` selects and applies the membership discount.
- `calc()` calculates the checkout total by coordinating subtotal calculation and discounts.

Preserved business rules:

1. Calculate each item's price multiplied by its quantity, accumulating in the original order.
2. Apply a 10% membership discount for level 2 or a 20% discount for level 3.
3. Subtract 5 only when loyalty points are **strictly greater than 500**.
4. Return a minimum total of zero.

Missing and empty carts still return integer zero. Item keys remain `"p"` and `"q"`, and the example still prints `Total: 39.0`. Discount arithmetic retains `total - total * discount_rate` to preserve floating-point results.

### Sales report

- `summarize_sales()` calculates the sales count and total.
- `format_sales_report()` converts the summary into HTML without sending email.
- `send_sales_report()` handles SMTP delivery.
- `SalesReport.generate()` coordinates these steps and returns the delivered HTML, preserving the existing interface.

Changing SMTP delivery now affects the delivery function without requiring changes to calculation or formatting. The HTML, SMTP settings, call order, and tested exception behaviour remain unchanged.

`SalesReport` intentionally exposes one public operation. Its class-scoped `pylint: disable=too-few-public-methods` is documented: adding unrelated methods solely to meet a method-count rule would weaken the design. The final Pylint score includes this explicit exception.

## Results

Baseline scores were measured from the original files in commit `7337060`. Results below use the project's local virtual environment.

| Check | Checkout: before → after | Sales report: before → after |
| --- | --- | --- |
| Pylint | **8.00/10 → 10.00/10** | **8.42/10 → 10.00/10** |
| Radon main operation | `calc`: **B (8) → A (5)** | `generate`: **A (2) → A (1)** |
| Radon helper functions | Membership helper: **A (3)** | Summary: **A (2)**; formatting and delivery: **A (1)** each |
| Ruff, final version | All checks passed | All checks passed |

Radon measures control-flow complexity; it does not measure SRP directly. The report's main improvement is separating responsibilities, even though its original complexity was already low. Pylint and Ruff scores also do not prove behavioural correctness.

`pip-audit` reported **no known vulnerabilities** in the active environment's dependencies. This is an environment-level dependency check, not a security assessment of either Python file.

## Behaviour verification

- Checkout underwent five refinement passes, with **1,836 original-versus-refactored comparisons per pass**. Checks covered missing/empty carts, membership levels, the loyalty boundary, negative totals, return types, exact floating-point results, and example output.
- Sales reporting passed **32 original-versus-refactored comparisons**, checking returned HTML, SMTP call order, and connection, delivery, and shutdown failures.
- Five persistent regression tests in `tests/test_report.py` cover summaries, floating-point addition order, formatting without delivery, returned/sent HTML, and delivery errors.
- SMTP was mocked during verification: **no real emails were sent**.

The comparison checks were run as temporary review scripts. The five report regression tests are committed and can be rerun using the command below.

## Run the checks

From the repository root, with the existing virtual environment and tools installed:

```bash
source .venv/bin/activate

ruff check snippets/ tests/
pylint snippets/checkout.py
pylint snippets/report.py
radon cc -s snippets/checkout.py snippets/report.py
pip-audit
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

Run the checkout example with:

```bash
python snippets/checkout.py
```

Running `python snippets/report.py` uses the configured SMTP server and attempts to send an email. Use the mocked regression tests to verify reporting without delivery.
