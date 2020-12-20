import base
import utils
import json


def type_ddl2dart(ddl_typ: str) -> str:
    if ddl_typ.startswith('varchar')\
            or ddl_typ.startswith('text'):
        return "String"
    if ddl_typ.startswith('numeric')\
            or ddl_typ.startswith('int')\
            or ddl_typ.startswith('timestamp'):
        return "int"
    if ddl_typ.startswith('bool'):
        return "bool"
    return "##unkonw-typ:{}#".format(ddl_typ)


class DartEntityGen(base.IGen):
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
            # head
            g_head_ln = "class %s extends IEntity<String> {" % (clz)
            # fields
            g_all_flds = ''
            all_fld_nm = []
            for fld in ddl.get('fields'):
                typ = type_ddl2dart(fld.get('type'))
                fld_nm = fld.get('field')
                all_fld_nm.append(fld_nm)
                g_all_flds += "  final {_typ} {_fld_nm};".format(
                    _typ=typ, _fld_nm=fld_nm)
            # 处理 all_fld_nm
            all_fld_nm_ln = ''
            for fld_nm in all_fld_nm:
                all_fld_nm_ln += "this.{_fld},".format(_fld=fld_nm)
            # 构造
            g_constructor = "%s({%s});" % (clz, all_fld_nm_ln)
            # props
            g_props = "  @override\n  List<Object> get props => [{}];".format(
                all_fld_nm_ln)
            # 合并
            all_r += (
                "\n%s\n%s\n%s\n%s}" % (g_head_ln, g_all_flds, g_constructor, g_props))
        return all_r


class DartDtoGen(DartEntityGen):
    def convertor_logic(self, in_str: str):
        all_dict = json.loads(in_str)
        all_r = ''
        for ddl in all_dict:
            clz = utils.underscore2upper_camel(ddl.get('table'))
            # head
            g_head_ln = "abstract class %sDto extends IDto with _$%sDto {" % (
                clz, clz)
            # fields
            # all_fld_nm = []
            all_fld_nm_ln = ''
            all_fld_param_ln = ''
            all_x_param_ln = ''
            for fld in ddl.get('fields'):
                typ = type_ddl2dart(fld.get('type'))
                fld_nm = fld.get('field')
                # --
                # all_fld_nm.append(fld_nm)
                all_fld_nm_ln += "  @JsonKey(defaultValue: null) {_typ} {_fld_nm},".format(
                    _typ=typ, _fld_nm=fld_nm)
                all_fld_param_ln += "{_fld}: d?.{_fld},".format(_fld=fld_nm)
                all_x_param_ln += "{_fld}:{_fld},".format(_fld=fld_nm)

            # 默认工厂构造
            g_constructor = "factory %sDto({%s}) = _%sDto;" % (
                clz, all_fld_nm_ln, clz)

            # 工厂命名构造 fromDM
            g_fm_dm = "factory {_clz}Dto.fromDM({_clz} d) => {_clz}Dto({_params});".format(
                _clz=clz, _params=all_fld_param_ln)

            # 工厂命名构造 fromJson
            g_fm_js = "factory {_clz}Dto.fromJson(Map<String, dynamic> json) => _${_clz}DtoFromJson(json);".format(
                _clz=clz)
            # 合并 Dto类
            all_r += (
                "\n@freezed\n%s\n%s\n%s\n%s}" % (g_head_ln, g_constructor, g_fm_dm, g_fm_js))
            ##
            # 构建 extension
            x_head_ln = "extension %sDtoX on %sDto {" % (clz, clz)
            # 构建 toDomain
            x_to_dm_ln = "  {_clz} toDomain() => {_clz}({_all_x_param});".format(
                _clz=clz, _all_x_param=all_x_param_ln)
            gg_extension_all = "%s %s}" % (x_head_ln, x_to_dm_ln)
            all_r += "\n"+gg_extension_all
        return all_r


if __name__ == "__main__":
    # DartEntityGen('_parse/otp.json', output_nm='_outputs/gen').run()
    # DartEntityGen('_parse/wms_ddl.json', output_nm='_outputs/wms_entities').run()
    # DartEntityGen('_parse/wms_ddl.json', output_nm='_outputs/wms_entity').run()
    DartDtoGen('_parse/wms_ddl.json', output_nm='_outputs/wms_dtos').run()
