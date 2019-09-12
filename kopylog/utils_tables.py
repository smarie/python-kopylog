#  Authors: Sylvain Marie <sylvain.marie@se.com>
#
#  License: BSD 3 clause

from collections import OrderedDict

from kopylog.utils_bags import ODict

try:  # python 3.5+
    from typing import Any
    ValueType = Any
#     from typing import Generic, TypeVar
# 
#     IdType = TypeVar('IdType')
#     """ The type of the id in an Entry """
# 
#     ValueType = TypeVar('ValueType')
#     """ The type of an Entry """
# 
#     tt_root = Generic[IdType, ValueType]
# 
except:
#     tt_root = object
    pass


class TypedTable(object):  # TODO maybe one day inherit OrderedMunch
    """
    An ordered key-value container of entries (= and OrderedDict)
    where 
     - the key is a field of the entry (so the entries "know" their id).
     - the type of the entry is known and can optionally be enforced


    This makes us able to provide to_df() and from_df() methods at the container level.
    """
    __slots__ = ('odict', 'value_type', 'key_name')

    def __init__(self,
                 value_type,    # type: Any
                 key_name       # type: str
                 ):
        """

        :param value_type:
        :param key_name:
        """
        self.odict = ODict()
        self.value_type = value_type
        self.key_name = key_name

    def append(self,
               entry  # type: ValueType
               ):
        """
        Adds an entry to this container, using its id

        :param entry:
        :return:
        """
        self.odict[getattr(entry, self.key_name)] = entry

    def __str__(self):
        # since all entries have their id in their str representation, do not display the keys(), only values() ?
        return "{cn} - {dct}".format(cn=type(self).__name__, dct=list(self.odict.values()))

    # ------ MappingProxyMixIn implementation

    # def get_internal_mapping(self):
    #     # type: (...) -> MutableMapping[IdType, ValueType]
    #     return self.odict
    #
    # def validate_value(self,
    #                    key,  # type: IdType
    #                    value,  # type: ValueType
    #                    **kwargs):
    #     if key != value.get_id():
    #         raise ValueError("Entries must be added with a key equal to their id. {} != {}".format(key, value.get_id()))

    # --------- BuildableFromDict/ConvertibleToDict implementation

    # def to_dict(self, deep: bool = True, **kwargs) -> Dict[str, Any]:
    #     """
    #     Transforms an entry container to a dictionary. By default deep=True: all entries are transformed to
    #     dictionaries as well. Turning deep=False will return PrintableOrderedDict(self)
    #
    #     :param kwargs:
    #     :return:
    #     """
    #     if deep:
    #         dct = PrintableOrderedDict()
    #         for id, entry in self.get_internal_mapping().items():
    #             dct[id] = entry.to_dict(**kwargs)
    #         return dct
    #     else:
    #         # return a dict copy of self
    #         return PrintableOrderedDict(self)
    #
    # @classmethod
    # def from_dict(cls: 'Type[ContainerType]', dct, **kwargs) -> ContainerType:
    #     """
    #     Builds an entry container from a dictionary of entries.
    #     Each entry may be either of the right type (the one from this classes' cls.values_type())
    #     Or it may be a dict. In which case cls.values_type().from_dict(entry, **kwargs) will be called.
    #
    #     :param dct:
    #     :param kwargs:
    #     :return:
    #     """
    #     # noinspection PyCallingNonCallable
    #     new_instance = cls()
    #     entry_type = cls.values_type()
    #
    #     if issubclass(entry_type, BuildableFromDict):
    #         # we potentially have to decode each entry, by convenience
    #         for entry_id in dct.keys():
    #             entry = dct[entry_id]
    #             if isinstance(entry, entry_type):
    #                 # Already of the correct type: keep it
    #                 new_instance.odict[entry_id] = entry
    #             elif isinstance(entry, Mapping):
    #                 # build from dict
    #                 new_instance.odict[entry_id] = entry_type.from_dict(entry, **kwargs)
    #             else:
    #                 raise ValueError("Cannot restore entry '{}' of desired type {} from received value {}"
    #                                  "".format(entry_id, entry_type, entry))
    #
    #     return new_instance


# class TypedTableField(TypedTable):
#     """
#     Implements the descriptor protocol over a typed table
#     """
#     def __get__(self, obj, objtype):
#         return self
#
#     def __set__(self, obj, value):
#         raise AttributeError('This attribute is frozen.')
#
#     def __delete__(self, obj):
#         raise AttributeError('This attribute is frozen.')
