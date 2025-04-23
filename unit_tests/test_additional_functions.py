import pytest
from json_context_manager_decorator import AddJsonContextManagerDecorator

class TestCreateDataObject:

    @pytest.mark.parametrize(('function_name','error'),
                             [(None,{}), (None,{'error':Exception('test_exception')})])
    def test_create_data_object_data_logging(self, function_name, error):
        assert str(type(AddJsonContextManagerDecorator(
            "TestName").create_data_object(**error))) == "<class 'json_context_manager_decorator.DataLogging'>"

    @pytest.mark.parametrize(('function_name','error','data_args_kwargs'),
                             [('TestName1',{},{}),
                              ('TestName2',{},{'data_args_kwargs': {'int1': 56,
                                                                     'list1': "<class 'list'>"}}),
                              ('TestName3',{'error':Exception('test_exception1')},{}),
                              ('TestName4',{'error':Exception('test_exception2')},
                               {'data_args_kwargs':{'par1': -6, 'par2': "<class 'tuple'>"}})])
    def test_create_data_object_data_logging_decorator(self, function_name, error, data_args_kwargs):
        a = AddJsonContextManagerDecorator("TestName")
        a.function_name = function_name
        assert str(type(a.create_data_object(**error, **data_args_kwargs))) == "<class 'json_context_manager_decorator.DataLoggingDecorator'>"
# Add ruff linter and use format
class TestReturnTransformArgType:

    @pytest.mark.parametrize(('arg','expected'),
                             [(3,3), (45.56,45.56), ('test_str','test_str'),
                              (True,True),((1,2,3),"<class 'tuple'>"),
                              ([1,2,3],"<class 'list'>"), ({1,2,3},"<class 'set'>"),
                              ({'key':1},"<class 'dict'>"), (lambda a : a, '<lambda>'),
                              (range(1), "<class 'range'>")])
    def test_return_transform_arg_type(self,arg,expected):
        assert AddJsonContextManagerDecorator("TestName").return_transform_arg_type(arg) == expected



