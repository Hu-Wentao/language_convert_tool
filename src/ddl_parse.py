import main
import re
import json
# -----------------------------------------------------------------------------
# pattern, 这里只适配 通过DBeaver 生成的DDL语句
# - 缩进使用一个 \t
# - 字段名不用或用"" 包裹

# 建表开始 - 第一行
_ddl_start_ln_ptn = r"(?P<start_ln>CREATE TABLE\s+((?P<tb_schema>[a-zA-Z_]+)\.)?(?P<tb_nm>[a-zA-Z_]+)\s+\(.*)"

# 建表内容 - 字段
_ddl_fld_ln_ptn = r"(?P<tb_fld_ln>\n\t(?P<fld_nm>[\"a-zA-Z]*)\s(?P<fld_typ>\w+(\(\d+\))?)\s*(?P<fld_other>(?P<fld_n_nul>(NOT)?\s?NULL)?).*)"
# 建表内容 - key
_ddl_key_ln_ptn = r"(?P<tb_key_ln>\n\tCONSTRAINT (?P<tb_key_nm>.*))"
# _ddl_key_ln_ptn = r"(?P<tb_key_ln>\n\tCONSTRAINT (?P<tb_key_nm>[\"a-zA-Z]*) PRIMARY KEY \((?P<tb_key_fld>.*)\).*)"

# 建表结束 - 最后一行
_ddl_end_ln_ptn = r"(?P<end_ln>\n\);.*)"


# DDL语句 - 完整解析 <无法正常使用!>
# _ddl_tb_ptn = r"(?P<crt_tb>{_s}(({_fld}|{_key})*){_end})".format(
#     _s=_ddl_start_ln_ptn,
#     _fld=_ddl_fld_ln_ptn,
#     _key=_ddl_key_ln_ptn,
#     _end=_ddl_end_ln_ptn)


# ------------------------------------------------------------------------------


def _pretreatment(ss: str) -> str:
    """
    预处理, 这里将会移除无法帮助regex定位的行和字符, 而可以帮助定位但不需要的字符将在 最终处理中移除
    移除 /**/ 和 -- 注释, 
    """
    ss = re.sub(r"/\*.*(\n.*)+\*/", "", ss)
    ss = re.sub(r"--.*", "", ss)
    # 移除多余的 \n
    # ss = re.sub(r"\n*{}\n+".format(_ddl_tb_ptn), r"\g<1>", ss)
    return ss

def proc_on_ddl(ddl):
    """
    [
        {
            "schema":"xxx 模式名",
            "table":"xxx 表名",
            "fields":[
                {"field":"xxx 字段名", "type":"xxx 字段类型"},
            ],
            "primary":{"field":"xxx 主键字段", "name":"xxx 主键名"},
        },
    ]
    """
    print("#######\n",ddl)
    _schema = re.search(_ddl_start_ln_ptn,ddl).group('tb_schema')
    if _schema is None:
        _schema = ""
    _table = re.search(_ddl_start_ln_ptn,ddl).group('tb_nm')
    
    # _fld_nm = re.sub(_ddl_fld_ln_ptn,"\\g<fld_nm>",ddl)
    # _fld_typ = re.sub(_ddl_fld_ln_ptn,"\\g<fld_typ>",ddl)

    # _prm_nm = re.sub(_ddl_key_ln_ptn,"\\g<tb_key_nm>",ddl)
    # _prm_nm = re.search(_ddl_key_ln_ptn,ddl).group('tb_key_ln')
    # _prm_fld = re.sub(_ddl_key_ln_ptn,"\\g<tb_key_fld>",ddl)


    data ={
        "schema":_schema,
        "table":_table,
        "fields":[
            {"field":"tst#", "type":"tst##"}
        ],
        "primary":{"field":'_prm_fld', "name":'_prm_nm'}
    }
    # print(data)
    return json.dumps(data)

# ------------------------------------------------------------------------------


class DdlParse(main.IParser):
    def convertor_logic(self, in_str: str):
        ss = in_str
        # ss = _pretreatment(ss)
        # 逻辑

        ## 匹配整个DDL
        all_dlls = re.findall(re.compile(r"(\nCREATE TABLE.*)((\n\t.*)*)\n\);.*"), ss)
        # all_dlls = re.findall(r'\nCREATE TABLE.*(\n\t.*)+\n\);', ss)
        # print(all_dlls)
        r=''
        for ddl in all_dlls:
            r += proc_on_ddl(str(ddl))+","

        # ss = re.sub(r'\nCREATE TABLE.*(\n\t.*)+\n\);.*', proc_on_ddl(), ss)
        # ss = re.sub(_ddl_start_ln_ptn, "##\\g<tb_schema>\n", ss)
        # ss = re.sub(_ddl_fld_ln_ptn, "## 字段[\\g<fld_nm>]类型[\\g<fld_typ>]\n", ss)
        # ss = re.sub(_ddl_key_ln_ptn, "\n## key名[\\g<tb_key_nm>] 字段[\\g<tb_key_fld>]\n", ss) 
        # ss = re.sub(_ddl_end_ln_ptn, "##\n", ss) 

        # 收尾

        # print(ss)
        return r
        pass


if __name__ == '__main__':
    DdlParse("_inputs/wms_ddl.sql", output_nm="_parse/otp").run()
    pass
