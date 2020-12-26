from abc import ABC

import base
import utils
import json


def type_ddl2dart(ddl_typ: str) -> str:
    if ddl_typ.startswith('varchar') \
            or ddl_typ.startswith('text'):
        return "String"
    if ddl_typ.startswith('numeric') \
            or ddl_typ.startswith('int') \
            or ddl_typ.startswith('timestamp'):
        return "int"
    if ddl_typ.startswith('bool'):
        return "bool"
    return "##unkonw-typ:{}#".format(ddl_typ)


# -----------------------------------------------------------------------------


class IDartGen(base.IGen, ABC):
    def __init__(self, input_nm: str, part_file_nm: str, otp_path: str = "", ):
        """
        otp_path: 生成文件的路径, 与[part_file_nm]和[self.output_postfix]合并, 成为完整的文件名
        part_file_nm: Dart文件的Part, 将会根据该文件生成文件名和 part of 头
            如, 要生成 xx_repo_impl.dart 的代码, 则该参数为 xx_repo_impl
        """
        self.part_file_nm = part_file_nm
        super(IDartGen, self).__init__(
            input_nm=input_nm,
            opt_postfix="py-g.dart",
            annotation_sign="/// ",
            opt_nm=otp_path + part_file_nm
        )


class DartEntityGen(base.IGen):
    def convert_by_ddl(self, ddl: dict) -> str:
        # todo 没有使用父类的convertor_logic方法,
        pass

    def __init__(self, input_nm: str, opt_nm: str = "gen"):
        """
        TODO : 让本类继承于 IDartGen, 同时适配 __init__
        """
        super(DartEntityGen, self).__init__(
            input_nm=input_nm,
            opt_postfix="dart",
            annotation_sign="/// ",
            opt_nm=opt_nm
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
            all_r += "\n" + gg_extension_all
        return all_r


class DartGacICrudRepoGen(IDartGen):
    def convert_by_ddl(self, ddl: dict):
        clz = utils.underscore2upper_camel(str(ddl.get('table')))
        c_ln = "abstract class I%sRepo extends ICrudRepo<%s, String> {}\n" % (
            clz, clz)
        return c_ln


class DartGacCrudRepoImplGen(IDartGen):
    # GetArch CrudRepo 生成
    def convert_by_ddl(self, ddl: dict):
        clz = utils.underscore2upper_camel(str(ddl.get('table')))
        under_clz = utils.upper_camel2underscore(clz)

        c_part_ln = "part of '{}.dart';".format(self.part_file_nm)
        c_anno_ln = "@LazySingleton(as: I{_clz}Repo)".format(_clz=clz)
        c_head_ln = "class %sRepoImpl extends I%sRepo {" % (clz, clz)
        c_crt_method_ln = (
                                  "\n  @override" +
                                  "\n  Future <%s> create(%s entity) async {" +
                                  "\n    var dto = %sDto.fromDM(entity);" +
                                  "\n    var id = getUuid();" +
                                  "\n    var r = await _sqlClient" +
                                  "\n        .table('%s')" +
                                  "\n        .insert(dto.toJson().appendUuid(uuid: id));" +
                                  "\n    return dto.copyWith(id: id).toDomain();" +
                                  "\n  }") % (clz, clz, clz, under_clz)
        c_del_method_ln = (
                                  "\n  @override" +
                                  "\n  Future <Unit> delete(String id) async {" +
                                  "\n    var r = await _sqlClient" +
                                  "\n        .table('%s')" +
                                  "\n        .whereColumn('id', equals: id)" +
                                  "\n        .deleteAll();" +
                                  "\n    return null;" +
                                  "\n  }") % (under_clz,)
        c_update_method_ln = (
                                     "\n  @override" +
                                     "\n  Future <%s> update(%s item) async {" +
                                     "\n    if (item.id == null) throw StorageFailure('被更新的对象id不能为null');" +
                                     "\n    var js = %sDto.fromDM(item).toJson();" +
                                     "\n    var r = await _sqlClient.table('%s').insert(js);" +
                                     "\n    return item;" +
                                     "\n  }") % (clz, clz, clz, under_clz)
        c_read_method_ln = (
                                   "\n  @override" +
                                   "\n  Future <%s> read(String id) async {" +
                                   "\n    var r = await _sqlClient" +
                                   "\n        .table('%s')" +
                                   "\n        .whereColumn('id', equals: id)" +
                                   "\n        .select()" +
                                   "\n        .toMaps();" +
                                   "\n    if (r.length == 0) {" +
                                   "\n      return null;" +
                                   "\n    } else if (r.length == 1) {" +
                                   "\n      var js = r[0];" +
                                   "\n      var dm = %sDto.fromJson(js).toDomain();" +
                                   "\n      return dm;" +
                                   "\n    } else {" +
                                   "\n      throw StorageFailure('通过id查询到了多个返回值!');" +
                                   "\n    }" +
                                   "\n  }") % (clz, under_clz, clz)
        c_query_by_ln = (
                                "\n  @override" +
                                "\n  Future<List<%s>> query({int limit = null, int offset = 0}) async {" +
                                "\n    var r = await _sqlClient" +
                                "\n        .table('%s')" +
                                "\n        .limit(limit)" +
                                "\n        .offset(offset)" +
                                "\n        .select()" +
                                "\n        .toMaps();" +
                                "\n    return r?.map((js) => %sDto.fromJson(js).toDomain())?.toList();" +
                                "\n  }") % (clz, under_clz, clz)

        c_end_ln = "}\n"
        _code_list = [
            c_part_ln, "\n\n",
            c_anno_ln, "\n",
            c_head_ln, "\n",
            c_crt_method_ln, "\n",
            c_del_method_ln, "\n",
            c_update_method_ln, "\n",
            c_read_method_ln, "\n",
            c_query_by_ln, "\n",
            c_end_ln
        ]
        return ''.join(_code_list)


if __name__ == "__main__":
    # DartEntityGen('_parse/otp.json', output_nm='_outputs/gen').run()
    # # DartEntityGen('_parse/wms_ddl.json', output_nm='_outputs/wms_entities').run()
    # # DartEntityGen('_parse/wms_ddl.json', output_nm='_outputs/wms_entity').run()
    # DartDtoGen('_parse/wms_ddl.json', output_nm='_outputs/wms_dtos').run()
    ###
    # DartGacICrudRepoGen('_parse/wms_ddl.json',
    #                     output_nm='_outputs/i_wms_repos').run()
    DartGacCrudRepoImplGen('_parse/wms_ddl.json', 'wms_repo_impls').run()
