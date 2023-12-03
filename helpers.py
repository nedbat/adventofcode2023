def string_lines(text):
    return text.splitlines()


def file_lines(fname):
    with open(fname) as f:
        return [l.strip() for l in f]
