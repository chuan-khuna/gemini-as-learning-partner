def with_cyan(text):
    return "\033[96m{}\033[00m".format(text)


def with_purple(text):
    return "\033[94m {}\033[00m".format(text)


def with_yellow(text):
    return "\033[93m {}\033[00m".format(text)


def with_green(text):
    return "\033[92m {}\033[00m".format(text)


def with_grey(text):
    return "\033[90m {}\033[00m".format(text)


with_gray = with_grey
