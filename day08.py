import pathlib
import re
from itertools import cycle

TEST_INPUT = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

FILE = pathlib.Path("day08_input.txt").read_text()

Graph = dict[str, list[str]]


def parse_table(text: str) -> tuple[str, Graph]:
    path, the_rest = text.split("\n\n")
    graph = {}
    for line in the_rest.splitlines():
        a, b, c = re.findall(r"[A-Z]{3}", line)
        graph[a] = [b, c]
    return (path, graph)


def traverse_graph(graph: Graph, path: str, start="AAA", end="ZZZ") -> int:
    steps_taken = 0
    path_to_travel = cycle(path)
    current_node = start
    while current_node != end:
        next_direction = next(path_to_travel)
        steps_taken += 1
        current_node = graph[current_node][0] if next_direction == "L" else graph[current_node][1]

    return steps_taken


def part1(text: str) -> int:
    path, graph = parse_table(text)
    return traverse_graph(graph, path)


def test_part1():
    assert part1(TEST_INPUT) == 6


if __name__ == "__main__":
    # answer = part1(TEST_INPUT)
    answer = part1(FILE)
    print(answer)


# def part2(text: str)-> int:
#     ...
#
#
# def test_part2():
#     assert part2(TEST_INPUT) == 123456
#
#
#
# if __name__ == "__main__":
#     answer = part2(FILE)
#     print(answer)
