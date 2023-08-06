#!/usr/bin/python3
# -*- coding: utf-8 -*-


class PlistItem:
    def __init__(self, item_index_tuple, item, item_index_head=''):
        """

        :param item_index_tuple:
        :param item: 当前节点在 .plist 中的名称 (key值)
        :param item_index_head: 当前节点的 前缀头数据 在  __pos__ __neg__ __invert__ 中引用拼接 节点路径前缀
        """
        self.item_index_tuple = item_index_tuple
        self.item = item
        self.item_index_head = item_index_head

    def __pos__(self):
        self_item_index = self.item_index_head
        for item in self.item_index_tuple:
            self_item_index = f'{self_item_index}["{item}"]' if self_item_index else f'["{item}"]'
        return f'{self_item_index}["{self.item}"]' if self_item_index else f'["{self.item}"]'

    def __neg__(self):
        self_item_index = self.item_index_head
        for item in self.item_index_tuple:
            self_item_index = f'{self_item_index}.{item}' if self_item_index else f'{item}'
        return f'{self_item_index}.{self.item}' if self_item_index else self.item

    def __invert__(self):
        return self.item_index_tuple + (self.item,)
class PlistCacheExtraItem(PlistItem):
    pass
class PlistCacheExtra(PlistItem):
    def __init__(self, item_index_tuple, item, item_index_head=''):
        super().__init__(item_index_tuple, item, item_index_head)
        self.device_category = PlistCacheExtraItem(item_index_tuple, 'VuGdqp8UBpi9vPWHlPluVQ',
                                                   item_index_head)  #: ['iPhone15,3'],
        self.device_issuance = PlistCacheExtraItem(item_index_tuple, 'zHeENZu+wbg7PUprwNwBWg',
                                                   item_index_head)  # : 'CH/A',
        self.device_model = PlistCacheExtraItem(item_index_tuple, 'Z/dqyWS6OZTRy10UcmUAhw',
                                                item_index_head)  # : 'iPhone14 Pro Max',
        self.device_system = PlistCacheExtraItem(item_index_tuple, 'ivIu8YTDnBSrYv/SN4G8Ag',
                                                 item_index_head)  # : 'iPhone OS',
class Plist(PlistItem):
    def __init__(self, item_index_tuple=None, item='Plist', item_index_head=''):
        super().__init__(item_index_tuple, item, item_index_head)
        item_index_tuple = () if item_index_tuple == None else item_index_tuple
        self.CacheUUID = PlistItem(item_index_tuple, 'CacheUUID')
        self.CacheData = PlistItem(item_index_tuple, 'CacheData')
        self.CacheVersion = PlistItem(item_index_tuple, 'CacheVersion')
        self.CacheExtra = PlistCacheExtra(('CacheExtra',), 'CacheExtra')

