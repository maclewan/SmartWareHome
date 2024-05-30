import re


class AnyInteger:
    def __eq__(self, other):
        return isinstance(other, int)


class AnyDateTime:
    def __eq__(self, other):
        pattern = (
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
            r"T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6}"
            r"\+[0-9]{2}:[0-9]{2}"
        )
        return re.match(pattern, other)
