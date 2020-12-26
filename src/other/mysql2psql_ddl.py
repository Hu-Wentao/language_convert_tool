# MySQL建表语句转 PostgreSQL DDL

import re  # 导入正则表达式包
import datetime
import main


# -----------------------------------------------------------------------------
# pattern

# 建表开始 - 第一行
_msq_crt_tb_start_ln_ptn = r"(?P<start_ln>CREATE TABLE\s*`(?P<tb_nm>.*)`\s*\(.*)"

# 建表内容 - 字段
_msq_crt_tb_fld_ln_ptn = r"(?P<tb_fld_ln>\n\s+`(?P<fld_nm>.*)`\s+(?P<fld_typ>\w+(\(\d+\))?)\s*(?P<fld_other>(?P<fld_n_nul>(NOT)?\s?NULL)?).*)"
# 建表内容 - key
_msq_crt_tb_key_ln_ptn = r"(?P<tb_key_ln>\n\s+PRIMARY KEY \(`(?P<tb_key_fld>.*)`\).*)"

# 建表结束 - 最后一行
_msq_crt_tb_end_ln_ptn = r"(?P<end_ln>\n\)\s*ENGINE.*)"

# 建表语句 - 完整解析
_msq_crt_tb_ptn = r"(?P<crt_tb>{_s}(({_fld}|{_key})*){_end})".format(
    _s=_msq_crt_tb_start_ln_ptn,
    _fld=_msq_crt_tb_fld_ln_ptn,
    _key=_msq_crt_tb_key_ln_ptn,
    _end=_msq_crt_tb_end_ln_ptn)

# ------------------------------------------------------------------------------


class Mysql2PsqlDdlConverter(main.IConvertor):
    """
    proc_on_head_ln:
    proc_on_fld_ln: 处理MySQL建表的 字段行 [_msq_crt_tb_fld_ln_ptn]
    proc_on_key_ln: 
    afert_proc:
    """
    def __init__(
            self, input_full_nm: str, output_nm: str = '_outputs/opt',
            before_proc=None,
            proc_on_head_ln=None,
            proc_on_fld_ln=None,
            proc_on_key_ln=None,
            afert_proc=None):
        super(Mysql2PsqlDdlConverter, self).__init__(
            input_full_nm=input_full_nm,
            output_postfix='sql',
            annotation_sign='--',
            output_nm=output_nm)
        self.before_proc = before_proc
        self.proc_on_head_ln = proc_on_head_ln
        self.proc_on_fld_ln = proc_on_fld_ln
        self.proc_on_key_ln = proc_on_key_ln
        self.afert_proc = afert_proc
    pass

    def convertor_logic(self, in_str: str) -> str:
        ss = in_str
        # 预处理
        ss = _pretreatment(ss)

        # ------ 用户定义开始 ---------------------------------------------------
        ss = self.before_proc(ss)
        ## 处理第一行
        if self.proc_on_head_ln is not None:
            ss = re.sub(_msq_crt_tb_start_ln_ptn, self.proc_on_head_ln(), ss)
        ## 处理字段
        if self.proc_on_fld_ln is not None:
            ss = re.sub(_msq_crt_tb_fld_ln_ptn, self.proc_on_fld_ln(), ss)
        ## 处理Key声明
        if self.proc_on_key_ln is not None:
            ss = re.sub(_msq_crt_tb_key_ln_ptn, self.proc_on_key_ln(), ss)
        ## 处理建表声明结尾
        if self.afert_proc is not None:
            ss = self.afert_proc(ss)
        # ------用户定义结束 ----------------------------------------------------

        # 最后处理
        ss = _aftertreatment(ss)
        return ss
# ------------------------------------------------------------------------------

def _pretreatment(ss: str) -> str:
    """
    预处理, 这里将会移除无法帮助regex定位的行和字符, 而可以帮助定位但不需要的字符将在 最终处理中移除
    移除 /**/ 和 -- 注释, DROP TABLE, INSERT INTO, SET NAMES, SET FOREIGN_KEY_CHECKS
    """
    ss = re.sub(r"/\*.*(\n.*)+\*/", "", ss)
    ss = re.sub(r"--.*", "", ss)
    ss = re.sub(r"DROP TABLE.*", "", ss)
    ss = re.sub(r"INSERT INTO.*", "", ss)
    ss = re.sub(r"SET NAMES.*", "", ss)
    ss = re.sub(r"SET FOREIGN_KEY_CHECKS.*", "", ss)
    # 移除多余的 \n
    ss = re.sub(r"\n*{}\n+".format(_msq_crt_tb_ptn), r"\g<1>", ss)
    return ss

# ------------------------------------------------------------------------------


if __name__ == "__main__":
    def _proc_head_ln(schema_name: str="public"):
        def replacer(m):
            tb_nm = m.group("tb_nm")
            ss = "\nCREATE TABLE {_skm_nm}{_tb_nm} (".format(_skm_nm=schema_name, _tb_nm=tb_nm)
            return ss
        return replacer

    def _proc_fld_ln():
        """
        处理MySQL建表的 字段行 [_msq_crt_tb_fld_ln_ptn]
        """
        def replacer(m):
            # 处理字段名
            # 大驼峰 -> 小驼峰
            fld_nm = m.group("fld_nm")
            if fld_nm[0].isupper():
                fld_nm = (fld_nm[0]).lower()+fld_nm[1:]
            # 更改字段名
            fld_nm = fld_nm.replace("Date", "At")
            fld_nm = fld_nm.replace("modified", "update")

            # 处理字段类型
            fld_typ = m.group("fld_typ")
            # 这里的 bigint(20) 也是MySQL表中的主键的类型
            fld_typ = fld_typ.replace("bigint(20)", "varchar(36)")
            fld_typ = fld_typ.replace("int(11)", "integer")
            fld_typ = fld_typ.replace("tinyint(4)", "boolean")
            fld_typ = fld_typ.replace("tinyinteger", "boolean")
            fld_typ = fld_typ.replace("datetime(0)", "timestamp")

            # 其他
            fld_other = m.group("fld_other")
            if fld_other != "":
                fld_other = " "+fld_other
            return "\n  \"{_fld_nm}\" {_fld_typ}{_fld_other},".format(_fld_nm=fld_nm, _fld_typ=fld_typ, _fld_other=fld_other)
        return replacer

    def _proc_key_ln():
        """
        处理 Key声明, 将Key重命名为小写加下划线
        """
        def replacer(m):
            tb_key_fld = m.group('tb_key_fld')
            tb_key_fld = re.sub(r'[A-Z]+', lambda x: "_" +
                                x.group(0).lower(), tb_key_fld)
            return "\n  CONSTRAINT {_fld} PRIMARY KEY (id)".format(_fld=tb_key_fld)
        return replacer

    def _aftertreatment(ss: str) -> str:
        """
        最后处理
        """
        ss = re.sub(_msq_crt_tb_end_ln_ptn, "\n);", ss)
        return ss

    Mysql2PsqlDdlConverter(
        '_inputs/input.sql',
        
        proc_on_head_ln=_proc_head_ln(),
        proc_on_fld_ln=_proc_fld_ln(),
        proc_on_key_ln=_proc_key_ln(),
        afert_proc= _aftertreatment,
        ).run()
