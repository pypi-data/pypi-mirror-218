import bisect
import codecs
import collections
import encodings
import functools
import itertools
import math
import operator
import pathlib
import random
import re
import sys
import textwrap
from ast import literal_eval
from collections import deque, defaultdict, OrderedDict
from copy import deepcopy
from functools import reduce
from math import sqrt, floor, ceil
from typing import Iterable
from urllib import parse
import os
from catmapper import category_mapping
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from flatten_everything import flatten_everything, ProtectedTuple
from intersection_grouper import group_lists_with_intersections
from isiter import isiter
from list2tree import treedict
from nested2nested import nested_list_to_nested_dict
from typing import Any
from screwhashesset import ScrewHashesSet
from tolerant_isinstance import isinstance_tolerant
from levelflatten import level_flatten
from bisectsearch import (
    rightmost_value_equal_to,
    leftmost_value_equal_to,
    rightmost_value_less_than,
    rightmost_value_less_than_or_equal,
    leftmost_value_greater_than,
    leftmost_value_greater_than_or_equal,
)


class Trie:
    r"""
    Tr = Trie()
    Tr.trie_regex_from_words(['ich', 'du', 'er', 'sie', 'es', 'wir', 'der', 'die', 'das'])
    text = '.....'
    result = Tr.find(text)
    print(result)
    """

    def __init__(self):
        self.data = {}
        self.union = ""

    def add(self, word: str):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[""] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self.quote(char) + recurse)
                except Exception:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append("[" + "".join(cc) + "]")

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())

    def trie_regex_from_words(
        self,
        words: list,
        boundary_right: bool = True,
        boundary_left: bool = True,
        capture: bool = False,
        ignorecase: bool = False,
        match_whole_line: bool = False,
    ):
        for word in words:
            self.add(word)
        anfang = ""
        ende = ""
        if match_whole_line is True:
            anfang += r"^\s*"
        if boundary_right is True:
            ende += r"\b"
        if capture is True:
            anfang += "("
        if boundary_left is True:
            anfang += r"\b"
        if capture is True:
            ende += ")"

        if match_whole_line is True:
            ende += r"\s*$"
        if ignorecase is True:
            self.union = re.compile(anfang + self.pattern() + ende, re.IGNORECASE)
        else:
            self.union = re.compile(anfang + self.pattern() + ende)


def checkiter(x):
    try:
        _ = iter(x)
        return True
    except TypeError:
        return False


def float_check_nan(num):
    if float("-inf") < float(num) < float("inf"):
        return False
    else:
        return True


def is_nan(
    x: Any,
    emptyiters: bool = False,
    nastrings: bool = False,
    emptystrings: bool = False,
    emptybytes: bool = False,
) -> bool:
    # useful when you read a csv file and the missing data is not converted correctly to nan
    nastringlist = [
        "<NA>",
        "<NAN>",
        "<nan>",
        "np.nan",
        "NoneType",
        "None",
        "-1.#IND",
        "1.#QNAN",
        "1.#IND",
        "-1.#QNAN",
        "#N/A N/A",
        "#N/A",
        "N/A",
        "n/a",
        "NA",
        "#NA",
        "NULL",
        "null",
        "NaN",
        "-NaN",
        "nan",
        "-nan",
    ]
    if isinstance(x, type(None)):
        return True
    try:
        if str(x.real) == "nan":
            return True
    except Exception:
        pass
    try:
        if x.__class__.__name__ == "NAType":
            return True
    except Exception:
        pass

    try:
        if math.isnan(x):
            return True
    except Exception:
        pass
    try:
        if x != x:
            return True
    except Exception:
        pass
    try:
        if not isinstance(x, str):
            if float_check_nan(x) is True:
                return True
    except Exception:
        pass
    if emptystrings is True:
        if isinstance(x, str):
            try:
                if x == "":
                    return True
            except Exception:
                pass
    if emptybytes is True:
        if isinstance(x, bytes):
            try:
                if x == b"":
                    return True
            except Exception:
                pass
    if nastrings is True:
        if isinstance(x, str):
            try:
                if x in nastringlist:
                    return True
            except Exception:
                pass
    if emptyiters is True:
        if isinstance(x, (str, bytes)):
            pass
        else:
            if isinstance(x, Iterable) or checkiter(x):
                try:
                    if not any(x.tolist()):
                        return True
                except Exception:
                    pass
                if str(type(x)) in [
                    "pandas.core.series.Series",
                    "pandas.core.frame.DataFrame",
                ]:
                    try:
                        if x.empty:
                            return True
                    except Exception:
                        pass
                try:
                    if not any(x):
                        return True
                except Exception:
                    pass

                try:
                    if not x:
                        return True
                except Exception:
                    pass
                try:
                    if len(x) == 0:
                        return True
                except Exception:
                    pass
    return False


