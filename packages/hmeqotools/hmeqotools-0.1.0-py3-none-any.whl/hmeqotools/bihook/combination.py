import itertools as _itertools


class Combination:
    """组合键"""

    def __init__(self, *args, iter_=None, order=False):
        self.origin = self._parse_origin(iter_ if iter_ else args)
        self.items = self._parse_items(self.origin)
        order_data = tuple(_itertools.product(
            *[(i,) if isinstance(i, int) else i for i in self.origin]))
        if order_data == ((),):
            order_data = ()
        if order:
            self.data = set(order_data)
        else:
            self.data = {
                cb2 for cb in order_data
                for cb2 in _itertools.product(*([cb] * len(cb)))
                if len(cb2) == len(set(cb2))}
        self.str_data = tuple(" ".join(map(str, i)) for i in self.data)

    def __str__(self):
        return "%s%s" % (self.__class__.__name__, self.origin)

    def __len__(self):
        return len(self.origin)

    def __hash__(self):
        return self.origin.__hash__()

    def __add__(self, other):
        if isinstance(other, self.__class__):
            new = self.__class__()
            new.origin = self.origin + other.origin
            new.items = self.items + other.items
            new.data = set(i + j for i in self.data for j in other.data)
            new.str_data = tuple(
                i + " " + j for i in self.str_data for j in other.str_data)
            return new
        elif isinstance(other, int):
            other = (other,)
            new = self.__class__()
            new.origin = self.origin + other
            new.items = self.items + other
            new.data = set(i + other for i in self.data)
            new.str_data = tuple(
                i + " " + " ".join(map(str, other)) for i in self.str_data)
            return new
        raise TypeError()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return bool(
                other.data.intersection(self.data)
                or self.data.intersection(other.data))
        elif isinstance(other, int):
            return len(self.origin) == 1 and other in self.items
        return any(
            i in self.data for i in self.__class__(*other, order=True).data)

    def __contains__(self, other):
        if isinstance(other, self.__class__):
            if len(other) > len(self):
                return False
            return any(j in i for i in self.str_data for j in other.str_data)
        elif isinstance(other, int):
            return other in self.items
        return self.__class__(*other, order=True) in self

    @classmethod
    def _parse_origin(cls, lst):
        origin = []
        for i in lst:
            if isinstance(i, cls):
                origin.extend(i.origin)
            else:
                origin.append(i)
        return tuple(origin)

    @staticmethod
    def _parse_items(lst):
        items = []
        for cb in lst:
            if isinstance(cb, int):
                items.append(cb)
            else:
                items.extend(cb)
        if len(set(items)) != len(items):
            raise ValueError("Repeat item in args.")
        return tuple(items)

    __repr__ = __str__
