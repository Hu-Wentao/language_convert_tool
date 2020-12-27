import datetime
import abc
import json
from abc import ABC


class IConvertor(metaclass=abc.ABCMeta):
    def __init__(self, input_full_nm: str, output_postfix: str, annotation_sign: str, output_nm: str = "otp", ):
        """
        input_full_nm: 输入文件的完全名称, 包括路径和后缀
        output_postfix: 输出文件的后缀
        annotation_sign: 代码注解符号, 如 //, --等
        output_nm: 输出文件的名称, 可以包含路径, 但不包含后缀
        """
        self.input_nm = input_full_nm
        self.output_postfix = output_postfix
        self.annotation_sign = annotation_sign
        self.output_nm = output_nm

    def insert_file_start(self) -> str:
        return ''

    def insert_file_end(self) -> str:
        return ''

    @abc.abstractmethod
    def convertor_logic(self, in_str: str) -> str:
        pass

    def run(self, input_nm: str = '', output_full_nm: str = '', insert_dt: bool = True):
        if input_nm == "":
            input_nm = self.input_nm
        if output_full_nm == "":
            output_full_nm = self.output_nm + "." + self.output_postfix

        with open(input_nm, "r", encoding="utf-8") as inp:
            rst = self.convertor_logic(inp.read(), )
            if rst is None:
                print("写入值为空, 请检查代码!")
                return
            with open(output_full_nm, "w", encoding="utf-8") as otp:
                all_outputs = []

                gen_dt = "{}GEN DT: {}\n".format(
                    self.annotation_sign,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                if insert_dt and (self.annotation_sign != ""):
                    all_outputs.append(gen_dt)
                    print("成功写入时间信息: " + gen_dt)
                else:
                    print("未写入时间信息: " + gen_dt)

                start = self.insert_file_start()
                end = self.insert_file_end()
                if start != '':
                    all_outputs.append(start)
                if rst != '':
                    all_outputs.append(rst)
                if end != '':
                    all_outputs.append(end)
                otp.writelines(all_outputs)
                print("文件输出路径: {}".format(output_full_nm))


class IParser(IConvertor, ABC):
    """
    解析其他语言生成json
    """

    def __init__(self, input_nm: str, output_nm: str = "parse"):
        super(IParser, self).__init__(
            input_full_nm=input_nm,
            output_postfix="json",
            annotation_sign="",
            output_nm=output_nm)


class IGen(IConvertor, ABC):
    """
    将json转换为其他语言
    """

    def __init__(self, annotation_sign: str,
                 input_nm: str,
                 opt_postfix: str,
                 otp_path: str = "_outputs/",
                 opt_nm: str = "gen"):
        super(IGen, self).__init__(
            input_full_nm=input_nm,
            output_postfix=opt_postfix,
            annotation_sign=annotation_sign,
            output_nm=otp_path + opt_nm
        )

    def convertor_logic(self, in_str: str):
        all_dict = json.loads(in_str)
        all_r = ''
        for ddl in all_dict:
            all_r += self.convert_by_ddl(ddl)
        return all_r

    @abc.abstractmethod
    def convert_by_ddl(self, ddl: dict) -> str:
        pass