def polymul(p, q):
    """
    Multiply two polynomials, represented as lists of coefficients.
    """
    r = [0] * (len(p) + len(q) - 1)
    for i, c in enumerate(p):
        for j, d in enumerate(q):
            r[i + j] += c * d
    return r


@functools.lru_cache
def get_codecs():
    dir = encodings.__path__[0]
    codec_names = OrderedDict()
    for filename in os.listdir(dir):
        if not filename.endswith(".py"):
            continue
        name = filename[:-3]
        try:
            codec_names[name] = OrderedDict({"object": codecs.lookup(name)})
        except Exception as Fehler:
            pass
    return codec_names


def uri_validator(x):
    try:
        result = parse.urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def euclid_dist(x0, y0, x1, y1):
    dx_sq = (x0 - x1) ** 2
    dy_sq = (y0 - y1) ** 2
    return sqrt(dx_sq + dy_sq)


def teex(iterable, n=2):
    it = iter(iterable)
    deques = [collections.deque() for i in range(n)]

    def gen(mydeque):
        while True:
            if not mydeque:  # when the local deque is empty
                try:
                    newval = next(it)  # fetch a new value and
                except StopIteration:
                    return
                for d in deques:  # load it to all the deques
                    d.append(newval)
            yield mydeque.popleft()

    return tuple(gen(d) for d in deques)


def convert_to_normal_dict(di):
    if isinstance_tolerant(di, defaultdict):
        di = {k: convert_to_normal_dict(v) for k, v in di.items()}
    return di


def groupBy(key, seq, continue_on_exceptions=True, withindex=True, withvalue=True):
    indexcounter = -1

    def execute_f(k, v):
        nonlocal indexcounter
        indexcounter += 1
        try:
            return k(v)
        except Exception as fa:
            if continue_on_exceptions:
                return "EXCEPTION: " + str(fa)
            else:
                raise fa

    # based on https://stackoverflow.com/a/60282640/15096247
    if withvalue:
        return convert_to_normal_dict(
            reduce(
                lambda grp, val: grp[execute_f(key, val)].append(
                    val if not withindex else (indexcounter, val)
                )
                or grp,
                seq,
                defaultdict(list),
            )
        )
    return convert_to_normal_dict(
        reduce(
            lambda grp, val: grp[execute_f(key, val)].append(indexcounter) or grp,
            seq,
            defaultdict(list),
        )
    )


def iter_windowed(iterable, n):
    accum = deque((), n)
    for element in iterable:
        accum.append(element)
        if len(accum) == n:
            yield tuple(accum)


def pairwise(iterable):
    a, b = teex(iterable)
    next(b, None)
    return zip(a, b)


def iter_batch(iterable, n):
    # https://stackoverflow.com/a/74997058/15096247
    _consume = collections.deque(maxlen=0).extend
    "Batch data into sub-iterators of length n. The last batch may be shorter."
    # batched_it('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    n -= (
        1  # First element pulled for us, pre-decrement n so we don't redo it every loop
    )
    it = iter(iterable)
    for first_el in it:
        chunk_it = itertools.islice(it, n)
        try:
            yield itertools.chain((first_el,), chunk_it)
        finally:
            _consume(chunk_it)  # Efficiently consume any elements caller didn't consume


