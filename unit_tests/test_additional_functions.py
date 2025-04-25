import pytest
from json_context_manager_decorator import AddJsonContextManagerDecorator


class TestCreateDataObject:
    @pytest.mark.parametrize(
        ("function_name", "error"),
        [(None, {}), (None, {"error": Exception("test_exception")})],
    )
    def test_create_data_object_data_logging(self, function_name, error):
        a = AddJsonContextManagerDecorator("TestName").create_data_object(**error)
        assert str(type(a)) == "<class 'json_context_manager_decorator.DataLogging'>"
        assert a.name == "TestName"
        assert a.start_time is None
        assert a.end_time is None
        assert a.error == error.get("error")
        assert a.inner == []

    @pytest.mark.parametrize(
        ("function_name", "error", "data_args_kwargs"),
        [
            ("TestName1", {}, {}),
            (
                "TestName2",
                {},
                {"data_args_kwargs": {"int1": 56, "list1": "<class 'list'>"}},
            ),
            ("TestName3", {"error": Exception("test_exception1")}, {}),
            (
                "TestName4",
                {"error": Exception("test_exception2")},
                {"data_args_kwargs": {"par1": -6, "par2": "<class 'tuple'>"}},
            ),
        ],
    )
    def test_create_data_object_data_logging_decorator(
        self, function_name, error, data_args_kwargs
    ):
        a = AddJsonContextManagerDecorator("TestName1")
        a.function_name = function_name
        b = a.create_data_object(**error, **data_args_kwargs)
        assert (
            str(type(b))
            == "<class 'json_context_manager_decorator.DataLoggingDecorator'>"
        )
        assert b.name == "TestName1"
        assert b.start_time is None
        assert b.end_time is None
        assert b.error == error.get("error")
        assert b.inner == []
        assert b.function_name == a.function_name
        assert b.function_arguments == data_args_kwargs.get("data_args_kwargs")


class TestReturnTransformArgType:
    @pytest.mark.parametrize(
        ("arg", "expected"),
        [
            (3, 3),
            (45.56, 45.56),
            ("test_str", "test_str"),
            (True, True),
            ((1, 2, 3), "<class 'tuple'>"),
            ([1, 2, 3], "<class 'list'>"),
            ({1, 2, 3}, "<class 'set'>"),
            ({"key": 1}, "<class 'dict'>"),
            (lambda a: a, "<lambda>"),
            (range(1), "<class 'range'>"),
        ],
    )
    def test_return_transform_arg_type(self, arg, expected):
        assert (
            AddJsonContextManagerDecorator("TestName").return_transform_arg_type(arg)
            == expected
        )
