"""
SNIPPET 3 — Dependency Inversion Principle (DIP)

Smell: the high-level OrderService reaches down and builds a concrete
EmailSender itself. It is welded to one delivery mechanism, so it can't
be tested without sending real email and can't switch to SMS.

Your job (via the AI harness):
  Invert the dependency — OrderService should depend on an abstraction
  that is PASSED IN, not on a concrete class it constructs.
  Then add an SmsSender without changing OrderService.
"""


class EmailSender:
    def send(self, message):
        print("EMAIL:", message)


class OrderService:
    def __init__(self):
        self.sender = EmailSender()   # hard-wired concrete dependency

    def place_order(self, item):
        # ... imagine real order logic here ...
        self.sender.send("Your order for " + item + " is confirmed.")


if __name__ == "__main__":
    OrderService().place_order("keyboard")