class NestedList(list):
    def __new__(
        cls,
        initlist=None,
        maxsize=None,
        convert_all=False,
        line_limit=160,
        print_limit=1000,
        *args,
        **kwargs,
    ):
        v = super().__new__(cls, initlist)
        v.maxsize = maxsize
        v.print_limit = print_limit
        v.convert_all = convert_all
        v.line_limit = line_limit
        return v

    def __init__(
        self,
        initlist=None,
        maxsize=None,
        convert_all=False,
        line_limit=160,
        print_limit=1000,
    ):
        try:
            super().__init__(initlist)
        except TypeError as e:
            if self.convert_all:
                super().__init__([initlist])
            else:
                raise e
        self._deli()

    def _deli(self):
        if self.maxsize:
            if (len(self)) > self.maxsize:
                del self[: -self.maxsize]

    def append(self, o):
        super().append(o)
        self._deli()

    def __str__(self):
        addto = "" if len(self) <= self.print_limit else "\n..."
        tostr = []
        for ini, d in enumerate(super().__iter__()):
            tostr.append(str(d))
            if ini >= self.print_limit:
                break
        return (
            "["
            + "\n".join(
                textwrap.wrap(
                    ", ".join(tostr) + addto,
                    width=self.line_limit,
                )
            )
            + "]"
        )

    def __repr__(self):
        return self.__str__()

    def __delitem__(self, i):
        if isinstance(i, (list, tuple)):
            if len(i) > 1:
                lastkey = i[-1]
                i = i[:-1]
                it = iter(i)
                firstkey = next(it)
                value = self[firstkey]
                for element in it:
                    value = operator.itemgetter(element)(value)
                del value[lastkey]
                return

            else:
                super().__delitem__(i[0])
                return
        super().__delitem__(i)

    def __getitem__(self, i):
        if isinstance(i, (list, tuple)):
            if len(i) > 1:
                it = iter(i)
                firstkey = next(it)
                value = self[firstkey]

                for element in it:
                    value = operator.itemgetter(element)(value)
                return value
            else:
                return super().__getitem__(i[0])
        else:
            if isinstance(i, slice):
                return self.__class__(super().__getitem__(i))
            return super().__getitem__(i)

    def __setitem__(self, i, item):
        if isinstance(i, (list, tuple)):
            if len(i) > 1:
                lastkey = i[-1]
                i = i[:-1]
                it = iter(i)
                firstkey = next(it)
                value = self[firstkey]

                for element in it:
                    value = operator.itemgetter(element)(value)
                value[lastkey] = item
            else:
                super().__setitem__(i[0], item)
        else:
            super().__setitem__(i, item)

    def __add__(self, other):
        if isinstance(
            other, (str, bytes, int, float, complex, bool, type(None), dict)
        ) or (
            hasattr(other, "keys")
            and hasattr(other, "items")
            and hasattr(other, "values")
        ):
            return self.__class__(self + [other])
        try:
            return super().__add__(other)
        except TypeError:
            return self.__class__(self + [other])

    def __iadd__(self, other, /):
        if isinstance(
            other, (int, float, complex, str, bytes, bool, dict, type(None))
        ) or (
            hasattr(other, "keys")
            and hasattr(other, "items")
            and hasattr(other, "values")
        ):
            super().append(other)

        else:
            try:
                super().__iadd__(other)

            except TypeError:
                try:
                    super().__iadd__(list(other))
                except TypeError:
                    super().__iadd__([other])
        self._deli()
        return self

    def __sub__(self, other):
        if not isiter(other):
            other = [other]
        selfcopy = self.copy()
        for o in other:
            if o in self:
                del selfcopy[selfcopy.index(o)]
        return selfcopy

    def __isub__(self, other):
        if not isiter(other):
            other = [other]
        for o in other:
            if o in self:
                del self[self.index(o)]
        return self

    def __truediv__(self, other):
        return [self[i : i + other] for i in range(len(self)) if i % other == 0]

    def __floordiv__(self, other):
        newother, rest = divmod(len(self), other)
        v = self.__truediv__(newother)
        if rest != 0 and len(v).__gt__(1):
            v[-2].extend(v[-1])
            del v[-1]
        return v

    def __itruediv__(self, other):
        v = self.__truediv__(other)
        self.clear()
        self.extend(v)
        return self

    def __ifloordiv__(self, other):
        v = self.__floordiv__(other)
        self.clear()
        self.extend(v)
        return self
    def extend(self, other) -> None:
        super().extend(other)
        self._deli()
    def insert(self, index, value) -> None:
        super().insert(index,value)
        self._deli()
    def extendleft(self,other):
        for _ in other:
            self.insert(0,_)
        self._deli()

    def convert_all_to_nested_list(self):
        for v, k in fla_tu(self):
            for i in range(len(k)):
                li = list(k[: i + 1])
                if isinstance(self[li], list) and not isinstance(
                    self[li], self.__class__
                ):
                    self[li] = self.__class__(self[li])

    def search(self, value):
        alreadydone = []
        for v, k in fla_tu(self):
            for i in range(len(k)):
                kt = k[: i + 1]
                if kt not in alreadydone:
                    alreadydone.append(kt)
                    li = list(kt)
                    if self[li] == value:
                        yield li

    def convert_to_list(self):
        for v, k in fla_tu(self):
            for i in range(len(k)):
                li = list(k[: i + 1])
                if isinstance(self[li], self.__class__):
                    self[li] = list(self[li])
        return list(self)

    def to_nested_dict(self):
        return nested_list_to_nested_dict(self)

    def flatten(self):
        return self.__class__((x[0] for x in fla_tu(self)))

    def flatten_with_index(self):
        return self.__class__(((x[1], x[0]) for x in fla_tu(self)))

    def remove_duplicates(self):
        return self.__class__((ScrewHashesSet(self)))

    def sorted(self, func, reverse=False):
        return self.__class__(sorted(self, key=func, reverse=reverse))

    def split_by_indices(self, indices):
        indices = sorted(indices)
        return self.__class__(
            (self[p[0] : p[1]] for p in pairwise([0] + indices + [len(self)]))
        )

    def get_iter_every_nth_element(self, step=2):
        return itertools.islice(self, 0, len(self), step)

    def repeat_items(self, reps):
        return self.__class__(((x for x in self for i in range(reps))))

    def get_iter_windowed(self, n):
        return iter_windowed(self, n)

    def get_iter_batch(self, n):
        for x in iter_batch(self, n):
            yield self.__class__(x)

    def get_iter_nested_for_loop(self):
        return itertools.product(*self)

    def get_iter_nested_for_loop_enumerated(self):
        co = 0
        for vals in itertools.product(*self):
            yield co, *vals
            co += 1

    def get_iter_add_one_item_each_iteration(self):
        for i in range(len(self)):
            yield self[: i + 1]

    def get_iter_add_one_item_each_iteration_reverse(self):
        l = len(self)
        for i in range(l):
            yield self[l - i - 1 :]

    def get_iter_nested(self):
        vara = self.copy()
        for x in fla_tu(vara):
            n = len(x[1])
            foryield = []
            for i in range(n):
                foryield.append(reduce(operator.getitem, x[1][: i + 1], vara))
            yield foryield

    def get_iter_nested_with_path(self):
        try:
            vara = self.copy()
        except Exception:
            vara = self
        for x in fla_tu(vara):
            n = len(x[1])
            foryield = []
            for i in range(n):
                foryield.append(
                    (x[1][: i + 1], reduce(operator.getitem, x[1][: i + 1], vara))
                )
            yield foryield

    def get_iter_find_same_ending_elements(self):
        iters = self
        iterables = [list(reversed(x)) for x in iters]
        return reversed(
            [
                x[0]
                for x in itertools.takewhile(
                    lambda x: len(set(x)) == 1, zip(*iterables)
                )
            ]
        )

    def get_iter_find_same_beginning_elements(self):
        return (
            x[0] for x in itertools.takewhile(lambda x: len(set(x)) == 1, zip(*self))
        )

    def reshape(self, how):
        def iter_reshape(seq, how):
            """
            # based on sympy.utilities.reshape
            """
            m = sum(flatten_everything(how))
            seq = list(flatten_everything(seq))
            n, rem = divmod(len(seq), m)
            if m < 0 or rem:
                raise ValueError(
                    f"template must sum to positive number that divides the length of the sequence, len is: {m}"
                )

            i = 0
            container = type(how)
            rv = [None] * n
            for k in range(len(rv)):
                _rv = []
                for hi in how:
                    if isinstance(hi, int):
                        _rv.extend(seq[i : i + hi])
                        i += hi
                    else:
                        n = sum(list(flatten_everything(hi)))
                        hi_type = type(hi)
                        _rv.append(hi_type(iter_reshape(seq[i : i + n], hi)[0]))
                        i += n
                rv[k] = container(_rv)
            return type(seq)(rv)

        return self.__class__((iter_reshape(self, how)[0]))

    def get_iter_rotate_left(self, n, onlyfinal=False):
        iterable_ = self.copy()
        for _ in range(n):
            iterable_ = iterable_[1:] + iterable_[:1]
            if not onlyfinal:
                yield iterable_
        if onlyfinal:
            yield iterable_

    def shape_repeat(self, shape):
        variable = self.copy()
        return self.__class__(
            reduce(
                lambda a, b: list(itertools.repeat(a, b)),
                shape,
                variable,
            )
        )

    def get_iter_rotate_right(self, n, onlyfinal=False):
        iterable_ = self.copy()

        for _ in range(n):
            iterable_ = iterable_[-1:] + iterable_[:-1]
            if not onlyfinal:
                yield iterable_
        if onlyfinal:
            yield iterable_

    def get_iter_enumerated_unpacked(self):
        for it in zip(itertools.count(), *self):
            yield it

    def get_iter_cycle_shortest(self, other):
        turnaround = (len(other)) > (len(self))
        if turnaround:
            la = other
            lb = self
        else:
            la = self
            lb = other
        if turnaround:
            looplist = ((y, x) for x, y in zip(la, itertools.cycle(lb)))
        else:
            looplist = ((x, y) for x, y in zip(la, itertools.cycle(lb)))
        return looplist

    def get_iter_reverse_lists_of_list(self):
        return (list(reversed(aa)) for aa in self)

    def get_iter_stop_when_next_item_is_duplicate(self):
        """https://github.com/joelgrus/stupid-itertools-tricks-pydata/blob/master/src/stupid_tricks.py"""

        def no_repeat(prev, curr):
            if prev == curr:
                raise StopIteration
            else:
                return curr

        return itertools.accumulate(self, no_repeat)

    def get_iter_nested_one_ahead(self):
        vara = self.copy()
        flali = list(fla_tu(vara))
        for x, x2 in itertools.zip_longest(flali, flali[1:]):
            n = len(x[1])
            foryield = []
            foryield1 = []
            for i in range(n):
                foryield1.append(reduce(operator.getitem, x[1][: i + 1], vara))
            foryield.append(foryield1.copy())
            foryield2 = []

            if not is_nan(x2):
                n = len(x2[1])
                for i in range(n):
                    foryield2.append(reduce(operator.getitem, x2[1][: i + 1], vara))
            if not any(foryield2):
                return
            foryield.append(foryield2.copy())
            yield foryield

    def get_iter_random_values_from_iter_endless(self):
        v = list(flatten_everything(self))
        while True:
            random.shuffle(v)
            yield from v

    def groupby_element_pos(
        self, pos, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda v: v[pos] if len(v) > pos else "",
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_substring(
        self, substrings, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        g = re.compile(
            "|".join(
                [
                    re.escape(substrings[: _ + 1])
                    for _ in reversed(range(len(substrings)))
                ]
            )
        )
        return groupBy(
            key=lambda i: sorted(h, key=lambda i: len(i))[-1]
            if (h := g.findall(i))
            else "",
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def count_all_items(self):
        d = defaultdict(int)
        tmpdict = {}
        for k in self:
            try:
                d[k] += 1
            except TypeError:
                strrep = f"{k}{repr(k)}"
                if strrep not in tmpdict:
                    tmpdict[strrep] = k
                d[strrep] += 1
        finalresults = []
        for k, v in d.items():
            if k in tmpdict:
                finalresults.append((tmpdict[k], v))
            else:
                finalresults.append((k, v))
        return finalresults

    def find_common_start_string(self):
        counter = 1
        resu = []
        while (
            len(
                g := (
                    self.groupby_startswith(
                        n=counter,
                        continue_on_exceptions=True,
                        withindex=False,
                        withvalue=True,
                    )
                )
            )
            == 1
        ):
            counter += 1
            resu.append(tuple(g.keys())[0])
        if resu:
            return resu[-1]
        return ""

    def get_iter_item_difference(self):
        return (x[1] - x[0] for x in zip(self, self[1:]))

    def find_sequence(self, seq: tuple, distance_tolerance=0):
        res = []
        resseq = []
        for s in seq:
            allind = self.index_all(s)
            for a in allind:
                bisect.insort(res, a)
                rightind = rightmost_value_equal_to(res, a)
                resseq.insert(rightind, s)

        for a, v in zip(
            self.__class__(res).get_iter_windowed(n=len(seq)),
            self.__class__(resseq).get_iter_windowed(n=len(seq)),
        ):
            if v == seq:
                di = sum(list(self.__class__(a).get_iter_item_difference())) + 1
                if di <= len(seq) + distance_tolerance:
                    yield a

    def index_all(self, n):
        indototal = 0
        allindex = []
        while True:
            try:
                indno = self[indototal:].index(n)
                indototal += indno + 1
                allindex.append(indototal - 1)
            except ValueError:
                break
        return allindex

    def popleft(self):
        v = self[0]
        del self[0]
        return v

    def appendleft(self, v):
        self.insert(0, v)

    def del_items(self, value):
        for i, v in enumerate(self.index_all(value)):
            delx = v - i
            del self[delx]

    def get_random_values_with_max_rep(self, howmany, maxrep):
        resi = []
        resistr = []
        numbers = self
        alldi = {f"{repr(x)}{x}": x for x in numbers}
        numbersdi = {}
        for ma in range(maxrep):
            for key, item in alldi.items():
                numbersdi[f"{key}{ma}"] = item
        if (h := len(numbersdi.keys())) < howmany:
            raise ValueError(f"choices: {howmany} / unique: {h}")
        while len(resi) <= howmany - 1:
            [
                (resi.append(numbersdi[g]), resistr.append(g))
                for x in range(len(numbers))
                if len(resi) <= howmany - 1
                and (g := random.choice(tuple(set(numbersdi.keys()) - set(resistr))))
                not in resistr
            ]
        return resi

    def get_random_not_repeating_values(self, howmany):
        resi = []
        resistr = []
        numbers = self
        numbersdi = {f"{repr(x)}{x}": x for x in numbers}
        if (h := len(numbersdi.keys())) < howmany:
            raise ValueError(f"choices: {howmany} / unique: {h}")
        while len(resi) <= howmany - 1:
            [
                (resi.append(numbersdi[g]), resistr.append(g))
                for x in range(len(numbers))
                if len(resi) <= howmany - 1
                and (g := random.choice(tuple(set(numbersdi.keys()) - set(resistr))))
                not in resistr
            ]
        return resi

    def get_cycle_list_until_every_list_fits(
        self,
        maxresults=5,
        append=False,
    ):
        def sort_dict(di):
            return {k: v for k, v in sorted(di.items(), key=lambda x: x[0])}

        args = list(reversed(sorted(self, key=len)))
        lenargs = [len(x) for x in args]
        lenargsmax = max(lenargs)
        lenargs_ = len(lenargs)
        a = []

        co = 0
        done = False
        while not done:
            co += 1
            for i in range(2, math.prod(lenargs)):
                if len([co * i for co in lenargs if co * i % i == 0]) == lenargs_:
                    a.append(co * i)
                if len(a) >= maxresults * 4:
                    done = True
                    break
        a.sort()
        a = list(reversed(a))
        resusa = {}
        for so in a:
            resusatemp = defaultdict(list)
            for ii, ba in enumerate(args):
                for i in range(lenargsmax * so // len(ba)):
                    if append:
                        resusatemp[ii].append(ba)
                    else:
                        resusatemp[ii].extend(ba)
            resusa[lenargsmax * so] = resusatemp
        resusa = sort_dict(resusa)
        resusa2 = resusa.copy()
        gop = []
        for key, item in resusa.items():
            allsi = []
            for key2, item2 in item.items():
                aax = tuple(flatten_everything(item2))
                allsi.append(len(aax))
            if len(set(allsi)) != 1:
                del resusa2[key]
            else:
                gop.append(key)
                if len(gop) >= maxresults:
                    break

        for key in list(resusa2.keys()):
            if key not in gop:
                del resusa2[key]
        return convert_to_normal_dict(resusa2)

    def group_by(
        self, func, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=func,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def number_of_combinations(self, k):
        """
        from https://stackoverflow.com/a/48612518/15096247
        Number of combinations of length *k* of the elements of *it*.
        """
        counts = collections.Counter(self).values()
        prod = reduce(polymul, [[1] * (count + 1) for count in counts], [1])
        return prod[k] if k < len(prod) else 0

    def flatten_and_group_by(
        self, func, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=func,
            seq=list(flatten_everything(self)),
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def get_normalized_list_of_lists(self, fillv=None):
        ml = max([len(x) for x in self])
        nl = []
        _ = [x for x in self if (nl.append((x + ([fillv] * (ml - len(x))))))]
        return nl

    def get_iter_transposed_list_of_lists(self):
        return (list(x) for x in zip(*self))

    def get_shuffle_copied_list(self):
        l1 = deepcopy(self)
        random.shuffle(l1)
        return l1

    def get_iter_call_function_over_and_over_with_new_value(self, f):
        """https://github.com/joelgrus/stupid-itertools-tricks-pydata/blob/master/src/stupid_tricks.py"""
        return itertools.accumulate(itertools.repeat(self), lambda fx, _: f(fx))

    def get_iter_windowed_distance(self, fillvalue=None, distance=1):
        it = self
        cou = 0
        for a, b, c in itertools.zip_longest(
            ([fillvalue] * distance) + it, it, it[distance:], fillvalue=fillvalue
        ):
            yield a, b, c
            cou += 1

            if cou == len(it):
                return

    def get_iter_2_cycle_second_until_first_done(self, other):
        return ((x, y) for x, y in zip(self, itertools.cycle(other)))

    def list_of_tuples_to_family_tree(self, main_mapping_keys=(), bi_rl_lr="bi"):
        mapped, airvar = treedict(
            pairs_list=self, main_mapping_keys=main_mapping_keys, bi_rl_lr=bi_rl_lr
        )
        return mapped, airvar

    def get_levenshtein_distance(self, strings):
        if isinstance(strings, str):
            strings = [strings]

        def levenshtein_distance(str1, str2):
            m = len(str1)
            n = len(str2)

            # Create a matrix to store the distances
            distances = [[0] * (n + 1) for _ in range(m + 1)]

            # Initialize the first row and column
            for i in range(m + 1):
                distances[i][0] = i
            for j in range(n + 1):
                distances[0][j] = j

            # Compute the distances
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if str1[i - 1] == str2[j - 1]:
                        distances[i][j] = distances[i - 1][j - 1]
                    else:
                        distances[i][j] = 1 + min(
                            distances[i - 1][j],
                            distances[i][j - 1],
                            distances[i - 1][j - 1],
                        )

            return distances[m][n]

        return self.__class__(
            [
                sorted(
                    [
                        (levenshtein_distance(str(x), str1), ini, x, str1)
                        for ini, x in enumerate(self)
                    ]
                )
                for str1 in strings
            ]
        )

    def flatten_level(
        self, n=None, dict_treatment="items", consider_non_iter=(str, bytes)
    ):
        if not n:
            n = sys.maxsize
        return level_flatten(
            self,
            n=n,
            dict_treatment=dict_treatment,
            consider_non_iter=consider_non_iter,
        )

    def groupby_euclid_dist(
        self,
        coord,
        mindistance=0,
        maxdistance=500,
        continue_on_exceptions=True,
        withindex=False,
        withvalue=True,
    ):
        return groupBy(
            key=lambda x: True
            if (u := euclid_dist(*coord, *x)) >= mindistance and u <= maxdistance
            else False,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_string_length(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: len(str(x)),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def group_values_in_flattened_nested_iter_and_count(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        li = groupBy(
            key=lambda x: x,
            seq=flatten_everything(self),
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )
        for key, item in li.copy().items():
            li[key] = len(item)
        return li

    def groupby_type(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: type(x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_frequency(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: self.count(x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_can_be_divided_by(
        self, div, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: True if x % div == 0 else False,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_division_remainder(
        self, div, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: divmod(x, div)[1],
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_divisor(
        self, div, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: divmod(x, div)[0],
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_bigger_than_or_equal(
        self, number, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: True if x >= number else False,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_less_than_or_equal(
        self, number, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: True if x <= number else False,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_bigger_than(
        self, number, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: True if x > number else False,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_less_than(
        self, number, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: True if x < number else False,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_equal(
        self, number, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: True if x == number else False,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_regular_expression_matches(
        self,
        regexpressions,
        continue_on_exceptions=True,
        withindex=False,
        withvalue=True,
    ):
        if not isinstance_tolerant(regexpressions, list):
            regexpressions = [regexpressions]
        compr = [re.compile(regexpression) for regexpression in regexpressions]

        def checkexp(compr, x):
            for co in compr:
                if co.search(str(x)) is not None:
                    return True
            return False

        return groupBy(
            key=lambda x: checkexp(compr, x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_is_integer(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: float(x).is_integer(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_floor(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: floor(x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_ceil(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: ceil(x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_round(
        self, n, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: round(x, n),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_endswith(
        self, n, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: str(x)[-n:],
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_startswith(
        self, n, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: str(x)[:n],
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_first_occurrence_in_string(
        self, char, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: str(x).find(char),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isalnum(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isalnum(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isalpha(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isalpha(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isascii(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isascii(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isdecimal(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isdecimal(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isdigit(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isdigit(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isidentifier(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isidentifier(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_islower(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.islower(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isnumeric(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isnumeric(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isprintable(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isprintable(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isspace(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isspace(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_istitle(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.istitle(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isupper(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x.isupper(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_last_occurrence_in_string(
        self, char, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: str(x).rfind(char),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isin(
        self, value, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: value in x,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_isiter(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: isiter(x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_file_extension(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: str(pathlib.Path(x).suffix).lower(),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_even_odd(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: "even" if x % 2 == 0 else "odd",
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_files_folder_link(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: "folder"
            if os.path.isdir(x)
            else "file"
            if os.path.isfile(x)
            else "link"
            if os.path.islink(x)
            else "unknown",
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_sys_size(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: sys.getsizeof(x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_first_item(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: x[0],
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_sum(self, continue_on_exceptions=True, withindex=False, withvalue=True):
        return groupBy(
            key=lambda x: sum(x),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_valid_url(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: "valid" if uri_validator(x) else "not_valid",
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_decoding_result(
        self,
        mode="strict",
        continue_on_exceptions=True,
        withindex=False,
        withvalue=True,
    ):
        seq = get_codecs()
        result = []
        for bytes_ in self:
            result.append(
                groupBy(
                    key=lambda x: bytes_.decode(x, mode),
                    seq=seq,
                    continue_on_exceptions=continue_on_exceptions,
                    withindex=withindex,
                    withvalue=withvalue,
                )
            )
        return result

    def groupby_literal_eval_type(
        self, continue_on_exceptions=True, withindex=False, withvalue=True
    ):
        return groupBy(
            key=lambda x: type((literal_eval(x))),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_percentage(
        self,
        percent_true,
        group1=True,
        group2=False,
        continue_on_exceptions=True,
        withindex=False,
        withvalue=True,
    ):
        return groupBy(
            key=lambda x: random.choices(
                [group1, group2],
                [int(percent_true * 100), int(10000 - percent_true * 100)],
            )[0],
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_almost_equal(
        self,
        value,
        equallimit,
        continue_on_exceptions=True,
        withindex=False,
        withvalue=True,
    ):
        return groupBy(
            key=lambda x: abs(x - value) <= equallimit,
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def groupby_coords_almost_equal(
        self,
        x_coord,
        y_coord,
        limit_x,
        limit_y,
        continue_on_exceptions=True,
        withindex=False,
        withvalue=True,
    ):
        return groupBy(
            key=lambda x: (
                abs(x[0] - x_coord) <= limit_x,
                abs(x[1] - y_coord) <= limit_y,
            ),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def group_intersections(self, keep_duplicates=False):
        return self.__class__(group_lists_with_intersections(self,keep_duplicates))

    def group_coordinates_by_distance(
        self, coordlist, limit_x, limit_y, continue_on_exceptions=True
    ):
        alltrues = []
        for _ in coordlist:
            xxx = self.groupby_coords_almost_equal(
                x_coord=_[0],
                y_coord=_[1],
                limit_x=limit_x,
                limit_y=limit_y,
                continue_on_exceptions=continue_on_exceptions,
                withindex=False,
                withvalue=True,
            )
            alltrues.append(xxx.get((True, True)))
        return self.__class__(
            group_lists_with_intersections(alltrues, keep_duplicates=False)
        )

    def groupby_words_in_texts(
        self,
        wordlist,
        case_sen=False,
        continue_on_exceptions=True,
        withindex=False,
        boundary_right=True,
        boundary_left=True,
        withvalue=True,
    ):
        trie = Trie()
        trie.trie_regex_from_words(
            words=wordlist,
            boundary_right=boundary_right,
            boundary_left=boundary_left,
            capture=True,
            match_whole_line=False,
        )
        if not case_sen:
            compr = re.compile(str(trie.union.pattern), flags=re.I)
        else:
            compr = re.compile(str(trie.union.pattern))

        return groupBy(
            key=lambda x: tuple(
                [k for k in flatten_everything(compr.findall(x)) if k != ""]
            ),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def bisect_rightmost_value_equal_to(self, n):
        return rightmost_value_equal_to(self, n)

    def bisect_leftmost_value_equal_to(self, n):
        return leftmost_value_equal_to(self, n)

    def bisect_rightmost_value_less_than(self, n):
        return rightmost_value_less_than(self, n)

    def bisect_rightmost_value_less_than_or_equal(self, n):
        return rightmost_value_less_than_or_equal(self, n)

    def bisect_leftmost_value_greater_than(self, n):
        return leftmost_value_greater_than(self, n)

    def bisect_leftmost_value_greater_than_or_equal(self, n):
        return leftmost_value_greater_than_or_equal(self, n)

    def bisect_category_mapping(self, cats):
        return category_mapping(self, cats)

    def group_sequences(self, fu):
        def _group_sequences(self, fu):
            x = [(fu(*x), *x, ini) for ini, x in enumerate(zip(self, self[1:]))]
            firstval = x[0][0]
            co = 0
            resu = defaultdict(list)
            for xx in x:
                if xx[0] != firstval:
                    firstval = xx[0]
                    co = co + 1
                resu[co].append(ProtectedTuple(xx))
            for key in resu:
                if resu[key][0][0]:
                    if len(resu[key]) > 1:
                        resu[key] = ProtectedTuple(resu[key])
            return self.__class__(list(flatten_everything(resu.values())))

        finalres = []

        oldvalue = False
        for ini2, x in enumerate(b := _group_sequences(self, fu)):
            if isinstance(x[0], tuple):
                if x[0][0]:
                    oldvalue = True
                    finalres.append([])
                    for ini, t in enumerate(x):
                        finalres[-1].append(self[t[-1]])
                        if ini + 1 == len(x):
                            finalres[-1].append(self[t[-1] + 1])
            elif x[0]:
                if not oldvalue:
                    finalres.append([])
                    finalres[-1].append(self[x[-1]])
                    finalres[-1].append(self[x[-1] + 1])
                oldvalue = True
            else:
                if not oldvalue:
                    finalres.append([])
                    finalres[-1].append(self[x[-1]])
                elif ini2 + 1 == len(b):
                    finalres.append([])
                    finalres[-1].append(self[x[-1] + 1])
                oldvalue = False

        return finalres

    def groupby_isna(
        self,
        emptyiters: bool = False,
        nastrings: bool = False,
        emptystrings: bool = False,
        emptybytes: bool = False,
        continue_on_exceptions=True,
        withindex=False,
        withvalue=True,
    ):
        return groupBy(
            key=lambda x: is_nan(
                x,
                emptyiters=emptyiters,
                nastrings=nastrings,
                emptystrings=emptystrings,
                emptybytes=emptybytes,
            ),
            seq=self,
            continue_on_exceptions=continue_on_exceptions,
            withindex=withindex,
            withvalue=withvalue,
        )

    def get_iter_list_ljust_rjust(
        self, ljust=0, ljustchr=" ", rjust=0, rjustchr=" ", getmax=True
    ):
        ln = tuple((str(x) for x in self))
        if r1 := isinstance_tolerant(ljust, None) or (
            r2 := isinstance_tolerant(rjust, None)
        ):
            if getmax:
                ma = len(tuple(sorted(ln, key=lambda x: len(x)))[-1])

                if r1:
                    ljust = ma
                try:
                    if r2:
                        rjust = ma
                except Exception:
                    if isinstance_tolerant(rjust, None):
                        rjust = ma
        if rjust != 0:
            ln = iter((x.rjust(rjust, rjustchr) for x in ln))
        if ljust != 0:
            ln = iter((x.ljust(ljust, ljustchr) for x in ln))
        return ln

    def get_iter_log_split(self):
        def logsplit(lst):
            # https://stackoverflow.com/a/35756376/15096247
            iterator = iter(lst)
            for n, e in enumerate(iterator):
                yield itertools.chain([e], itertools.islice(iterator, n))

        for x in logsplit(self):
            yield list(x)

