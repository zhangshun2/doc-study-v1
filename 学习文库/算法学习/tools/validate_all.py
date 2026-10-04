#!/usr/bin/env python3
"""Run the cross-platform documentation and Java validation gate."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


LIBRARY_ROOT = Path(__file__).resolve().parent.parent
TOOLS_ROOT = LIBRARY_ROOT / "tools"


def main() -> int:
    commands = [
        ("Library contract", [sys.executable, str(TOOLS_ROOT / "validate_library.py")]),
        (
            "Java blocks and official examples",
            [sys.executable, str(TOOLS_ROOT / "verify_java_examples.py")],
        ),
    ]

    for label, command in commands:
        print(f"\n== {label} ==", flush=True)
        result = subprocess.run(command, cwd=str(LIBRARY_ROOT), check=False)
        if result.returncode != 0:
            print(f"\nValidation failed during: {label}", file=sys.stderr)
            return result.returncode

    print("\nAll validation gates passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
