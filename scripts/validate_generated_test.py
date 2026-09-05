"""Lightweight static checks for generated Playwright tests.

This is intentionally not a replacement for executing the tests. It catches a
few common AI-generation mistakes before execution.
"""

from pathlib import Path
import ast
import sys


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = []

    try:
        ast.parse(text)
    except SyntaxError as exc:
        errors.append(f"Syntax error: {exc}")
        return errors

    if "time.sleep(" in text:
        errors.append("Arbitrary time.sleep() detected.")
    if "wait_for_timeout(" in text:
        errors.append("Arbitrary wait_for_timeout() detected.")
    if "page.goto(" not in text:
        errors.append("No page.goto() found.")
    if "expect(" not in text:
        errors.append("No Playwright assertions found.")
    if "get_by_role(" not in text and "get_by_label(" not in text:
        errors.append("No semantic Playwright locator detected.")

    return errors


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("generated/flow_01_test.py")
    problems = validate(target)
    if problems:
        print("VALIDATION FAILED")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)

    print(f"STATIC VALIDATION PASSED: {target}")
