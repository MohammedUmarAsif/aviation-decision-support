"""Compare recorded and reproduced analytical results with numeric tolerance."""

import json
import math
import sys


def compare(expected, actual) -> None:
    if isinstance(expected, dict):
        assert expected.keys() == actual.keys()
        for key in expected:
            compare(expected[key], actual[key])
    elif isinstance(expected, list):
        assert len(expected) == len(actual)
        for left, right in zip(expected, actual, strict=True):
            compare(left, right)
    elif isinstance(expected, float):
        assert math.isclose(expected, actual, rel_tol=1e-8, abs_tol=1e-8), (
            expected,
            actual,
        )
    else:
        assert expected == actual, (expected, actual)


if __name__ == "__main__":
    with (
        open(sys.argv[1], encoding="utf-8") as left,
        open(sys.argv[2], encoding="utf-8") as right,
    ):
        compare(json.load(left), json.load(right))
    print("Recorded forecast results reproduced within 1e-8 tolerance.")
