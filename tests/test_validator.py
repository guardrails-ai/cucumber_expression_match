# to run these, run 
# make tests

from guardrails import Guard
import pytest
from validator import cucumber_expression_match
from cucumber_expressions.expression import CucumberExpression
from cucumber_expressions.parameter_type import ParameterType
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry

# We use 'exception' as the validator's fail action,
#  so we expect failures to always raise an Exception
# Learn more about corrective actions here:
#  https://www.guardrailsai.com/docs/concepts/output/#%EF%B8%8F-specifying-corrective-actions
EXPRESSION = "I buy {positive_number} apple(s)/banana(s)/orange(s)"

@pytest.mark.parametrize("good_text", [
    "I buy 0 apples",
    "I buy 1 apple",
    "I buy 1 banana",
    "I buy 2 bananas",
    "I buy 1 orange",
    "I buy 3 oranges",
])
def test_validate_on_success(self, good_text):
  positive_number = ParameterType("positive_number", regexp=r"\d+", type=int)
  validator = CucumberExpressionMatch(self.EXPRESSION, parameter_types=[positive_number], on_fail=OnFailAction.EXCEPTION)
  result = validator.validate(good_text)
  assert isinstance(result, PassResult) is True

@pytest.mark.parametrize("bad_text, reason", [
        ("I buy 2 melons", "Unexpected fruit"),
        ("I buy -10 apples", "Negative number"),
    ])
def test_validate_on_failure(self, bad_text, reason):
  positive_number = ParameterType("positive_number", regexp=r"\d+", type=int)
  validator = CucumberExpressionMatch(self.EXPRESSION, parameter_types=[positive_number], on_fail=OnFailAction.EXCEPTION)
  result = validator.validate(bad_text)
  assert isinstance(result, FailResult) is True
  assert result.error_message == f"Result must match: {self.EXPRESSION}"
  print(f"fix_value: {result.fix_value};")
