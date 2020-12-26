from parse.ddl_parse import DdlParse
from gen.dart_gen import DartEntityGen

if __name__ == "__main__":
    # test
    DdlParse("_inputs/wms_ddl.sql", output_nm="_parse/wms_ddl").run()
    DartEntityGen(
        '_parse/wms_ddl.json', opt_nm='wms_entity').run()
