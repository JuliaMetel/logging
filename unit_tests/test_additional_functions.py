import pytest
from json_context_manager_decorator import (
    AddJsonContextManagerDecorator,
    DataLogging,
    DataLoggingDecorator,
)


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


class TestParserArgsKwargsForJson:
    def test_zero_variables(self):
        def func():
            pass

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                tuple(), dict(), func
            )
            == dict()
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [((7,), dict(), {"a": 7}), (tuple(), {"a": 7}, {"a": 7})],
    )
    def test_one_variable(self, args, kwargs, expected):
        def func(a):
            return f"{a}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            ((7, 8), dict(), {"a": 7, "b": 8}),
            (tuple(), {"a": 7, "b": 8}, {"a": 7, "b": 8}),
            ((7,), {"b": 8}, {"a": 7, "b": 8}),
        ],
    )
    def test_several_variables(self, args, kwargs, expected):
        def func(a, b):
            return f"{a},{b}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            (tuple(), dict(), dict()),
            ((7,), dict(), {"a": (7,)}),
            ((7, 8, 9), dict(), {"a": (7, 8, 9)}),
        ],
    )
    def test_unlimited_args(self, args, kwargs, expected):
        def func(*a):
            return f"{a}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    def test_one_arg_unlimited_args(self):
        def func(a, *b):
            return f"{a},{b}"

        assert AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
            (7, 8, 9), dict(), func
        ) == {"a": 7, "b": (8, 9)}

    def test_one_arg_unlimited_args_one_kwarg(self):
        def func(a, *b, c):
            return f"{a},{b},{c}"

        assert AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
            (7, 8, 9), {"c": 10}, func
        ) == {"a": 7, "b": (8, 9), "c": 10}

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            (tuple(), dict(), dict()),
            (tuple(), {"a": 5}, {"a": 5}),
            (tuple(), {"a": 5, "b": 7, "c": 10}, {"a": 5, "b": 7, "c": 10}),
        ],
    )
    def test_unlimited_kwargs(self, args, kwargs, expected):
        def func(**a):
            return f"{a}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            ((7,), {"b": 5, "c": 8}, {"a": 7, "b": 5, "c": 8}),
            (tuple(), {"b": 5, "a": 7, "c": 8}, {"b": 5, "a": 7, "c": 8}),
        ],
    )
    def test_one_arg_unlimited_kwargs(self, args, kwargs, expected):
        def func(a, **b):
            return f"{a},{b}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            (tuple(), dict(), dict()),
            ((7, 8), dict(), {"a": (7, 8)}),
            (tuple(), {"c": 3}, {"c": 3}),
            ((7, 8), {"c": 3, "b": 0}, {"a": (7, 8), "c": 3, "b": 0}),
        ],
    )
    def test_unlimited_args_unlimited_kwargs(self, args, kwargs, expected):
        def func(*a, **b):
            return f"{a},{b}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    def test_one_arg_unlimited_args_unlimited_kwargs(self):
        def func(a, *b, **c):
            return f"{a},{b},{c}"

        assert AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
            (7, 8), {"k": 0}, func
        ) == {"a": 7, "b": (8,), "k": 0}

    def test_unlimited_args_one_kwarg_unlimited_kwargs(self):
        def func(*a, b, **c):
            return f"{a},{b},{c}"

        assert AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
            (7, 8), {"b": 0, "m": 1}, func
        ) == {"a": (7, 8), "b": 0, "m": 1}

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            ((7,), {"c": 3}, {"a": 7, "c": 3}),
            (
                (1, 2, 3),
                {"c": 4, "k": 5, "m": 6},
                {"a": 1, "b": (2, 3), "c": 4, "k": 5, "m": 6},
            ),
        ],
    )
    def test_one_arg_unlimited_args_one_kwarg_unlimited_kwargs(
        self, args, kwargs, expected
    ):
        def func(a, *b, c, **d):
            return f"{a},{b},{c},{d}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            (tuple(), dict(), {"a": 1, "b": 2, "c": 3}),
            ((7,), dict(), {"a": 7, "b": 2, "c": 3}),
            ((7, 8, 9), dict(), {"a": 7, "b": 8, "c": 9}),
            (tuple(), {"b": 4}, {"a": 1, "b": 4, "c": 3}),
            (tuple(), {"b": 1, "c": 2, "a": 3}, {"a": 3, "b": 1, "c": 2}),
            ((4,), {"c": 0}, {"a": 4, "b": 2, "c": 0}),
        ],
    )
    def test_several_default_variables(self, args, kwargs, expected):
        def func(a=1, b=2, c=3):
            return f"{a},{b},{c}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            ((4,), dict(), {"a": 4, "b": 3}),
            ((4, 5, 6, 7), dict(), {"a": 4, "b": 5, "c": (6, 7)}),
        ],
    )
    def test_one_arg_one_default_unlimited_args(self, args, kwargs, expected):
        def func(a, b=3, *c):
            return f"{a},{b},{c}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            (tuple(), {"d": 3, "k": 4}, {"a": 1, "b": 2, "d": 3, "k": 4}),
            (tuple(), {"d": 3, "b": 6, "k": 4}, {"a": 1, "b": 6, "d": 3, "k": 4}),
            ((7,), {"k": 4}, {"a": 7, "b": 2, "k": 4}),
            ((6,), {"k": 4, "b": 9}, {"a": 6, "b": 9, "k": 4}),
        ],
    )
    def test_two_default_unlimited_kwargs(self, args, kwargs, expected):
        def func(a=1, b=2, **c):
            return f"{a},{b},{c}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            (tuple(), dict(), {"a": 1, "c": 7}),
            ((2, 3, 4), dict(), {"a": 2, "b": (3, 4), "c": 7}),
            (tuple(), {"c": 8}, {"a": 1, "c": 8}),
            (
                (2, 3, 4),
                {"k": 5, "m": 1, "c": 6},
                {"a": 2, "b": (3, 4), "c": 6, "k": 5, "m": 1},
            ),
            (tuple(), {"k": 5, "m": 3}, {"a": 1, "c": 7, "k": 5, "m": 3}),
        ],
    )
    def test_one_default_arg_unlimited_args_one_default_kwarg_unlimited_kwargs(
        self, args, kwargs, expected
    ):
        def func(a=1, *b, c=7, **d):
            return f"{a},{b},{c},{d}"

        assert (
            AddJsonContextManagerDecorator.parser_args_kwargs_for_json(
                args, kwargs, func
            )
            == expected
        )


