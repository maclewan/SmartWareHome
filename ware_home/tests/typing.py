class AnyInteger:
    def __eq__(self, other):
        return isinstance(other, int)
