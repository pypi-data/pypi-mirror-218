import operator
import sys
from types import GeneratorType

from isiter import isiter
from tolerant_isinstance import isinstance_tolerant


def level_flatten(
    iterable, n=sys.maxsize, dict_treatment="items", consider_non_iter=(str, bytes)
):
    """
        Perform a level-wise flattening of an iterable.

        Args:
            iterable (iterable): The input iterable to be flattened.
            n (int, optional): The maximum number of levels to flatten. Defaults to sys.maxsize.
            dict_treatment (str, optional): Treatment for dictionaries. Can be one of "items",
                "keys", or "values". Defaults to "items".
            consider_non_iter (tuple or list, optional): Tuple or list of data types to be
                considered non-iterable and flattened as individual elements. Defaults to
                (str, bytes).

        Returns:
            list: A flattened list containing the elements from the input iterable.

        Examples:
            import numpy as np
            from collections import defaultdict

            d = defaultdict(list)
            d[1].append((1, 2, 3, [44, 5, 5]))
            iti = [
                {(1, 2), (3, 4)},
                ["a", 111, 3],
                (1, 2),
                d,
                "stristristri",
                range(100, 110),
                455j,
                b"xxxxaaa",
                frozenset({1, 2, 3, 4}),
                [
                    11,
                    [
                        222,
                        33,
                        4,
                        (333, 4, {1, 2, 3, 4}, {3333: 333}, [33312, 33323], bytearray(b"xxxxx")),
                    ],
                ],
                [
                    {2: 3},
                    (
                        2,
                        3,
                        4,
                    ),
                    ["babab", "dd", {10: 12}, (("bbb", 12), [333, 4, {4: 32}])],
                ],
                (1.2, 11, 1232),
                bytearray(b"xxxxx"),
                np.array([1, 2, 3, 4, 5]),
                [None, np.nan],
                [[True, False, True]],
            ]

            t1 = level_flatten(
                iti,
                n=1,
                dict_treatment="items",
                consider_non_iter=(str, bytes, frozenset, bytearray),
            )
            print(t1)
            # [(1, 2), (3, 4), 'a', 111, 3, 1, 2, (1, [(1, 2, 3, [44, 5, 5])]), 'stristristri', 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 455j, b'xxxxaaa', frozenset({1, 2, 3, 4}), 11, [222, 33, 4, (333, 4, {1, 2, 3, 4}, {3333: 333}, [33312, 33323], bytearray(b'xxxxx'))], {2: 3}, (2, 3, 4), ['babab', 'dd', {10: 12}, (('bbb', 12), [333, 4, {4: 32}])], 1.2, 11, 1232, bytearray(b'xxxxx'), 1, 2, 3, 4, 5, None, nan, [True, False, True]]

            t1 = level_flatten(
                iti, n=2, dict_treatment="values", consider_non_iter=(str, bytes, dict)
            )
            print(t1)
            # [1, 2, 3, 4, 'a', 111, 3, 1, 2, (1, 2, 3, [44, 5, 5]), 'stristristri', 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 455j, b'xxxxaaa', 1, 2, 3, 4, 11, 222, 33, 4, (333, 4, {1, 2, 3, 4}, {3333: 333}, [33312, 33323], bytearray(b'xxxxx')), {2: 3}, 2, 3, 4, 'babab', 'dd', {10: 12}, (('bbb', 12), [333, 4, {4: 32}]), 1.2, 11, 1232, 120, 120, 120, 120, 120, 1, 2, 3, 4, 5, None, nan, True, False, True]


            t1 = level_flatten(
                iti, n=3, dict_treatment="keys", consider_non_iter=(str, bytes, set, tuple)
            )
            print(t1)
            # [{(1, 2), (3, 4)}, 'a', 111, 3, (1, 2), 1, 'stristristri', 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 455j, b'xxxxaaa', 1, 2, 3, 4, 11, 222, 33, 4, (333, 4, {1, 2, 3, 4}, {3333: 333}, [33312, 33323], bytearray(b'xxxxx')), 2, (2, 3, 4), 'babab', 'dd', 10, (('bbb', 12), [333, 4, {4: 32}]), (1.2, 11, 1232), 120, 120, 120, 120, 120, 1, 2, 3, 4, 5, None, nan, True, False, True]


            t1 = level_flatten(
                iti,
                n=4,
                dict_treatment="items",
                consider_non_iter=(str, bytes, set, tuple, dict, bytearray),
            )
            print(t1)
            # [{(1, 2), (3, 4)}, 'a', 111, 3, (1, 2), (1, [(1, 2, 3, [44, 5, 5])]), 'stristristri', 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 455j, b'xxxxaaa', 1, 2, 3, 4, 11, 222, 33, 4, (333, 4, {1, 2, 3, 4}, {3333: 333}, [33312, 33323], bytearray(b'xxxxx')), {2: 3}, (2, 3, 4), 'babab', 'dd', {10: 12}, (('bbb', 12), [333, 4, {4: 32}]), (1.2, 11, 1232), bytearray(b'xxxxx'), 1, 2, 3, 4, 5, None, nan, True, False, True]


            t1 = level_flatten(
                iti, n=sys.maxsize, dict_treatment="items", consider_non_iter=(np.array, np.ndarray)
            )
            print(t1)
            # [1, 2, 3, 4, 'a', 111, 3, 1, 2, 1, 1, 2, 3, 44, 5, 5, 's', 't', 'r', 'i', 's', 't', 'r', 'i', 's', 't', 'r', 'i', 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 455j, 120, 120, 120, 120, 97, 97, 97, 1, 2, 3, 4, 11, 222, 33, 4, 333, 4, 1, 2, 3, 4, 3333, 333, 33312, 33323, 120, 120, 120, 120, 120, 2, 3, 2, 3, 4, 'b', 'a', 'b', 'a', 'b', 'd', 'd', 10, 12, 'b', 'b', 'b', 12, 333, 4, 4, 32, 1.2, 11, 1232, 120, 120, 120, 120, 120, array([1, 2, 3, 4, 5]), None, nan, True, False, True]

    """

    def reducen(function, sequence):
        if (
            hasattr(sequence, "keys")
            and hasattr(sequence, "items")
            and hasattr(sequence, "values")
        ):
            sequence = [sequence]
        if not isinstance_tolerant(sequence, GeneratorType):
            it = iter(sequence)
        else:
            it = sequence
        value = []
        for element in it:
            try:
                if isiter(element, consider_non_iter=consider_non_iter):
                    if (
                        hasattr(element, "keys")
                        and hasattr(element, "items")
                        and hasattr(element, "values")
                    ):
                        element = [
                            x
                            if dict_treatment == "items"
                            else x[0]
                            if dict_treatment == "keys"
                            else x[1]
                            for x in element.items()
                        ]

                    try:
                        if isinstance_tolerant(element, list):
                            value = function(value, element)
                        else:
                            value = function(value, list(element))
                    except Exception:
                        value = function(value, [element])
                else:
                    value = function(value, [element])
            except Exception:
                value = function(value, [element])
        return value

    old = iterable
    for _ in range(n):
        iterable = reducen(function=operator.add, sequence=iterable)
        if iterable == old:
            break
        else:
            old = iterable
    return iterable
