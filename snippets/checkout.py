"""
SNIPPET 4 — Clean-code / coding practices (no SOLID needed)

Smells: cryptic names, magic numbers, duplication, deep nesting,
no guard clauses, a comment explaining what good names would say for free.

Your job (via the AI harness):
  Make it readable WITHOUT changing behaviour — meaningful names,
  named constants, guard clauses, remove duplication. Keep the output identical.
"""


def calc(c, m, lp):
    # c = cart items, m = membership level, lp = loyalty points
    if c != None:
        if len(c) > 0:
            t = 0
            for i in c:
                t = t + i["p"] * i["q"]
            if m == 2:
                t = t - t * 0.10
            else:
                if m == 3:
                    t = t - t * 0.20
            if lp > 500:
                t = t - 5
            if t < 0:
                t = 0
            return t
        else:
            return 0
    else:
        return 0


if __name__ == "__main__":
    cart = [{"p": 20, "q": 2}, {"p": 15, "q": 1}]
    print("Total:", calc(cart, 3, 600))
