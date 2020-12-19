import re
import main
import utils
import json


def type_ddl2dart(ddl_typ: str) -> str:
    if ddl_typ.startswith('varchar'):
        return "String"
    if ddl_typ.startswith('numeric')\
            or ddl_typ.startswith('int')\
            or ddl_typ.startswith('timestamp'):
        return "int"
    if ddl_typ.startswith('bool'):
        return "bool"
    return "##unkonw-typ:{}#".format(ddl_typ)


class DartEntityGen(main.IGen):
    def __init__(self, input_nm: str, output_nm: str = "gen"):
        super(DartEntityGen, self).__init__(
            input_nm=input_nm,
            output_postfix="dart",
            annotation_sign="/// ",
            output_nm=output_nm
        )

    def convertor_logic(self, in_str: str):
        all_dict = json.loads(in_str)
        all_r = ''
        for ddl in all_dict:
            # print(ddl,'\n')
            clz = utils.underscore2upper_camel(ddl.get('table'))
            g_head_ln = "class %s extends IEntity<String> {" % (clz)
            g_all_flds = ''
            all_fld_nm = []
            for fld in ddl.get('fields'):
                typ = type_ddl2dart(fld.get('type'))
                fld_nm = fld.get('field')
                all_fld_nm.append(fld_nm)
                g_all_flds += "  final {_typ} {_fld_nm};".format(
                    _typ=typ, _fld_nm=fld_nm)
            # 处理 al_fld_nm
            all_fld_nm_ln = ''
            for fld_nm in all_fld_nm:
                all_fld_nm_ln += "this.{_fld},".format(_fld=fld_nm) 
            g_constructor = "%s({%s});" % (clz, all_fld_nm_ln)
            g_props = "  @override\n  List<Object> get props => [{}];".format(
                all_fld_nm_ln)
            all_r += (
                "\n%s\n%s\n%s\n%s}" % (g_head_ln, g_all_flds, g_constructor, g_props))
        return all_r


if __name__ == "__main__":
    DartEntityGen('_parse/otp.json', output_nm='_outputs/gen').run()