class TestToDict:
    @pytest.mark.parametrize(
        ("name", "start_time", "end_time", "error", "inner", "expected"),
        [
            (
                "Name1",
                12345,
                67890,
                None,
                dict(),
                {
                    "name": "Name1",
                    "startTime": 12345,
                    "endTime": 67890,
                    "inner": list(),
                },
            ),
            (
                "Name2",
                12346,
                67891,
                Exception("Test exception"),
                dict(),
                {
                    "name": "Name2",
                    "startTime": 12346,
                    "endTime": 67891,
                    "error": "Test exception",
                    "inner": list(),
                },
            ),
            (
                "Name3",
                12347,
                67892,
                None,
                {
                    "inner": [
                        DataLogging(
                            name="TEST_3",
                            start_time=1745853851,
                            end_time=1745853854,
                            error=None,
                            inner=[
                                DataLogging(
                                    name="7Task",
                                    start_time=1745853851,
                                    end_time=1745853854,
                                    error=None,
                                    inner=[],
                                )
                            ],
                        )
                    ]
                },
                {
                    "name": "Name3",
                    "startTime": 12347,
                    "endTime": 67892,
                    "inner": [
                        {
                            "name": "TEST_3",
                            "startTime": 1745853851,
                            "endTime": 1745853854,
                            "inner": [
                                {
                                    "name": "7Task",
                                    "startTime": 1745853851,
                                    "endTime": 1745853854,
                                    "inner": [],
                                }
                            ],
                        }
                    ],
                },
            ),
            (
                "Name4",
                12348,
                67893,
                Exception("Test exception 1"),
                {
                    "inner": [
                        DataLogging(
                            name="TEST_4",
                            start_time=1745853851,
                            end_time=1745853854,
                            error=None,
                            inner=[],
                        )
                    ]
                },
                {
                    "name": "Name4",
                    "startTime": 12348,
                    "endTime": 67893,
                    "error": "Test exception 1",
                    "inner": [
                        {
                            "name": "TEST_4",
                            "startTime": 1745853851,
                            "endTime": 1745853854,
                            "inner": [],
                        }
                    ],
                },
            ),
            (
                "Name5",
                12351,
                67896,
                None,
                {
                    "inner": [
                        DataLoggingDecorator(
                            name="TEST_7",
                            start_time=1745855778,
                            end_time=1745855781,
                            error=None,
                            inner=[],
                            function_name="function03",
                            function_arguments={"test": 3},
                        )
                    ]
                },
                {
                    "name": "Name5",
                    "startTime": 12351,
                    "endTime": 67896,
                    "inner": [
                        {
                            "name": "TEST_7",
                            "startTime": 1745855778,
                            "endTime": 1745855781,
                            "inner": [],
                            "functionName": "function03",
                            "functionArguments": {"test": 3},
                        }
                    ],
                },
            ),
        ],
    )
    def test_for_class_data_logging(
        self, name, start_time, end_time, error, inner, expected
    ):
        assert (
            DataLogging(name, start_time, end_time, error, **inner).to_dict()
            == expected
        )

    @pytest.mark.parametrize(
        (
            "name",
            "start_time",
            "end_time",
            "error",
            "function_name",
            "function_arguments",
            "inner",
            "expected",
        ),
        [
            (
                "Name5",
                12349,
                67894,
                Exception("Test exception 2"),
                "Function's name",
                {"str": "test", "list01": "<class 'list'>"},
                {
                    "inner": [
                        DataLoggingDecorator(
                            name="TEST_5",
                            start_time=1745855779,
                            end_time=1745855782,
                            error=None,
                            inner=[],
                            function_name="function02",
                            function_arguments={},
                        )
                    ]
                },
                {
                    "name": "Name5",
                    "startTime": 12349,
                    "endTime": 67894,
                    "error": "Test exception 2",
                    "functionName": "Function's name",
                    "functionArguments": {"str": "test", "list01": "<class 'list'>"},
                    "inner": [
                        {
                            "name": "TEST_5",
                            "startTime": 1745855779,
                            "endTime": 1745855782,
                            "inner": [],
                            "functionName": "function02",
                            "functionArguments": {},
                        }
                    ],
                },
            ),
            (
                "Name6",
                12350,
                67895,
                None,
                "Function's name 1",
                {},
                {
                    "inner": [
                        DataLogging(
                            name="TEST_6",
                            start_time=1745855779,
                            end_time=1745855782,
                            error=None,
                            inner=[],
                        )
                    ]
                },
                {
                    "name": "Name6",
                    "startTime": 12350,
                    "endTime": 67895,
                    "functionName": "Function's name 1",
                    "functionArguments": {},
                    "inner": [
                        {
                            "name": "TEST_6",
                            "startTime": 1745855779,
                            "endTime": 1745855782,
                            "inner": [],
                        }
                    ],
                },
            ),
        ],
    )
    def test_for_class_data_logging_decorator(
        self,
        name,
        start_time,
        end_time,
        error,
        function_name,
        function_arguments,
        inner,
        expected,
    ):
        assert (
            DataLoggingDecorator(
                name,
                start_time,
                end_time,
                error,
                function_name,
                function_arguments,
                **inner,
            ).to_dict()
            == expected
        )
