""" shimport.abc
"""

import itertools

from shimport.util import typing


# FIXME: move to fleks?
class FilterResult(typing.List[typing.Any]):
    """ """

    def map(self, fxn, logger: object = None):
        """

        :param fxn: param logger: object:  (Default value = None)
        :param logger: object:  (Default value = None)

        """
        return FilterResult(list(map(fxn, self)))

    def starmap(self, fxn, logger: object = None):
        """

        :param fxn: param logger: object:  (Default value = None)
        :param logger: object:  (Default value = None)

        """
        return FilterResult(list(itertools.starmap(fxn, self)))

    def prune(self, **kwargs):
        """

        :param **kwargs:

        """
        return FilterResult(filter(None, [x.prune(**kwargs) for x in self]))

    def filter(self, **kwargs):
        """

        :param **kwargs:

        """
        return FilterResult([x.filter(**kwargs) for x in self])

    def __str__(self):
        return "<{self.__class__.__name__}>"

    __repr__ = __str__
