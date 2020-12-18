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
_ddl_fld_ln_ptn = r"(?P<tb_fld_ln>\t\"?(?P<fld_nm>[a-zA-Z]*)\"?\s(?P<fld_typ>\w+(\(\d+\))?)\s*(?P<fld_other>(?P<fld_n_nul>(NOT)?\s?NULL)?).*)"
# 建表内容 - key
_ddl_key_ln_ptn = r"(?P<tb_key_ln>\tCONSTRAINT \"?(?P<tb_key_nm>[a-zA-Z_]+)\"? PRIMARY KEY \((?P<tb_key_fld>.*)\))"

# 建表结束 - 最后一行
_ddl_end_ln_ptn = r"(?P<end_ln>\);.*)"

# # DDL语句 - 完整解析 <无法正常使用!>
# _ddl_tb_ptn = r"(?P<crt_tb>{_s}|(({_fld}|{_key})*)|{_end})".format(
#     _s=_ddl_start_ln_ptn,
#     _fld=_ddl_fld_ln_ptn,
#     _key=_ddl_key_ln_ptn,
#     _end=_ddl_end_ln_ptn)

# ------------------------------------------------------------------------------


class DdlParse(main.IParser):
    def convertor_logic(self, in_str: str):
        ss = in_str
        data = []  # ddl list
        # 逻辑
        r_list = re.findall(r"(CREATE.*)|(\tCONSTRAINT.*)|(\t.*)|(\);)", ss)
        meta_map = {}
        for r in r_list:
            if r[0] != "": # 匹配 CREATE行
                ddl = r[0]
                meta_map["schema"] = re.search(
                    _ddl_start_ln_ptn, ddl).group('tb_schema')
                meta_map["table"] = re.search(
                    _ddl_start_ln_ptn, ddl).group('tb_nm')
            elif r[1] != "":
                ddl = r[1] # 匹配 key行
                if meta_map.get("primary") is None:
                    meta_map["primary"] = {}
                meta_map["primary"]["field"] = re.sub(
                    _ddl_key_ln_ptn, "\\g<tb_key_fld>", ddl)
                meta_map["primary"]["name"] = re.sub(
                    _ddl_key_ln_ptn, "\\g<tb_key_nm>", ddl)
            elif r[2] != "":
                ddl = r[2] # 匹配 字段行
                fld = {}
                fld["field"] = re.search(_ddl_fld_ln_ptn, ddl).group('fld_nm')
                fld["type"] = re.sub(_ddl_fld_ln_ptn, "\\g<fld_typ>", ddl)
                if meta_map.get("fields") is None:
                    meta_map["fields"] = []
                meta_map["fields"].append(fld)
            elif r[3] != "": # 匹配 结尾);
                print(meta_map)
                data.append(meta_map)
                meta_map = {}
        return json.dumps(data)


if __name__ == '__main__':
    DdlParse("test/test_file/t_ddl.sql", output_nm="_parse/otp").run()
    # DdlParse("_inputs/wms_ddl.sql", output_nm="_parse/otp").run()
    pass
