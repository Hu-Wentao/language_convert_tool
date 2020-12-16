import re # 导入正则表达式包
import datetime

def repl_camel():
  """
  # 将表的字段名由大驼峰改为小驼峰, 
  # xxxDate重命名为 xxxAt
  # modifiedXxx -> updateXxx
  # """
  def replacer(m):
    # 找到 字段名的首字母(这里是第$char_offset个), 然后替换为小写, 完成大小驼峰转换
    char_offset = 1
    all = m.group(0)

    char = all[char_offset]
    if char.isupper():
      all = all[:char_offset]+char.lower()+all[char_offset+1:]

    # 将 xxxDate 重命名为 xxxAt
    all = str(all).replace("Date", "At")
    # modifiedXxx -> updateXxx
    all = str(all).replace("modified", "update")
    return all
  return replacer

def transverter(ss: str, 
  psql_schema_name: str='public',
  pk_type: str='varchar(36)',
  ) -> str:
  """
  将MySQL语句 转换为 PostgreSQL DDL语句

  # 移除引擎,charset等声明语句 (0)
  # 
  """

  # --> 1 为表名添加 数据库名称 
  # CREATE TABLE `sys_dept` -> CREATE TABLE $psql_schema_name.sys_dept(指定库名 $psql_schema_name.)
  # DROP 删除.. -- DDL不支持DROP语句, 并在 5 处移除
  # INSERT 插入.. -- 由于修改了字段类型, 因此不再支持插入, 在 5处移除
  # 建表语句,末尾补上分号";"
  ss = re.sub(r"CREATE TABLE `(.*)` ", "CREATE TABLE {}.`\g<1>`".format(psql_schema_name), ss)
  # ss = re.sub(r"DROP TABLE IF EXISTS `(.*)`", "DROP TABLE IF EXISTS {}.`\g<1>`".format(psql_schema_name), ss)
  # ss = re.sub(r"INSERT INTO `(.*)`", "INSERT INTO {}.`\g<1>`".format(psql_schema_name), ss)
  ss = re.sub(r"(CREATE.*\n)((\s{2}.*)+)(\n\))", "\g<1>\g<2>\g<4>;", ss)

  # --> 2 字段名更改
  # 将表的字段名由大驼峰改为小驼峰, 
  # xxxDate重命名为 xxxAt
  # modifiedXxx -> updateXxx
  ss = re.sub(r"`(\w.*)`", repl_camel(), ss)

  # 2-> 3 替换 主键声明为DDL格式, 主键名固定为id , CONSTRAINT <表名>_pkey PRIMARY KEY (id)
  # - 2将字段改为小驼峰后, 将会影响到 主键的定义名称
  ss = re.sub(r"(CREATE TABLE .*`(.*)`.*)((\n\s{2}`.*)+)((\n\s{2}.*)*)(\n\);)",r"\g<1>\g<3>\n  CONSTRAINT \g<2>_pkey PRIMARY KEY (id)\g<7>", ss)

  # 3-> 4 替换 
  # - 3将主键统一为 id
  # 主键名称统一为 `id`, 字段类型为 varchar(36), 因为uuid长度为36
  # bigint(xx) -> bigint
  # int(11) -> integer
  # tinyint(4) -> boolean
  # tinyinteger -> boolean
  # datetime(0) -> timestamp (无时区)
  ss = re.sub(r"(CREATE.*\n\s{2})`.*Id` bigint\(20\) NOT NULL.*,", "\g<1>`id` {} NOT NULL,".format(pk_type), ss,flags=re.MULTILINE)
  ss = re.sub(r"(`.*By` )(bigint\(.*\))(.*,)", "\g<1>{}\g<3>".format(pk_type), ss,flags=re.MULTILINE)
  ss = re.sub(r"bigint\(.*\)", "bigint", ss)
  ss = re.sub(r"int\(.*\)", "integer", ss)
  ss = re.sub(r"tinyint\(4\)", "boolean", ss)
  ss = re.sub(r"tinyinteger", "boolean", ss)
  ss = re.sub(r"datetime\(0\)", "timestamp", ss)

  # --> 5 收尾工作
  # 替换 `` 为 ""
  # 删除 COMMENT 注释
  # 删除 DEFAULT NULL 
  # 删除 SET FOREIGN_KEY_CHECKS ...
  # 删除 SET FOREIGN_KEY_CHECKS .. 
  # 删除 SET NAMES ...
  # 删除 /* */ 和 -- 注释
  # 删除 DROP语句
  # 删除 两个建表语句之间多余的 \n
  # 删除 引擎声明, 
  # 删除 字段后的charset声明
  ss = re.sub("`", "\"", ss)
  ss = re.sub(" COMMENT.*", ",", ss)
  ss = re.sub(r"\s?DEFAULT NULL\s?", "", ss)
  ss = re.sub(r"SET FOREIGN_KEY_CHECKS.*", "", ss)
  ss = re.sub(r"SET NAMES.*", "", ss)
  ss = re.sub(r"/\*.*(\n.*)+\*/", "", ss)
  ss = re.sub(r"--.*", "", ss)
  ss = re.sub(r"DROP TABLE.*", "", ss)
  ss = re.sub(r"INSERT INTO.*", "", ss)
  ss = re.sub(r"(\n+)(CREATE.*)", r"\n\g<2>", ss)
  ss = re.sub(r"ENGINE = InnoDB.*;","", ss)
  ss = re.sub(r" CHARACTER SET.*,",",", ss)
  # --> 6 修改Insert 
  # "sys_menu_wms"表
  # ss = re.sub(r"(INSERT INTO {}.\"sys_menu_wms\" VALUES \(\d+, '\w+', .+, .+, \d+, \d+, )(\d+)(.*)".format(psql_schema_name),"\g<1>true\g<3>", ss)

  return ss


def file_io(input_file: str='input.sql',output_file: str='outputs.sql',insert_dt:bool=True,):
      # with open("input.sql", "rw",encoding="utf-8") as sql:
    with open(input_file, "r",encoding="utf-8") as sql:
      rst = transverter(sql.read(),)
      with open(output_file, "w", encoding="utf-8") as otp:
        gen_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if insert_dt:
          rst = "-- GEN DT: {}\n\n{}".format(gen_dt,rst)
        otp.write(rst)

if __name__ == "__main__":
  file_io()