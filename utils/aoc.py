"""
Some advent of code utils for downloading input and submitting the result.
All copied from here: https://github.com/anthonywritescode/aoc2015/tree/main/support
with some pathlib.Path used instead of os.path
"""

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent


def _get_cookie_headers() -> dict[str, str]:
    return {"Cookie": (HERE.parent / ".env").read_text()}


def get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = urllib.request.Request(url, headers=_get_cookie_headers())
    return urllib.request.urlopen(req).read().decode()


def get_year_day() -> tuple[int, int]:
    """Get (year, day) based on the current working dir

    Substituted os.path with pathlib.Path according to this table:
    https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module
    """
    cwd = Path.cwd()
    day_s = Path(cwd).name
    year_s = Path(Path(cwd).parent).name

    if not day_s.startswith("day") or not year_s.startswith("adventofcode"):
        raise AssertionError(f"unexpected working dir: {cwd}")

    return int(year_s[len("adventofcode") :]), int(day_s[len("day") :])


def download_input() -> int:
    year, day = get_year_day()

    s = get_input(year, day)

    Path("input.txt").write_text(s)

    lines = s.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print("...")
    else:
        print(lines[0][:80])
        print("...")

    return 0


TOO_QUICK = re.compile("You gave an answer too recently.*to wait.")
WRONG = re.compile(r"That's not the right answer.*?\.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


def _post_answer(year: int, day: int, part: int, answer: str) -> str:
    params = urllib.parse.urlencode({"level": part, "answer": answer})
    req = urllib.request.Request(
        f"https://adventofcode.com/{year}/day/{day}/answer",
        method="POST",
        data=params.encode(),
        headers=_get_cookie_headers(),
    )
    resp = urllib.request.urlopen(req)

    return resp.read().decode()


def submit_solution() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, required=True)
    args = parser.parse_args()

    year, day = get_year_day()
    answer = sys.stdin.read()

    print(f"answer: {answer}")

    contents = _post_answer(year, day, args.part, answer)

    for error_regex in (WRONG, TOO_QUICK, ALREADY_DONE):
        error_match = error_regex.search(contents)
        if error_match:
            print(f"\033[41m{error_match[0]}\033[m")
            return 1

    if RIGHT in contents:
        print(f"\033[42m{RIGHT}\033[m")
        return 0
    else:
        # unexpected output?
        print(contents)
        return 1
