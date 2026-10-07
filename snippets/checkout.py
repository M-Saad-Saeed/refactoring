"""
SNIPPET 4 — Clean-code / coding practices (no SOLID needed)

Smells: cryptic names, magic numbers, duplication, deep nesting,
no guard clauses, a comment explaining what good names would say for free.

Your job (via the AI harness):
  Make it readable WITHOUT changing behaviour — meaningful names,
  named constants, guard clauses, remove duplication. Keep the output identical.
"""


MEMBERSHIP_LEVEL_TWO = 2
MEMBERSHIP_LEVEL_THREE = 3
MEMBERSHIP_LEVEL_TWO_DISCOUNT_RATE = 0.10
MEMBERSHIP_LEVEL_THREE_DISCOUNT_RATE = 0.20
LOYALTY_POINTS_THRESHOLD = 500
LOYALTY_DISCOUNT_AMOUNT = 5


def _apply_membership_discount(total, membership_level):
    """Apply the matching membership rate, or leave the total unchanged."""
    if membership_level == MEMBERSHIP_LEVEL_TWO:
        discount_rate = MEMBERSHIP_LEVEL_TWO_DISCOUNT_RATE
    elif membership_level == MEMBERSHIP_LEVEL_THREE:
        discount_rate = MEMBERSHIP_LEVEL_THREE_DISCOUNT_RATE
    else:
        return total

    return total - total * discount_rate


def calc(cart, membership_level, loyalty_points):
    """Apply membership then loyalty discounts, with a minimum total of zero."""
    if cart is None or len(cart) == 0:
        return 0

    subtotal = 0
    for item in cart:
        unit_price = item["p"]
        quantity = item["q"]
        subtotal = subtotal + unit_price * quantity

    total = _apply_membership_discount(subtotal, membership_level)
    if loyalty_points > LOYALTY_POINTS_THRESHOLD:
        total = total - LOYALTY_DISCOUNT_AMOUNT
    return max(total, 0)


if __name__ == "__main__":
    example_cart = [{"p": 20, "q": 2}, {"p": 15, "q": 1}]
    print("Total:", calc(example_cart, MEMBERSHIP_LEVEL_THREE, 600))
