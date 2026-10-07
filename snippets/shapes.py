"""
SNIPPET 2 — Open/Closed Principle (OCP)

Smell: every time we add a new shape we must crack open area() and add
another 'if'. The function is NOT closed for modification.

Your job (via the AI harness):
  Refactor so a new shape can be added WITHOUT editing existing code
  (hint: polymorphism / a common interface). Then add a Triangle to prove it.
"""

import math


def area(shape):
    if shape["type"] == "circle":
        return math.pi * shape["radius"] ** 2
    elif shape["type"] == "rectangle":
        return shape["width"] * shape["height"]
    elif shape["type"] == "square":
        return shape["side"] * shape["side"]
    else:
        raise ValueError("Unknown shape")


def total_area(shapes):
    return sum(area(s) for s in shapes)


if __name__ == "__main__":
    shapes = [
        {"type": "circle", "radius": 2},
        {"type": "rectangle", "width": 3, "height": 4},
        {"type": "square", "side": 5},
    ]
    print("Total area:", total_area(shapes))
