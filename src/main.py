import datetime
import abc


class IConvertor(metaclass=abc.ABCMeta):
    def __init__(self, input_full_nm: str, output_postfix: str, annotation_sign: str, output_nm: str = "otp",):
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

    @abc.abstractmethod
    def convertor_logic(self, in_str: str) -> str:
        pass

    def run(self, input_nm: str = '', output_full_nm: str = '', insert_dt: bool = True):
        if input_nm == "":
            input_nm = self.input_nm
        if output_full_nm == "":
            output_full_nm = self.output_nm+"."+self.output_postfix

        with open(input_nm, "r", encoding="utf-8") as inpt:
            rst = self.convertor_logic(inpt.read(),)
            if rst is None:
                print("写入值为空, 请检查代码!")
                return
            with open(output_full_nm, "w", encoding="utf-8") as otpt:
                gen_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                gen_dt = "GEN DT: {}\n".format(gen_dt)
                if insert_dt and (self.annotation_sign != ""):
                    rst = "{}{}\n{}".format(
                        self.annotation_sign, gen_dt, rst)
                else:
                    print("未向文件写入生成信息 "+gen_dt)
                otpt.write(rst)


class IParser(IConvertor):
    """
    解析其他语言生成json
    """

    def __init__(self, input_nm: str, output_nm: str = "parse"):
        super(IParser, self).__init__(
            input_full_nm=input_nm,
            output_postfix="json",
            annotation_sign="",
            output_nm=output_nm)

class IGen(IConvertor):
    """
    将json转换为其他语言
    """
    def __init__(self, input_nm: str, output_postfix: str, annotation_sign: str, output_nm: str = "gen"):
        super(IGen, self).__init__(
            input_full_nm=input_nm,
            output_postfix=output_postfix,
            annotation_sign=annotation_sign,
            output_nm=output_nm
        )
