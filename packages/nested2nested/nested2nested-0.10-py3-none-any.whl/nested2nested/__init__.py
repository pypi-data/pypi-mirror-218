from flatten_any_dict_iterable_or_whatsoever import fla_tu
from multikeyiterdict import MultiKeyIterDict


def nested_list_to_nested_dict(l):
    """
    Convert a nested list into a nested dictionary.

    Args:
        l (list): The nested list to be converted.

    Returns:
        dict: A nested dictionary representing the input nested list.

    Examples:
        from nested2nested import nested_list_to_nested_dict
        >>> d = nested_list_to_nested_dict(l=[33,4,['baba',4,['babx',[[4,4,5,2],4],4,32],4,3],423])
        >>> print(d)
        {
            0: 33,
            1: 4,
            2: {
                0: 'baba',
                1: 4,
                2: {
                    0: 'babx',
                    1: {
                        0: {
                            0: 4,
                            1: 4,
                            2: 5,
                            3: 2
                        },
                        1: 4
                    },
                    2: 4,
                    3: 32
                },
                3: 4,
                4: 3
            },
            3: 423
        }
    """
    di = MultiKeyIterDict()
    for v, k in fla_tu(l):
        di[list(k)] = v
    return di.to_dict()
