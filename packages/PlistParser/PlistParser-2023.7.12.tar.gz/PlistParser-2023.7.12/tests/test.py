"""
py 代码 格式化 https://stackoverflow.org.cn/formatpy/
"""
from PlistParser.Plist import Plist
from PlistParser.PlistParser import PlistParser
from PlistParser.Base64 import Base64

if __name__ == '__main__':
    plist = r'plist/com.apple.MobileGestalt.plist'
    out_plist = r'plist/example.plist'

    plist_parser = PlistParser()
    plist_value = plist_parser.parser_dict(plist)
    print(plist_value)
    plist_value = plist_parser.parser_plist(plist_value, out_plist)
    print(plist_value)
    data = plist_parser.customization_parser_dict_value(~Plist().CacheExtra.device_model, 'abbbcd')
    print(data)

    print(+Plist().CacheExtra.device_model)
    print(+Plist().CacheExtra.device_category)
    print(+Plist().CacheExtra.device_issuance)
    print(+Plist().CacheExtra.device_system)
    print(-Plist().CacheExtra.device_model)
    print(~Plist().CacheExtra.device_model)

    plist_value = plist_parser.parser_plist(out_file='plist/example.plist')

    data = plist_parser.device_model()
    print(data)
    data = plist_parser.device_category()
    print(data)
    data = plist_parser.device_issuance()
    print(data)
    data = plist_parser.device_system()
    print(data)

    print(+Plist().CacheExtra.device_model)

    data = {
        ~Plist().CacheUUID: None,
        ~Plist().CacheExtra.device_category: None,
        ~Plist().CacheExtra.device_issuance: None,
    }
    print(data)
    data = plist_parser.plist_dict_to_cust_dict(data)
    print(data)

    data = plist_parser.customization_parser_dict_values(data)
    print(data)
    print(plist_parser.customization_parser_dict_value(~Plist().CacheExtra.device_issuance))
    print(plist_parser.plist_dict)

    data = {
        Base64.Decode.bit64: {},
    }
    data = plist_parser.parser_base64(b'YWRtaW4=', data)
    print(data)

