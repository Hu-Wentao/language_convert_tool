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
    self.value 以 str 类型保存读取到的数据
    """

    def __init__(self, value:str=None):
        self.value = value
        pass

    @abc.abstractmethod
    def read(self) -> str:
        pass

    @abc.abstractmethod
    def write(self) -> Optional[str]:
        """
        返回值表示 出错时的提示信息
        """
        pass

    @abc.abstractmethod
    def set(self, value) -> str:
        self.value = value
        return self.value

    @abc.abstractmethod
    def get(self) -> str:
        return self.value


class IProcessor(IAccess):
    def __init__(self, access: IAccess):
        self.access = access

    def run(self) -> IAccess:
        """
        返回 IAccess, 可以向其他Proc提供数据
        """
        self.read()
        self.access.write()
        return self.access

    @abc.abstractmethod
    def on_run(self,input: str) -> str:
        pass

    def read(self, ) -> str:
        """
        这里重写 read(), 当Processor作为 IAccess时, 将会调用本方法 
        """
        self.access.set(self.on_run(self.access.read()))
        return self.access.get()

# -----------------------------------------------------------------------------


class CustomAccess(IAccess):
    """
    快速自定义 Access, 
    on_read: String Function()
    on_write: String Function()
    """

    def __init__(self, on_read, on_write, value: str = ''):
        super(CustomAccess, self).__init__(value)
        self.on_read = on_read
        self.on_write = on_write

    def read(self) -> str:
        if self.on_read is not None:
            self.value = self.on_read()
        return self.value

    def write(self) -> Optional[str]:
        if self.on_write is not None:
            err = self.on_write(self.value)
            return err


class CmdAccess(IAccess):
    """
    从CMD中读取和输出数据
    """

    def __init__(self, value: str = '', need_read: bool = True):
        super(CmdAccess, self).__init__(value)
        self.need_read = need_read

    def read(self, tips: str = ''):
        if self.need_read is True:
            self.value = input(tips)
        return self.value

    def write(self, leading: str = '', trailing: str = ''):
        print(leading+self.value+trailing)

class FileAccess(IAccess):
    """
    从文件中读写数据
    """
    def __init__(self,in_file:str, in_path="_inputs/",out_file:str="opt", out_path:str="_outputs/",write_gen:bool= True):
        super(FileAccess, self).__init__()
        self.in_file = in_file
        self.in_path = in_path
        self.out_file = out_file
        self.out_path = out_path
        self.write_gen= write_gen

    def read(self):
        with open(self.in_path+self.in_file, "r", encoding="utf-8") as f:
            self.value = f.read()
    
    def write(self):
        path = self.out_path+self.out_file
        gen_dt = "GEN DT: {}\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        with open(path,"w",encoding="utf-8") as f:
            w = self.value
            if self.write_gen:
                w = gen_dt+w
            f.write(w)
        print('写入文件:'+path+"\n"+gen_dt)
        

class CustomProcessor(IProcessor):
    """
    on_run: String Function(String input)
    """

    def __init__(self, access: IAccess, proc):
        super(CustomProcessor, self).__init__(access=access)
        self.proc = proc

    def read(self) -> str:
        self.value = self.on_run(self.access.read())
        self.access.write()
        return self.value

    def on_run(self, input: str) -> str:
        r = self.proc(input)
        print('rr',r)
        return r
        


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # 直接运行, 通过 access定义的方式进行读写
    # 用 .read()取代 .run(), 可以获取处理结果(str类型)
    c = CustomProcessor(
        access=CustomAccess(
            on_read=lambda: '哈哈哈###',
            on_write=lambda x: print(x),
        ),
        proc=lambda x: x+'啦啦啦'
    ).run()

    # 将其他 Processor作为 Access
    # CustomProcessor(
    #     access=CustomAccess(
    #         on_read=lambda: c.get(),
    #         on_write=lambda: print,
    #     ),
    #     proc=lambda x: x+'啦啦啦'
    # ).run()