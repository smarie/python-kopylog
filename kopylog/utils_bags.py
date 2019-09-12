#  Authors: Sylvain Marie <sylvain.marie@se.com>
#
#  License: BSD 3 clause
import sys

if sys.version_info < (3, 7):
    from collections import OrderedDict as ODict
else:
    ODict = dict

from six import raise_from

try:  # python 3.5+
    from typing import Iterable, Tuple, Any, Mapping
except ImportError:
    pass


class OrderedMunch(object):
    """
    A simple 'Munch', that is, a dual object/dict.
    It is hashable with a not very interesting hash, but at least a unique one in a python session (id(self)).

    See other similar projects: Bunch/Munch/addict/Box
    """

    __slots__ = 'odict',

    def __init__(self,
                 initial_pairs=None,  # type: Iterable[Tuple[str, Any]]
                 initial_dict=None,   # type: Mapping[str, Any]
                 *args,               # type: Tuple[str, Any]
                 **kwargs             # type: Any
                 ):
        """
        Constructor with optional initial entries. One can provide the initial entries as:

         - a list of pairs in `initial_pairs` or in *args
         - a mapping in `initial_dict` or **kwargs

        Only one initialization method should be used, otherwise a `ValueError`will be raised.

        Unfortunately with python 3.5 and lower, **kwargs loses information that's why users interested in
        portability will prefer to use this `initial_dict` argument.
        See https://www.python.org/dev/peps/pep-0468/

        :param initial_pairs:
        :param initial_dict:
        :param args: an optional initial list of key-value pairs. The order will be preserved
        :param kwargs: an optional initial list of key-value pairs. The order will be preserved IF the python version
        """
        # An internal dictionary to store all other information.
        # - self will be a proxy of this dictionary through MappingProxyMixIn
        # - getting, setting and deleting attributes on the object will interact with that dict through MunchMixIn
        self.set_attrs(odict=ODict())  # PrintableOrderedDict()

        # check that only a single way is used to initialize the dict
        nb_provided = (initial_pairs is not None) + (initial_dict is not None) + (len(args) > 0) + (len(kwargs) > 0)
        if nb_provided > 1:
            raise ValueError("only one of `initial_pairs`, `initial_dict`, `*args` or `**kwargs` should be provided")

        # initialize
        if initial_pairs is not None:
            self.odict.update(initial_pairs)
        elif len(args) > 0:
            self.odict.update(args)
        elif initial_dict is not None:
            self.odict.update(initial_dict.items())
        elif len(kwargs) > 0:
            self.odict.update(**kwargs)

    def set_attrs(self, **kwargs):
        """Actually sets the attr on the object (rather than inserting a value in the odict)"""
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)

    # object
    def __setattr__(self, key, value):
        # try:  No exception can happen: key is always a string, and new entries are allowed in a dict
        self.odict[key] = value
        # except KeyError as e:
        #     raise_from(AttributeError(key), e)

    def __getattr__(self, key):
        try:
            # print(key)
            return self.odict[key]
        except KeyError as e:
            raise_from(AttributeError(key), e)

    def __delattr__(self, key):
        try:
            del self.odict[key]
        except KeyError as e:
            raise_from(AttributeError(key), e)

    # object base
    def __str__(self):
        return dict.__str__(self.odict)

    def __repr__(self):
        return "%s:\n%s" % (self.__class__.__name__, dict.__repr__(self.odict))

    def __hash__(self):
        """Make the type hashable with a fake hash: python object id"""
        return id(self)
