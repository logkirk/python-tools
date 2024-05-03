from dataclasses import asdict
from random import randint, shuffle


def get_random_item_from_list(list_, exclusions=None):
    """Returns a randomly selected item from the list, optionally excluding certain
    items.

    Args:
        list_ (list): list to get item from
        exclusions (list): values to exclude (will not choose these values)

    Returns:
        randomly selected item from list_
    """
    if exclusions is not None:
        list_ = [i for i in list_ if i not in exclusions]

    return list_[randint(0, len(list_) - 1)]


def shuffle_string(to_shuffle):
    """Shuffles space-separated words in a string."""
    to_shuffle = to_shuffle.split(" ")
    shuffle(to_shuffle)
    return " ".join(to_shuffle)


def strip_none_values_from_dataclass(dataclass_):
    """Returns the provided dataclass as a dict with None values removed."""
    return asdict(
        dataclass_, dict_factory=lambda x: {k: v for k, v in x if v is not None}
    )
