from functools import reduce
from common import test


EXAMPLE = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def parse_line(line):
    left, right = tuple(str.split(line, " ")[:2])
    counts = [int(p) for p in str.split(right, ",")]
    return (left, counts)


def f(sequence, groups):
    cache = {}
    n = len(sequence)
    k = len(groups)

    def _f(index_pos, index_group, group_length):
        key = (index_pos, index_group, group_length)
        if key in cache:
            return cache[key]
        # Recrusion terminators
        if index_pos == n:
            if index_group == k and group_length == 0:
                return 1
            if index_group == k - 1 and group_length == groups[index_group]:
                return 1
            return 0

        # Dynamic transitions
        answer = 0
        for t in [".", "#"]:
            c = sequence[index_pos]
            if c == t or c == "?":
                if t == "." and group_length == 0:
                    answer += _f(index_pos + 1, index_group, 0)
                elif (
                    t == "."
                    and group_length > 0
                    and index_group < k
                    and groups[index_group] == group_length
                ):
                    answer += _f(index_pos + 1, index_group + 1, 0)
                elif t == "#":
                    answer += _f(index_pos + 1, index_group, group_length + 1)

        cache[key] = answer
        return answer

    return _f(0, 0, 0)


if __name__ == "__main__":
    example_lines = str.strip(EXAMPLE).split("\n")
    example_memo = [parse_line(line) for line in example_lines]
    example_counts = [f(line, groups) for line, groups in example_memo]
    test(example_counts, [1, 4, 1, 1, 4, 10])
    test(sum(example_counts), 21)

    with open("input/12.txt", "r") as file:
        source_info = "".join(file.readlines())

    task_memo = [parse_line(line) for line in str.strip(source_info).split("\n")]
    task_counts = [f(line, groups) for line, groups in task_memo]
    print(sum(task_counts))

    task_2_counts = [
        f("?".join([line] * 5), reduce(lambda x, y: x + y, [groups] * 5))
        for line, groups in task_memo
    ]
    print(sum(task_2_counts))
