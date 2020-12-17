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
            input_nm =self.input_nm
        if output_full_nm == "":
            output_full_nm =self.output_nm+"."+self.output_postfix

        with open(input_nm, "r", encoding="utf-8") as inpt:
            rst = self.convertor_logic(inpt.read(),)
            with open(output_full_nm, "w", encoding="utf-8") as otpt:
                gen_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                if insert_dt and (self.annotation_sign is not None):
                    rst = "{} GEN DT: {}\n\n{}".format(
                        self.annotation_sign, gen_dt, rst)
                otpt.write(rst)
