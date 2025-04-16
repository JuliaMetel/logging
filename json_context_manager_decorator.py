import inspect
from collections.abc import Callable
from dataclasses import field
from typing import Any
from uuid import uuid4
from pathlib import Path
import json
import time
import types
import dataclasses

LIST_OF_OBJECTS = list()


# Include logic, that each internal function should attach own data to the nearest external function,
# function may have several  internal functions with data, implement and use Stack collection inside
# the storage to understand which function is external in the current moment of time


@dataclasses.dataclass()
class DataLogging:
    name: str
    function_start_time: int
    function_end_time: int
    error: str | None
    inner_function: list = field(default_factory=list, kw_only=True)

    def to_dict(self) -> dict:
        data = {
            'name': self.name,
            'functionStartTime': self.function_start_time,
            'functionEndTime': self.function_end_time,
        }
        if self.error is not None:
            data['error'] = str(self.error)
        data['innerFunctions'] = [i.to_dict() for i in self.inner_function]
        return data

    @staticmethod
    def create_file(data, param_call) -> None:
        with Path(f'./Logs/{param_call}/{uuid4()}.json').open('w') as outfile:
            json.dump(data, outfile)

@dataclasses.dataclass()
class DataLoggingDecorator(DataLogging):
    function_name: str
    function_arguments: dict

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['functionName'] = self.function_name
        data['functionArguments'] = self.function_arguments
        return data


class AddJsonContextManagerDecorator:
    def __init__(self, name: str) -> None:
        self.name = name
        self.error: Exception | None = None
        self.function_start_time: int | None = None
        self.function_end_time: int | None = None
        self.function_name: str | None = None

    def create_data_object(self, error: Exception | None = None, data_args_kwargs: dict |None = None) -> DataLogging | DataLoggingDecorator:
        if self.function_name is None:
            data_obj = DataLogging(self.name, self.function_start_time, self.function_end_time, str(error))
        else:
            data_obj = DataLoggingDecorator(self.name, self.function_start_time, self.function_end_time, str(error),
                                   self.function_name, data_args_kwargs)
        return data_obj

    @staticmethod
    def return_transform_arg_type(arg):
        if isinstance(arg, int | float | str | bool):
            return arg
        if isinstance(arg, tuple | list | set | dict):
            return str(type(arg))
        elif isinstance(arg, (types.FunctionType,type)):
            return arg.__name__
        else:
            return str(arg.__class__)


    @staticmethod
    def parser_args_kwargs_for_json(args: tuple,kwargs: dict,function: Callable[...,Any]) -> dict:
        data = {}
        full_arg_spec = inspect.getfullargspec(function)
        len_full_arg_spec_args = len(full_arg_spec.args)
        len_args = len(args)

        if len_args != 0:
            if len_args == len_full_arg_spec_args:
                for i in range(len_full_arg_spec_args):
                    data[full_arg_spec.args[i]] = AddJsonContextManagerDecorator.return_transform_arg_type(args[i])
            elif len_full_arg_spec_args == 0:
                for x in args:
                    data[full_arg_spec.varargs] = AddJsonContextManagerDecorator.return_transform_arg_type(x)
            elif len_args > len_full_arg_spec_args:
                for i in range(len_full_arg_spec_args):
                    data[full_arg_spec.args[i]] = AddJsonContextManagerDecorator.return_transform_arg_type(args[i])
                else:
                    for k in args[i + 1::]:
                        data[full_arg_spec.varargs] = AddJsonContextManagerDecorator.return_transform_arg_type(k)
            else:
                for i in range(len_args):
                    data[full_arg_spec.args[i]] = AddJsonContextManagerDecorator.return_transform_arg_type(args[i])
                else:
                    for a in range(len(full_arg_spec.defaults)):
                        i += 1
                        data[full_arg_spec.args[i]] = AddJsonContextManagerDecorator.return_transform_arg_type(full_arg_spec.defaults[a])
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                data[key] = AddJsonContextManagerDecorator.return_transform_arg_type(value)
        return data

    def __call__(self, function: Callable[...,Any]) -> Callable[...,Any]:
        self.function_name = function.__name__
        def the_wrapper_around(*args: Any, **kwargs: Any) -> Any:
            data_args_kwargs = self.parser_args_kwargs_for_json(args,kwargs,function)
            self.function_start_time = int(time.time())
            a = self.create_data_object(data_args_kwargs = data_args_kwargs)
            try:
                if len(LIST_OF_OBJECTS) != 0:
                    LIST_OF_OBJECTS[len(LIST_OF_OBJECTS)-1].inner_function.append(a)
                LIST_OF_OBJECTS.append(a)
                result = function(*args, **kwargs)
            except Exception as error:
                a.error = str(error)
                raise
            finally:
                self.function_end_time = a.function_end_time = int(time.time())
                if len(LIST_OF_OBJECTS) == 1:
                    a.create_file(a.to_dict(),'decorator')
                LIST_OF_OBJECTS.pop()
            return result
        return the_wrapper_around

    def __enter__(self) -> None:
        self.function_start_time = int(time.time())

    def __exit__(self,exc_type: type[Exception],exc_value: Exception,traceback: Any) -> None:
        self.function_end_time = int(time.time())
        b = self.create_data_object(error = exc_value)
        b.create_file(b.to_dict(),'context_manager')

@AddJsonContextManagerDecorator('TEST0')
def new3_decorated_func(str01: str, int01: int, list01: list, par01: int = 0, par02: tuple = (1, 2, 3), **r) -> None:
    time.sleep(3)
    print(function2())
    print(function1())
    # raise Exception("My Error0")
    return (print(str01 + str(int01) + str(list01) + str(par01) + str(par02)+'_!'+str(r)))

@AddJsonContextManagerDecorator('7Task')
def function1() -> str:
    time.sleep(3)
    # raise Exception("My Error1")
    return 'I am returned str'

@AddJsonContextManagerDecorator('7Task')
def function2() -> str:
    time.sleep(3)
    function1()
    # raise Exception("My Error1")
    return 'I am returned str1'

new3_decorated_func('test', 56, [5, 6, 90], par01 = -6, s={'1':1,'2':2},ty=9,yui=range(1))
function1()

def new4_decorated_func(str1: str, int1: int, list1: list, par1: int = 0, par2: tuple = (1, 2, 3)) -> None:
    time.sleep(3)
    # raise Exception("My Error")
    return (print(str1 + str(int1) + str(list1) + str(par1) + str(par2)+'__!'))

with AddJsonContextManagerDecorator('TEST'):
    new4_decorated_func('test', 56, [5, 6, 91])
    function2()

