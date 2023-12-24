import z3
import numpy
from common import read_file_as_string, test


def parse_puzzle(example):
    return [
        tuple(
            tuple(int(p) for p in str.split(str.strip(part), ", "))
            for part in str.split(line, "@")
        )
        for line in str.split(str.strip(example), "\n")
    ]


def check_intersection(line_a, line_b):
    (x1, y1), (v1x, v1y) = line_a[0][:2], line_a[1][:2]
    (x2, y2), (v2x, v2y) = line_b[0][:2], line_b[1][:2]

    if not numpy.cross((v1x, v1y), (v2x, v2y)):
        return None

    numerator = (y2 - y1) + (x1 - x2) / v2x * v2y
    denominator = v1y - v1x * v2y / v2x

    t = numerator / denominator
    if t < 0:
        return None

    s = (x1 - x2 + t * v1x) / v2x
    if s < 0:
        return None

    return x1 + t * v1x, y1 + t * v1y


def pairs(n):
    return [(i, j) for i in range(n - 1) for j in range(i + 1, n)]


def future_intersections(lines, area):
    return len(
        [
            intersection
            for intersection in [
                check_intersection(lines[i], lines[j]) for i, j in pairs(len(lines))
            ]
            if intersection and is_in_area(intersection, area)
        ]
    )


def is_in_area(intersection, area):
    return all(area[0] < p < area[1] for p in intersection)


if __name__ == "__main__":
    example = read_file_as_string("input/24-ex.txt")
    test(
        future_intersections(
            parse_puzzle(example),
            [7, 27],
        ),
        2,
    )

    task = read_file_as_string("input/24.txt")
    task_parsed = parse_puzzle(task)
    test(
        future_intersections(
            task_parsed,
            [200_000_000_000_000, 400_000_000_000_000],
        ),
        18098,
    )

    # Part 2
    solver = z3.Solver()

    p = z3.RealVector("p", 3)
    v = z3.RealVector("v", 3)
    time = z3.RealVector("t", 4)

    solver.add(
        *[
            p[d] + v[d] * t == op[d] + ov[d] * t
            for t, (op, ov) in zip(time, task_parsed)
            for d in range(3)  # dimension size
        ]
    )
    solver.check()

    test(
        solver.model().eval(sum(p)),
        886858737029295,
    )
