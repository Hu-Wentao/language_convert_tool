import datetime
import abc
from typing import Optional
from typing import List
from sys import stdin


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
                    print("成功写入时间信息: "+gen_dt)
                else:
                    print("未写入时间信息: "+gen_dt)
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

# -----------------------------------------------------------------------------


class IAccess:
    """
    读写通道, 可以是文件, 控制台 或者其他 IAccess实现类进行读写
    """

    def __init__(self,value=None):
        self.value = value
        pass

    @abc.abstractmethod
    def read(self) -> object:
        pass

    @abc.abstractmethod
    def set(self, value)->object:
        self.value = value
        return self.value

    @abc.abstractmethod
    def write(self) -> Optional[str]:
        """
        返回值表示 出错时的提示信息
        """
        pass


class IProcessor(object):
    @abc.abstractmethod
    def run(self, access: IAccess) -> IAccess:
        """
        返回值为 access: IAccess, 正常情况下直接运行 access 即可, 
        但如果有多个Processor, 则需要将 access 作为下一个processor的input
        """
        pass


class IBaseConverter:
    """
    全新的转换基类
    """

    def __init__(
        self,
        access: IAccess,
        process_list: List[IProcessor],
    ):
        self.access = access
        self.process_list = process_list
        pass

    @abc.abstractmethod
    def on_init(self):
        pass
# -----------------------------------------------------------------------------


class CmdAccess(IAccess):
    def __init__(self, value: str = '', need_read: bool = True):
        self.value = value
        self.need_read = need_read

    def read(self, tips: str = ''):
        if self.need_read is True:
            self.value = input(tips)
        return self.value

    def write(self, leading: str = '', trailing: str = ''):
        print(leading+self.value+trailing)


class CustomProcessor(IProcessor):
    def __init__(self, on_run):
        self.on_run = on_run

    def run(self, input: IAccess):
        v = self.on_run(input.read())
        input.set(v)
        return input


class CustomConverter(IBaseConverter):
    def __init__(
        self,
        access: IAccess,
        process_list: List[IProcessor],
    ):
        super(CustomConverter, self).__init__(
            access, process_list=process_list)
        self.on_init()

    def on_init(self):
        acc = self.access
        for proc in self.process_list:
            acc = proc.run(acc)
        acc.write()


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    CustomConverter(
        access=CmdAccess('请输入:', need_read=False),
        process_list=[
            CustomProcessor(on_run=lambda x: x+'asdff')
        ],
    )
