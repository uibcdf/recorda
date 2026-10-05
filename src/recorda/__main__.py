"""Read a stored record without the producing library."""

import argparse
import json
from dataclasses import asdict

from .reader import inspect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="experimental JSONL journal to inspect")
    args = parser.parse_args()
    print(json.dumps(asdict(inspect(args.path)), indent=2))


if __name__ == "__main__":
    main()
