from common import read_file


def parse_line(line: str) -> int:
    first = None
    last = None
    for i in range(len(line)):
        if not first:
            c = line[i]
            if str.isdigit(c):
                first = c
        if not last:
            c = line[-(i + 1)]
            if str.isdigit(c):
                last = c
        if first and last:
            break

    num = int(first + last)
    return num


nums = []
for line in read_file("input/1-1.txt"):
    nums.append(parse_line(line))

print(sum(nums))

if __name__ == "__main__":
    print(parse_line("1abc2"))
