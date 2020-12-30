from abc import ABC

import utils
from base import IGen


class IPhpGen(IGen, ABC):
    def __init__(self, input_nm: str, opt_nm: str, otp_path: str = '../../_outputs/'):
        super(IPhpGen, self).__init__(
            annotation_sign="// ",
            input_nm=input_nm,
            opt_postfix="py-g.php",
            otp_path=otp_path,
            opt_nm=opt_nm,
        )

    def insert_file_start(self) -> str:
        return '<?php\n'

    def insert_file_end(self) -> str:
        return '\n?>'


class PhpEntityGen(IPhpGen):

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
        pass


if __name__ == '__main__':
    PhpEntityGen(input_nm='../../_parse/wms_ddl.json', opt_nm='wms_entities').run()
    # PhpEntityGen(input_nm='D:\proj_py\language_convert_tool\_parse\wms_ddl.json', opt_nm='wms_ddl').run()
