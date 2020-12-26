import base
import utils
import json
import abc


class IDdlGen(base.IGen):
    def __init__(self, input_nm: str, gen_file_nm: str, otp_path: str = "", ):
        """
        otp_path: 生成文件的路径, 与[part_file_nm]和[self.output_postfix]合并, 成为完整的文件名
        part_file_nm: Dart文件的Part, 将会根据该文件生成文件名和 part of 头
            如, 要生成 xx_repo_impl.dart 的代码, 则该参数为 xx_repo_impl
        """
        self.gen_file_nm = gen_file_nm
        super(IDdlGen, self).__init__(
            input_nm=input_nm,
            opt_postfix="py-g.sql",
            annotation_sign="-- ",
            opt_nm=otp_path + gen_file_nm
        )

    def convertor_logic(self, in_str: str):
        all_dict = json.loads(in_str)
        print('load')
        all_r = ''
        for ddl in all_dict:
            all_r += self.convert_by_ddl(ddl)
        return all_r

    @abc.abstractmethod
    def convert_by_ddl(self, ddl: dict):
        pass


class DdlGen(IDdlGen):
    # GetArch CrudRepo 生成
    def convert_by_ddl(self, ddl: dict):
        schema = str(ddl.get('schema'))
        clz = utils.underscore2upper_camel(str(ddl.get('table')))
        under_clz = utils.upper_camel2underscore(clz)
        fls = ddl.get('fields')
        prm_key_nm = ddl.get('primary')['name']
        prm_key_fld = ddl.get('primary')['field']

        # fixme 如果schema是空呢?
        c_head_ln = "  CREATE TABLE {_skm}.{_under_clz} (".format(
            _skm=schema, _under_clz=under_clz)
        c_fld_ln = []
        for fld in fls:
            name = fld.get('field')
            typ = fld.get('type')
            fl_ln = '    "{_nm}" {_typ},'.format(_nm=name, _typ=typ)
            c_fld_ln.append(fl_ln)
        c_fld_ln = ''.join(c_fld_ln)
        key_ln = "    CONSTRAINT %s PRIMARY KEY (%s)" % (prm_key_nm, prm_key_fld)
        c_end_ln = "  );\n"
        _code_list = [
            c_head_ln, "\n",
            c_fld_ln, "\n",
            key_ln, "\n",
            c_end_ln
        ]
        return ''.join(_code_list)


if __name__ == "__main__":
    DdlGen(input_nm='_parse/wms_ddl.json', gen_file_nm='wms_ddl', ).run()
