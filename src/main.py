# import ddl_parse
# import dart_entity_gen
from ddl_parse import DdlParse
from dart_gen import DartEntityGen

if __name__ == "__main__":
    # test
    DdlParse("_inputs/wms_ddl.sql", output_nm="_parse/wms_ddl").run()
    DartEntityGen(
        '_parse/wms_ddl.json', output_nm='_outputs/wms_entity').run()
