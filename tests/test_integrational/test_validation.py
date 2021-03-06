from datetime import datetime
from decimal import Decimal

import pytest

from super_mario import BasePipeline, process_pipe
from super_mario.exceptions import ProgrammingException


def test_allowed_data_types_in_result_is_ok():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'get_data',
            'get_money',
        ]

        @process_pipe
        def get_data():
            return {'a': 1, 'b': 0.2, 'c': 'test', 'd': datetime(2019, 1, 1), 'e': [], 'f': {}, 'g': None}

        @process_pipe
        def get_money(discount: Decimal):
            return {'money': Decimal('100500') * discount}

    result = SimplePipeline().run(discount=Decimal('0.1'))

    assert result == Decimal('10050')


def test_lack_of_pipes_raises_error():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
            'multiply_numbers',
        ]

        @process_pipe
        def sum_numbers(a, b):
            return {'c': a + b}

    with pytest.raises(ProgrammingException):
        SimplePipeline()


def test_complex_data_in_result_raises_error():
    class C:
        pass

    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
        ]

        @process_pipe
        def sum_numbers():
            return {'c': C()}

    with pytest.raises(ProgrammingException):
        SimplePipeline().run()


def test_raises_error_on_no_data_in_context():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
            'sum_numbers_again',
        ]

        @process_pipe
        def sum_numbers(a):
            return {'b': a + 1}

        @process_pipe
        def sum_numbers_again(c):
            return {'d': c + 4}

    with pytest.raises(ProgrammingException):
        SimplePipeline().run()

    with pytest.raises(ProgrammingException):
        SimplePipeline().run(a=1)


def test_raise_error_on_wrong_run_arguments():
    class SimplePipeline(BasePipeline):
        pipeline = [
            'sum_numbers',
        ]
        initial_arguments = [('a', int)]

        @process_pipe
        def sum_numbers(a):
            return {'b': a + 1}

    with pytest.raises(ProgrammingException):
        SimplePipeline().run(b=1)

    with pytest.raises(ProgrammingException):
        SimplePipeline().run(a='1')
