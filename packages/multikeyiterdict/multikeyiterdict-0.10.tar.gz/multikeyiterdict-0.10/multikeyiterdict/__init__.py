from itertools import takewhile

from dict_merger_keep_all import dict_merger
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from mymulti_key_dict import (
    MultiKeyDict,
    convert_to_normal_dict_simple,
    convert_to_default_dict,
)
from isiter import isiter


class MultiKeyIterDict(MultiKeyDict):
    """A dictionary implementation that supports multiple keys for nested lookups."""

    def __init__(self, /, initialdata=None, **kwargs):
        """
        Initialize the MultiKeyIterDict.

        Args:
            initialdata: Initial data to populate the dictionary. Default is None.
            **kwargs: Additional key-value pairs to populate the dictionary.
        """
        super().__init__(initialdata, **kwargs)


    def nested_items(self):
        """
        Generate nested items in the dictionary.

        Yields:
            Tuple: A tuple containing the nested key and value.
        """
        for v, k in fla_tu(self.data):
            yield list(k), v

    def nested_values(self):
        """
        Generate nested values in the dictionary.

        Yields:
            Any: The nested value.
        """
        for v, k in fla_tu(self.data):
            yield v

    def nested_keys(self):
        """
        Generate nested keys in the dictionary.

        Yields:
            List: The nested key.
        """
        for v, k in fla_tu(self.data):
            yield list(k)

    def _check_last_item(self):
        """
        Check the last item in the nested dictionary.

        Yields:
            Tuple: A tuple containing the key and value of the last item.
        """
        alreadydone = []
        for v, k in fla_tu(self.data):
            if len(k) > 1 and k not in alreadydone:
                qr=list(k)[:-1]
                if isiter(v := self[qr]):
                    k = qr
                    alreadydone.append(k)
                    yield k, v
            else:
                yield list(k), v

    def nested_value_search(self, value):
        """
        Search for nested keys based on the given value.

        Args:
            value: The value to search for.

        Yields:
            List: The nested key(s) corresponding to the given value.
        """
        for k, v in self._check_last_item():
            if v == value:
                yield k

    def nested_key_search(self, key):
        """
        Search for nested keys based on the given key.

        Args:
            key: The key to search for.

        Yields:
            Tuple: A tuple containing the nested key and the corresponding value.
        """
        return (
            (q := list(takewhile(lambda xx: xx != key, list(x))) + [key], self[q])
            for x in list(self.nested_keys())
            if key in x
        )

    def nested_update(self, *args):
        """
        Update the dictionary with nested key-value pairs.

        Args:
            *args: One or more dictionaries to update the current dictionary.

        Note:
            This method modifies the current dictionary in-place.
        """
        self.data = convert_to_default_dict(dict_merger(self.to_dict(), *args))

    def nested_merge(self, *args):
        """
        Merge the dictionary with nested key-value pairs.

        Args:
            *args: One or more dictionaries to merge with the current dictionary.

        Returns:
            dict: The merged dictionary.
        """
        return convert_to_normal_dict_simple(dict_merger(self.to_dict(), *args))

