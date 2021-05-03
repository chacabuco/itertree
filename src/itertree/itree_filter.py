"""
filter classes

we use here lambda to create a method which is feed with an item and delivers then True/False depending on
the given condition so that it can be used in filter iterators
"""
from __future__ import absolute_import
import fnmatch
import operator
from .itree_helpers import *

# List representation of the possible combinations of parameters (for quicker execution)
__FILTER_FACTORY__=[lambda result,item_filter: lambda item: item_filter(item) or result(item), # 0 item_filter=not None, invert=False, use_and=False
                    lambda result,item_filter: lambda item: item_filter(item) or not result(item), # 1 item_filter=not None, invert=True,  use_and=False
                    lambda result,item_filter: lambda item: item_filter(item) and result(item), # 2 item_filter=not None, invert=False, use_and=True
                    lambda result, item_filter: lambda item: item_filter(item) and not result(item), # 3 item_filter=not None, invert=True, use_and=True
                    lambda result,item_filter: lambda item: result(item),# 4 item_filter=None, invert=False, use_and=False
                    lambda result, item_filter: lambda item: not result(item), # 5 item_filter=None,invert=True, use_and=False
                    lambda result, item_filter: lambda item: result(item), # 6 item_filter=None, invert=False, use_and=True
                    lambda result, item_filter: lambda item: not result(item),# 7 item_filter=None, invert=True, use_and=True
                    # use any (iterator results)
                    lambda result, item_filter: lambda item: item_filter(item) or any(result(item)),
                    # 0 item_filter=not None, invert=False, use_and=False
                    lambda result, item_filter: lambda item: item_filter(item) or not any(result(item)),
                    # 1 item_filter=not None, invert=True,  use_and=False
                    lambda result, item_filter: lambda item: item_filter(item) and any(result(item)),
                    # 2 item_filter=not None, invert=False, use_and=True
                    lambda result, item_filter: lambda item: item_filter(item) and not any(result(item)),
                    # 3 item_filter=not None, invert=True, use_and=True
                    lambda result, item_filter: lambda item: any(result(item)),
                    # 4 item_filter=None, invert=False, use_and=False
                    lambda result, item_filter: lambda item: not any(result(item)),
                    # 5 item_filter=None,invert=True, use_and=False
                    lambda result, item_filter: lambda item: any(result(item)),
                    # 6 item_filter=None, invert=False, use_and=True
                    lambda result, item_filter: lambda item: not any(result(item)),
                    # 7 item_filter=None, invert=True, use_and=True

                    ]

__FILTER_DATA_FACTORY__={# In this case we search for values == None:
                         0: lambda item,data_key,data_value:
                            filter(lambda v: v is None,item.data.values()),
                         # key match:
                         0b1: lambda item,data_key,data_value:
                            filter(lambda k: data_key.check(k),item.data.keys()),
                         # key equal:
                         0b10: lambda item, data_key, data_value:
                            filter(lambda k: data_key==k,item.data.keys()),
                         # value match:
                         0b100: lambda item, data_key, data_value: (
                             filter(lambda v: data_value.check(v), item.data.values())),
                         # value equal
                         0b1000: lambda item, data_key, data_value: (
                             filter(lambda v: data_value == v, item.data.values())),
                         # key match and data match
                         0b101: lambda item, data_key, data_value: (
                             filter(lambda i: data_key.check(i[0]) and data_value.check(i[1]), item.data.items())),
                         # key equal and data match
                         0b110: lambda item, data_key, data_value: (
                             filter(lambda i: data_key==i[0] and data_value.check(i[1]), item.data.items())),
                         # key match and data equal
                         0b1001: lambda item, data_key, data_value: (
                             filter(lambda i: data_value==i[1] and data_key.check(i[0]), item.data.items())),
                         # key equal and data equal
                         0b1010: lambda item, data_key, data_value: (
                             filter(lambda i: data_value == i[1] and data_key==i[0], item.data.items())),
                         # or:
                         # In this case we search for values == None -> same as 0
                         10000: lambda item, data_key, data_value:
                            filter(lambda v: v is None, item.data.values()),
                         # key match
                         0b10001: lambda item, data_key, data_value: (
                             filter(lambda i: data_key.check(i[0]) or i[1] is None, item.data.items())),
                         # key equal
                         0b10010: lambda item, data_key, data_value:
                            filter(lambda i: data_key==i[0] or i[1] is None, item.data.items()) ,
                         # value match same as 0b100
                         0b10100: lambda item, data_key, data_value: (
                             filter(lambda v: data_value.check(v), item.data.values())),
                         # value equal same as 0b1000
                         0b11000: lambda item, data_key, data_value: (
                             filter(lambda v: data_value == v, item.data.values())),
                         # key match and data match
                         0b10101: lambda item, data_key, data_value: (
                             filter(lambda i: data_key.check(i[0]) or data_value.check(i[1]), item.data.items())),
                         # key equal and data match
                         0b10110: lambda item, data_key, data_value: (
                             filter(lambda i: data_key == i[0] or data_value.check(i[1]), item.data.items())),
                         # key match and data equal
                         0b11001: lambda item, data_key, data_value: (
                             filter(lambda i: data_value == i[1] or data_key.check(i[0]), item.data.items())),
                         # key equal and data equal
                         0b11010: lambda item, data_key, data_value: (
                             filter(lambda i: data_value == i[1] or data_key == i[0], item.data.items())),
                         }

