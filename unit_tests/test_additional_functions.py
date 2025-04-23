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

