import re # 导入正则表达式包
import datetime

def repl_camel():
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

def fun(ss: str) -> str:
  """
  将MySQL 转换为DDL语句
  """
  # --> 0 移除声明语句
  # 引擎声明, 
  # 字段后的charset声明
  ss = re.sub(r"ENGINE = InnoDB.*;","", ss)
  ss = re.sub(r" CHARACTER SET.*,",",", ss)

  # --> 1 为表名添加 数据库名称 
  # CREATE TABLE `sys_dept` -> CREATE TABLE public.sys_dept(指定库名 public.)
  # DROP 删除..
  # INSERT 插入..
  ss = re.sub(r"CREATE TABLE `(.*)`", "CREATE TABLE public.`\g<1>`", ss)
  ss = re.sub(r"DROP TABLE IF EXISTS `(.*)`", "DROP TABLE IF EXISTS public.`\g<1>`", ss)
  ss = re.sub(r"INSERT INTO `(.*)`", "INSERT INTO public.`\g<1>`", ss)
  # ss = re.sub(r"CREATE TABLE `(.*)`", "CREATE TABLE public.\g<1>", ss)
  # ss = re.sub(r"DROP TABLE IF EXISTS `(.*)`", "DROP TABLE IF EXISTS public.\g<1>", ss)
  # ss = re.sub(r"INSERT INTO `(.*)`", "INSERT INTO public.\g<1>", ss)

  # --> 2 字段名更改
  # 将表的字段名由大驼峰改为小驼峰, 
  # xxxDate重命名为 xxxAt
  # modifiedXxx -> updateXxx
  ss = re.sub(r"`(\w.*)`", repl_camel(), ss)

  # --> 3 替换 主键声明为DDL格式, 主键名固定为id , CONSTRAINT warehouse_pkey PRIMARY KEY (id)
  ss = re.sub(r"PRIMARY KEY \(`(.*)`\)( USING BTREE)?","CONSTRAINT \g<1>_pkey PRIMARY KEY (id)", ss)

  # 3-> 4 替换 将主键名称统一为 `id`, 字段类型为 varchar(36), 因为uuid长度为36
  ss = re.sub(r"(CREATE.*\n\s{2})`.*Id` bigint\(20\) NOT NULL.*,", "\g<1>`id` varchar(36) NOT NULL,", ss,flags=re.MULTILINE)
  # ss = re.sub(r"(CREATE.*\n\s{2})`(.*Id)` bigint\(20\) NOT NULL.*,", "\g<1>`id` varchar(36) NOT NULL,", ss)
  # ss = re.sub(r"bigint\(20\)", "varchar(36)", ss)

  # --> 5 收尾工作
  # 替换 `` 为 ""
  # 删除 COMMENT 注释
  ss = re.sub("`", "\"", ss)
  ss = re.sub(" COMMENT.*", ",", ss)
  ss = re.sub(r"tinyint\(4\)", "boolean", ss)
  ss = re.sub(r"datetime\(0\)", "timestamp", ss)
  return ss


def file_io(input_file: str='input.sql',output_file: str='outputs.sql' ):
      # with open("input.sql", "rw",encoding="utf-8") as sql:
    with open(input_file, "r",encoding="utf-8") as sql:
      rst = fun(sql.read(),)
      with open(output_file, "w", encoding="utf-8") as otp:
        gen_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        rst = "-- GEN DT: {}\n\n{}".format(gen_dt,rst)
        otp.write(rst)

if __name__ == "__main__":
  file_io(
    input_file="test/t1.sql",
  )