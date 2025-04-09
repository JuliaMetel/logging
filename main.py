from collections.abc import Callable
from typing import Any
from uuid import uuid4
from pathlib import Path
import json
import time
from contextlib import ContextDecorator

def add_json_decorator(param: str) -> Callable[...,Callable[...,Any]]:
    def real_decorator(func: Callable[...,Any]) -> Callable[...,Any]:
        def the_wrapper_around(*args, **kwargs) -> Any:
            function_start_time = int(time.time())
            error = None
            try:
                result = func(*args, **kwargs)
            except Exception as err:
                error = str(err)
                raise
            finally:
                function_end_time = int(time.time())
                data = {
                    'name': param,
                    'functionStartTime': function_start_time,
                    'functionEndTime': function_end_time
                }
                if error is not None:
                    data['error'] = error
                with Path(f'./Logs/decorator/{uuid4()}.json').open('w') as outfile:
                    json.dump(data, outfile)
            return result
        return the_wrapper_around
    return real_decorator

class AddJsonContextManager(ContextDecorator):
    def __init__(self, name: str) -> None:
        self.name = name
        self.function_start_time: int | None = None
        self.function_end_time: int | None = None

    def __enter__(self) -> None:
        self.function_start_time = int(time.time())

    def __exit__(self,exc_type,exc_value,traceback) -> None:
        self.function_end_time = int(time.time())
        data = {
            'name': self.name,
            'functionStartTime': self.function_start_time,
            'functionEndTime': self.function_end_time
        }
        if exc_value is not None:
            data['error'] = str(exc_value)
        with Path(f'./Logs/context_manager/{uuid4()}.json').open('w') as outfile:
            json.dump(data, outfile)

@add_json_decorator('newName03')
def decorated_func(str1: str, int1: int, list1: list, par1=0, par2=(1, 2, 3)):
    time.sleep(3)
    #raise Exception("my error")
    return (print(str1 + str(int1) + str(list1) + str(par1) + str(par2)))

decorated_func('string', 18, [-3,-2,-1])

def new_decorated_func(str1: str, int1: int, list1: list, par1=0, par2=(1, 2, 3)):
    time.sleep(3)
    # raise Exception("My Error")
    return (print(str1 + str(int1) + str(list1) + str(par1) + str(par2)+'!'))

with AddJsonContextManager('NewName03'):
    new_decorated_func('test',56,[5,6,7])

@AddJsonContextManager('NewName04')
def new1_decorated_func(str1: str, int1: int, list1: list, par1=0, par2=(1, 2, 3)):
    time.sleep(4)
    # raise Exception("My Error!")
    return (print(str1 + str(int1) + str(list1) + str(par1) + str(par2)+'!!'))

new1_decorated_func('test1',56,[5,6,7])