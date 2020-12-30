import abc

import utils


class CodeAdapter:
    def __init__(self, annotation_symbol: str, file_postfix: str, file_start: str = '', file_end: str = ''):
        """
        适配某种特定语言
        :param annotation_symbol:
        :param file_postfix:
        """
        self.annotation_symbol = annotation_symbol
        self.file_postfix = file_postfix
        self.file_start = file_start
        self.file_end = file_end


class ICodeTransformer:
    def __init__(self):

        @abc.abstractmethod
        def trans(self, src: str):
            pass


class IDdlJsonTransformer(ICodeTransformer):
    def trans(self, src: str):
        import json
        all_dict = json.loads(src)
        all_r = ''
        for ddl in all_dict:
            all_r += self.convert_by_ddl(ddl)
        return all_r

    @abc.abstractmethod
    def convert_by_ddl(self, ddl: dict) -> str:
        pass


class DdlJsonPhpTrans(IDdlJsonTransformer):
    def convert_by_ddl(self, ddl: dict) -> str:
        clz = utils.underscore2upper_camel(str(ddl.get('table')))
        fls = ddl.get('fields')
        # --
        c_head_ln = "class %s\n{" % clz
        c_fld_ln = []
        for fld in fls:
            name = fld.get('field')
            fl_ln = "    private $%s;\n" % name
            c_fld_ln.append(fl_ln)
        c_fld_ln = ''.join(c_fld_ln)

        c_fld_gc_ln = []
        for fld in fls:
            name = fld.get('field')
            up_name = utils.low2upper_camel(name)
            fl_get_ln = ("\n    public function get%s()" +
                         "\n    {" +
                         "\n        return $this->%s;" +
                         "\n    }\n") % (up_name, name)
            fl_set_ln = ("\n    public function set%s($%s)" +
                         "\n    {" +
                         "\n        $this->%s = $%s;" +
                         "\n    }\n") % (up_name, name, name, name)
            c_fld_gc_ln.append(fl_get_ln + fl_set_ln)
        c_fld_gc_ln = ''.join(c_fld_gc_ln)
        _code_list = [
            c_head_ln, "\n",
            c_fld_ln, "\n",
            c_fld_gc_ln, "\n",
            '}', "\n",
        ]
        return ''.join(_code_list)


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------

class CodeBuilder:
    def __init__(self, adapter: CodeAdapter, insert_gen_info: bool = True):
        # 被操作的数据
        self.operate = ''
        self.adapter = adapter

    # -- From
    def from_str(self, src: str):
        self.operate = src
        return self

    def from_file(self, file_path: str, encoding='utf-8'):
        with open(file_path, "r", encoding=encoding) as f:
            self.from_str(f.read())
        return self

    # -- Do
    def _gen_info(self):
        from datetime import datetime
        return "{}GEN DT: {}\n".format(
            self.adapter.annotation_symbol,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    def transform(self, trans: ICodeTransformer):

        return self

    # -- To
    def _on_output(self):
        gen = self._gen_info()
        print(gen)
        if self.adapter.annotation_symbol != '':
            self.operate = self._gen_info() + self.operate
        else:
            print('未配置adapter的注释符号, 无法写入生成信息')

    def to_cmd(self):
        self._on_output()
        print(self.operate)
        return self

    def to_file(self, file_path: str, encoding='utf-8'):
        self._on_output()
        print('文件将写入到: ', file_path)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(self.operate)
        return self

    def to_file_with_adapter(self, file_name: str, encoding='utf-8'):
        return self.to_file(file_path=file_name + self.adapter.file_postfix, encoding=encoding)


# ------------------------------------------------------------------------------
# Adapter
php_adapter = CodeAdapter(
    annotation_symbol="// ",
    file_postfix=".py_g.php",
    file_start="<?php",
    file_end="?>",
)

if __name__ == '__main__':
    CodeBuilder(
        adapter=php_adapter, ) \
        .from_file('../_parse/wms_ddl.json', ) \
        .transform() \
        .to_cmd()
