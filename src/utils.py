import re

def underscore2upper_camel(nm: str)-> str:
    """
    小写下划线 转 小驼峰
    """
    arr = filter(None, nm.lower().split('_'))
    res = ''
    j = 0
    for i in arr:
        if j == 0:
            res = i
        else:
            res = res + i[0].upper() + i[1:]
        j += 1
    
    res = res[0].upper()+res[1:]
    if nm.startswith('_'):
        res = "_"+res
    return res

# def uncamelize( camelCaps, separator="_"):
#     """
#     驼峰转下划线
#     """
#     pattern = re.compile(r'([A-Z]{1})')
#     sub = re.sub(pattern, separator+r'\1', camelCaps).lower()
#     return sub

if __name__ == "__main__":
    print(underscore2upper_camel('wms_asdf'))
    print(underscore2upper_camel('_wms_asdf'))
    print(underscore2upper_camel('__wms_asdf'))