class iTFilterBase(object):
    def __new__(cls,filter_method,item_filter=None,invert=False,use_and=True,_any=False):
        """
        Base/Super class for all itertree filter classes might be used for user defined filters too

        :param filter_method: method that is fet with an iTree item and that delivers True/False
        :param item_filter: Additional filter to combine with this filter (will always be calculated before this filter!
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        index=int(item_filter is None)<<2 | int(invert) | int(use_and)<<1 |int(_any)<<3
        #print(index)
        return __FILTER_FACTORY__[index](filter_method,item_filter)

class iTFilterTrue(iTFilterBase):

    def __new__(cls,item_filter=None,invert=False,use_and=True):
        """
        This filter might be useless but it delivers True for all items (or False if inverted).

        :param item_filter: Additional filter to combine with this filter (will always be calculated before this filter!
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        return super().__new__(cls,
                               lambda item: True,
                               item_filter,
                               invert,
                               use_and)


class iTFilterItemType(iTFilterBase):

    def __new__(cls,item_type,item_filter=None,invert=False,use_and=True):
        """
        Filter for iTree types (we have iTree,ITreeReadOnly,iTreeTemporary,iTreeLink types)
        :param item_type: target type class
        :param item_filter: Additional filter to combine with this filter (will always be calculated before this filter!
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        return super().__new__(cls,
                               lambda item: type(item)==item_type,
                               item_filter,
                               invert,
                               use_and)

class iTFilterItemTagMatch(iTFilterBase):
    def __new__(cls,match,item_filter=None,invert=False,use_and=True):
        """
        Filter using the iTMatch object (have a look on th iTMatch for more details). In generalyou can
        use wild cards, etc. to find matching item tags
        :param match: iTMatch object that checks the item for a match
        :param item_filter: Additional filter to combine with this filter (will always be calculated before this filter!
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        return super().__new__(cls,
                               lambda item: (match.check(item)),
                               item_filter,
                               invert,
                               use_and)

class iTFilterData(iTFilterBase):
    def __new__(cls,data_key=None,data_value=None,item_filter=None,invert=False,use_and=True):
        """
        This is the main data filter that allows a large number of different filtering based on iTree.data content.
        It's the recommended filter for this proposes because different than the simpler data filters in this module
        we can filter based on combinations (key/value) related to the iTree.data items
        :param data_key: Checks if the given data key exists in item.data in case iTMatch is given matching keys will be considered
                         None - all keys will be considered
        :param data_value: Checks if the given data value exists in item.data in case iTMatch is given matching values
                           will be considered, if iTInterval is given numerical values matching to interval will be considered.
                           None - all values will be considered
        :param item_filter: Additional filter to combine with this filter (will always be calculated before this filter!
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        filter_number=0
        if data_key is not None:
            if type(data_key) is iTMatch:
                filter_number = 0b1
            else:
                # normal key
                filter_number =  0b10
        if data_value is not None:
            t=type(data_value)
            if t is iTMatch or t is iTInterval:
                filter_number = filter_number | 0b100
            else:
                filter_number = filter_number | 0b1000
        if not use_and:
            # or!
            filter_number = filter_number | 0b10000
        # possible numbers (keys) are 0, 0b1, 0b10, 0b100,0b1000, 0b101, 0b110,0b1001,0b1010
        return super().__new__(cls,
                               lambda item: __FILTER_DATA_FACTORY__[filter_number](item,data_key,data_value),
                               item_filter,
                               invert,
                               use_and,_any=True)

# we kept some simpler data filters in the lib but they can all be replaced by the filter iTFilterData

class iTFilterDataKey(iTFilterBase):

    def __new__(cls,data_key,item_filter=None,invert=False,use_and=True):
        """
        Filters in all items for the data key given. Delivers all items that have the given key in there data
        :param data_key: Checks if the given data key exists in item.data
        :param item_filter: Additional filter to combine with this filter (will always be calculated before this filter!
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        return super().__new__(cls,
                               lambda item: (data_key in item.data),
                               item_filter,
                               invert,
                               use_and)

class iTFilterDataKeyMatch(iTFilterBase):

    def __new__(cls,match_pattern,item_filter=None,invert=False,use_and=True):
        """
        Filters in all items for the data key which matches to the given pattern (fnmatch search is used) you can
        use wildcards here.
        This filter works only on string or byte keys in the item.data (not on other objects)
        :param match_pattern: string/bytes that contains a match pattern
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        return super().__new__(cls,
                               lambda item: fnmatch.filter(filter(lambda v: (type(v) is str) or (type(v) is bytes),
                                                           item.data.keys()),match_pattern),
                               item_filter,
                               invert,
                               use_and)

class iTFilterDataKeyMatch(iTFilterBase):

    def __new__(cls,match_pattern,item_filter=None,invert=False,use_and=True):
        """
        Filters in all items for the data key which matches to the given pattern (fnmatch search is used) you can
        use wildcards here.
        This filter works only on string or byte keys in the item.data (not on other objects)
        :param match_pattern: string/bytes that contains a match pattern
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        return super().__new__(cls,
                               lambda item: fnmatch.filter(filter(lambda v: (type(v) is str) or (type(v) is bytes),
                                                           item.data.keys()),match_pattern),
                               item_filter,
                               invert,
                               use_and)

class iTFilterDataValueMatch(iTFilterBase):
    def __new__(cls,match_pattern,item_filter=None,invert=False,use_and=True):
        """
        Filters in all items for containing a matching data value to given pattern. (Works only on string and byte values
        :param match_pattern: pattern fnmatch will search for (you can use wildcards here)
        :param item_filter: Additional filter to combine with this filter (will always be calculated before this filter!
        :param invert: True - invert the result of the filter (not)
                       False (default) - result of filter is kept unchanged
        :param use_and: True (default) - combine this filter with item_filter via and operator
                        False - use or operator instead of and
        """
        return super().__new__(cls,
                               lambda item: fnmatch.filter(filter(lambda v: (type(v) is str) or (type(v) is bytes),
                                                           item.data.values()),match_pattern),
                           item_filter,
                           invert,
                           use_and)


