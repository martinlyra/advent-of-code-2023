from functools import reduce
from typing import Optional

from common import test


EXAMPLE = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""


class Node:
    def __init__(self, pos_x, pos_y, connectors: dict, start=False, tile='') -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.start = start
        self.connectors = connectors
        self.symbol = tile

    def unconnected(self) -> list[str]:
        return [key for key, node in self.connectors.items() if node is None]


def parse_map(map):
    rows = str.strip(map).split("\n")
    lines = [line for line in rows if len(line)]

    starting: Optional[Node] = None
    nodes: dict[int, dict[int, Optional[Node]]] = {}
    for i, line in enumerate(lines):
        nodes[i] = {j: parse_tile(i, j, tile) for j, tile in enumerate(line)}

    tiles: list[Node] = [
        tile
        for tile in reduce(lambda x, y: x + y, [list(d.values()) for d in nodes.values()])
        if tile
    ]
    starting = [tile for tile in tiles if tile.start][0]

    distance = check_connectivity(starting, nodes)

    return distance, starting, nodes


def parse_tile(x, y, tile) -> Optional[Node]:
    match tile:
        case ".":
            return None
        case "|":
            return Node(x, y, {"north": None, "south": None}, tile=tile)
        case "-":
            return Node(x, y, {"west": None, "east": None}, tile=tile)
        case "L":
            return Node(x, y, {"north": None, "east": None}, tile=tile)
        case "J":
            return Node(x, y, {"north": None, "west": None}, tile=tile)
        case "7":
            return Node(x, y, {"south": None, "west": None}, tile=tile)
        case "F":
            return Node(x, y, {"south": None, "east": None}, tile=tile)
        case "S":
            return Node(x, y, {}, start=True, tile=tile)
        case _:
            raise RuntimeError(f"Unknown tile symbol '{tile}'")


def check_connectivity(
    starting: Node, nodes: dict[int, dict[int, Optional[Node]]]
) -> int:
    def connect(node_a: Node, node_b: Node) -> bool:
        node_b_unconnected = node_b.unconnected()
        for key in node_a.unconnected():
            match key:
                case "north":
                    if (
                        "south" in node_b_unconnected
                        and node_a.pos_x > node_b.pos_x
                        and node_a.pos_y == node_b.pos_y
                    ):
                        node_a.connectors["north"] = node_b
                        node_b.connectors["south"] = node_a
                        return True
                case "south":
                    if (
                        "north" in node_b_unconnected
                        and node_a.pos_x < node_b.pos_x
                        and node_a.pos_y == node_b.pos_y
                    ):
                        node_a.connectors["south"] = node_b
                        node_b.connectors["north"] = node_a
                        return True
                case "east":
                    if (
                        "west" in node_b_unconnected
                        and node_a.pos_y < node_b.pos_y
                        and node_a.pos_x == node_b.pos_x
                    ):
                        node_a.connectors["east"] = node_b
                        node_b.connectors["west"] = node_a
                        return True
                case "west":
                    if (
                        "east" in node_b_unconnected
                        and node_a.pos_y > node_b.pos_y
                        and node_a.pos_x == node_b.pos_x
                    ):
                        node_a.connectors["west"] = node_b
                        node_b.connectors["east"] = node_a
                        return True
        return False

    start_x = starting.pos_x
    start_y = starting.pos_y
    rows = len(nodes)
    cols = len(nodes[0])

    neighbors = [
        node
        for node in [
            ("north", nodes[start_x - 1][start_y]) if start_x > 0 else None,
            ("south", nodes[start_x + 1][start_y]) if start_x < rows - 1 else None,
            ("west", nodes[start_x][start_y - 1]) if start_y > 0 else None,
            ("east", nodes[start_x][start_y + 1]) if start_y < cols - 1 else None,
        ]
        if node
    ]

    for neighbor in neighbors:
        direction, node = neighbor
        if node is None:
            continue
        starting.connectors[direction] = None
        if connect(starting, node):
            continue
        starting.connectors.pop(direction)
    
    travelled = 0
    current = None
    next_node: Optional[Node] = list(starting.connectors.values())[0]
    while next_node is not None:
        current = next_node
        directions = current.unconnected()
        if len(directions) < 1:
            next_node = None
            continue

        direction = directions[0]
        match direction:
            case "north":
                next_node = nodes[current.pos_x - 1][current.pos_y]
            case "south":
                next_node = nodes[current.pos_x + 1][current.pos_y]
            case "west":
                next_node = nodes[current.pos_x][current.pos_y - 1]
            case "east":
                next_node = nodes[current.pos_x][current.pos_y + 1]
        if not connect(current, next_node):
            raise RuntimeError("Failed to connect")
        travelled += 1

    return travelled


def farthest_point(map):
    distance, _, _ = parse_map(map)
    return int(distance / 2) + 1


if __name__ == "__main__":
    test(farthest_point(EXAMPLE), 8)

    with open("input/10-1.txt", "r") as f:
        source_info = "".join(f.readlines())

    print(farthest_point(source_info))
