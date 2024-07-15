from typing import Any, Callable, Dict, List, Optional
from cucumber_expressions.expression import CucumberExpression
from cucumber_expressions.parameter_type import ParameterType
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)
import rstr
import pytest

@register_validator(name="guardrails/cucumber_expression_match", data_type="string")
class CucumberExpressionMatch(Validator):
    """Validates that the input string matches a specified cucumber expression.

    **Key Properties**

    | Property                      | Description                                             |
    | ----------------------------- | ------------------------------------------------------- |
    | Name for `format` attribute   | `guardrails/cucumber_expression_match`                  |
    | Supported data types          | `string`                                                |
    | Programmatic fix              | Generate a string that matches this cucumber expression |

    Args:
        expression (str): Cucumber expression to use (as string).
        parameter_types (Optional[List[ParameterType]]): Parameter types to use (optional).
        on_fail (str, Callable): The policy to enact when a validator fails. If `str`, must be one of `reask`, `fix`, `filter`, `refrain`, `noop`, `exception` or `fix_reask`. Otherwise, must be a function that is called when the validator fails.
    """  # noqa

    def __init__(
        self,
        expression: str,
        parameter_types: Optional[List[ParameterType]] = None,
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail)
        parameter_types = parameter_types or []
        self._expression = expression
        self._parameter_type_registry = ParameterTypeRegistry()
        for parameter_type in parameter_types:
            self._parameter_type_registry.define_parameter_type(parameter_type)

    def validate(self, value: Any, metadata: Dict = {}) -> ValidationResult:
        """Validates that the input string matches the specified cucumber expression.

        Args:
            value (Any): The value to validate.
            metadata (Dict): The metadata to validate against.

        Returns:
            ValidationResult: The validation result (PassResult or FailResult).
        """
        this_expression = CucumberExpression(self._expression, self._parameter_type_registry)
        matched = this_expression.match(value)
        if matched is None:
            fix_string = rstr.xeger(this_expression.regexp)
            return FailResult(
                error_message=f"Result must match: {self._expression}",
                fix_value=fix_string,
            )

        return PassResult()