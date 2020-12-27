import re


def underscore2upper_camel(nm: str) -> str:
    """
    小写下划线 转 大驼峰
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

    res = res[0].upper() + res[1:]
    if nm.startswith('_'):
        res = "_" + res
    return res


def upper_camel2underscore(text):
    """
    大驼峰 转 小写下划线
    """
    lst = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()


def low2upper_camel(text: str) -> str:
    """
    小驼峰转大驼峰
    :param text:
    :return:
    """
    return text[:1].upper()+text[1:]


if __name__ == "__main__":
    # print(underscore2upper_camel('wms_asdf'))
    # print(underscore2upper_camel('_wms_asdf'))
    # print(underscore2upper_camel('__wms_asdf'))
    print(upper_camel2underscore("AbcAA"))
