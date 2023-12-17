
def test(value, expected):
    print("Value: %s, Expected: %s" % (value, expected))
    assert value == expected


def read_file(file: str):
    with open(file, "rt", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                break

def read_file_as_string(file_path: str):
    return "".join(open(file_path, "rt", encoding="utf-8").readlines())
