from collections.abc import Callable
from typing import Any
from uuid import uuid4
from pathlib import Path
import json
import time


class AddJsonContextManagerDecorator:
    def __init__(self, name: str) -> None:
        self.name = name
        self.error: Exception | None = None
        self.function_start_time: int | None = None
        self.function_end_time: int | None = None

    def create_json_file(self, error: Exception | None, param_call: str) -> None:
        data = {
            'name': self.name,
            'functionStartTime': self.function_start_time,
            'functionEndTime': self.function_end_time
        }
        if error is not None:
            data['error'] = str(error)
        with Path(f'./Logs/{param_call}/{uuid4()}.json').open('w') as outfile:
            json.dump(data, outfile)

    def __call__(self, function: Callable[...,Any]) -> Callable[...,Any]:
        def the_wrapper_around(*args: Any, **kwargs: Any) -> Any:
            self.function_start_time = int(time.time())
            try:
                result = function(*args, **kwargs)
            except Exception as err:
                self.error = err
                raise
            finally:
                self.function_end_time = int(time.time())
                self.create_json_file(self.error, 'decorator')
            return result
        return the_wrapper_around

    def __enter__(self) -> None:
        self.function_start_time = int(time.time())

    def __exit__(self,exc_type: type[Exception],exc_value: Exception,traceback: Any) -> None:
        self.function_end_time = int(time.time())
        self.create_json_file(exc_value, 'context_manager')


@AddJsonContextManagerDecorator('TEST0')
def new3_decorated_func(str1: str, int1: int, list1: list, par1: int = 0, par2: tuple = (1, 2, 3)) -> None:
    time.sleep(3)
    # raise Exception("My Error0")
    return (print(str1 + str(int1) + str(list1) + str(par1) + str(par2)+'_!'))

new3_decorated_func('test', 56, [5, 6, 90])

def new4_decorated_func(str1: str, int1: int, list1: list, par1: int = 0, par2: tuple = (1, 2, 3)) -> None:
    time.sleep(3)
    # raise Exception("My Error")
    return (print(str1 + str(int1) + str(list1) + str(par1) + str(par2)+'__!'))

with AddJsonContextManagerDecorator('TEST'):
    new4_decorated_func('test', 56, [5, 6, 91])