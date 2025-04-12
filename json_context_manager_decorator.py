import inspect
from collections.abc import Callable
from typing import Any
from uuid import uuid4
from pathlib import Path
import json
import time


# Modify code and store function name, arguments names and values in same json for decorator

class AddJsonContextManagerDecorator:
    def __init__(self, name: str) -> None:
        self.name = name
        self.error: Exception | None = None
        self.function_start_time: int | None = None
        self.function_end_time: int | None = None
        self.function_name: str | None = None

    def create_json_file(self, error: Exception | None, param_call: str, data_args_kwargs: dict |None = None) -> None:
        data = {
            'name': self.name,
            'functionStartTime': self.function_start_time,
            'functionEndTime': self.function_end_time,
        }
        if self.function_name is not None:
            data['functionName'] = self.function_name
            data['functionArguments'] = data_args_kwargs
        if error is not None:
            data['error'] = str(error)
        with Path(f'./Logs/{param_call}/{uuid4()}.json').open('w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def parser_args_kwargs_for_json(args: tuple,kwargs: dict,function: Callable[...,Any]) -> dict:
        data = {}
        full_arg_spec = inspect.getfullargspec(function)
        len_full_arg_spec_args = len(full_arg_spec.args)
        len_args = len(args)
        if len_args != 0:
            if len_args == len_full_arg_spec_args:
                for i in range(len_full_arg_spec_args):
                    data[full_arg_spec.args[i]] = args[i]
            elif len_full_arg_spec_args == 0:
                data[full_arg_spec.varargs] = args
            elif len_args > len_full_arg_spec_args:
                for i in range(len_full_arg_spec_args):
                    data[full_arg_spec.args[i]] = args[i]
                else:
                    data[full_arg_spec.varargs] = args[i + 1::]
            else:
                for i in range(len_args):
                    data[full_arg_spec.args[i]] = args[i]
                else:
                    for a in range(len(full_arg_spec.defaults)):
                        i += 1
                        data[full_arg_spec.args[i]] = full_arg_spec.defaults[a]
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                data[key] = value
        return data

    def __call__(self, function: Callable[...,Any]) -> Callable[...,Any]:
        self.function_name = function.__name__
        def the_wrapper_around(*args: Any, **kwargs: Any) -> Any:
            data_args_kwargs = self.parser_args_kwargs_for_json(args,kwargs,function)
            self.function_start_time = int(time.time())
            try:
                result = function(*args, **kwargs)
            except Exception as err:
                self.error = err
                raise
            finally:
                self.function_end_time = int(time.time())
                self.create_json_file(self.error, 'decorator', data_args_kwargs)
            return result
        return the_wrapper_around

    def __enter__(self) -> None:
        self.function_start_time = int(time.time())

    def __exit__(self,exc_type: type[Exception],exc_value: Exception,traceback: Any) -> None:
        self.function_end_time = int(time.time())
        self.create_json_file(exc_value, 'context_manager')


@AddJsonContextManagerDecorator('TEST0')
def new3_decorated_func(str01: str, int01: int, list01: list, par01: int = 0, par02: tuple = (1, 2, 3), **r) -> None:
    time.sleep(3)
    # raise Exception("My Error0")
    return (print(str01 + str(int01) + str(list01) + str(par01) + str(par02)+'_!'+str(r)))

new3_decorated_func('test', 56, [5, 6, 90], par01 = -6, s={'1':1,'2':2},ty=9,yui=789)

def new4_decorated_func(str1: str, int1: int, list1: list, par1: int = 0, par2: tuple = (1, 2, 3)) -> None:
    time.sleep(3)
    # raise Exception("My Error")
    return (print(str1 + str(int1) + str(list1) + str(par1) + str(par2)+'__!'))

with AddJsonContextManagerDecorator('TEST'):
    new4_decorated_func('test', 56, [5, 6, 91])
