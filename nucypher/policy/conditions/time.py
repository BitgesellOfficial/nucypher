

import time
from typing import Tuple

from marshmallow import fields, post_load

from nucypher.policy.conditions.base import ReencryptionCondition
from nucypher.policy.conditions.exceptions import InvalidCondition
from nucypher.policy.conditions.lingo import ReturnValueTest
from nucypher.policy.conditions.utils import CamelCaseSchema


class TimeCondition(ReencryptionCondition):
    METHOD = 'timelock'

    class Schema(CamelCaseSchema):
        name = fields.Str()
        method = fields.Str(dump_default="timelock")
        return_value_test = fields.Nested(ReturnValueTest.ReturnValueTestSchema())

        @post_load
        def make(self, data, **kwargs):
            return TimeCondition(**data)

    def __repr__(self) -> str:
        r = f'{self.__class__.__name__}(timestamp={self.return_value_test.value})'
        return r

    def __init__(self, return_value_test: ReturnValueTest, method: str = METHOD):
        if method != self.METHOD:
            raise InvalidCondition(
                f"{self.__class__.__name__} must be instantiated with the {self.METHOD} method."
            )
        self.return_value_test = return_value_test

    @property
    def method(self):
        return self.METHOD

    @property
    def timestamp(self):
        return self.return_value_test.value

    def verify(self, *args, **kwargs) -> Tuple[bool, float]:
        eval_time = time.time()   # system  clock
        return self.return_value_test.eval(data=eval_time), eval_time
