import itertools as it
from unittest import TestCase

from analyzer import analyze
from test_tokenizer import parametrize
from tokenizer import TokenType, tokenize

OPERATION_TO_TOKEN_TYPE = {
    "+": TokenType.ADDITION_OPERATOR,
    "-": TokenType.MINUS_SIGN,
    "*": TokenType.MULTIPLICATION_OPERATOR,
    "/": TokenType.DIVISION_OPERATOR,
}

EMPTY_PARENTHESES_ERROR_MSG = (
    "Token(type='opening_parenthesis') can't be followed by "
    "Token(type='closing_parenthesis')"
)
CLOSING_PARENTHESIS_ERROR_MSG = ( 
    "')' has never been openned with '('"
)
OPENING_PARENTHESIS_ERROR_MSG = (
    "'(' has never been closed with ')'"
)

class TestAnalyzer(TestCase):
    def test_expression_can_not_start_with_closing_parenthesis(self) -> None:
        tokens, _ = tokenize(")a+b")
        errors = analyze(tokens)
        self.assertTrue(str(TokenType.CLOSING_PARENTHESIS) in str(errors[0]))

    @parametrize(
        "expression,operator", [
            (f"{op}a+b", OPERATION_TO_TOKEN_TYPE[op])
            for op in '+*/'
        ]
    )
    def test_expression_can_not_start_with_algebraic_operations(
        self, expression: str, operator: TokenType
    ) -> None:
        # Well, minus sign is allowed as unary operation
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(operator) in str(errors[0]))

    @parametrize(
        "expression,operator", [
            (f"a+b{op}", OPERATION_TO_TOKEN_TYPE[op])
            for op in '+-*/'
        ]
    )
    def test_expression_can_not_end_with_algebraic_operations(
        self, expression: str, operator: TokenType
    ) -> None:
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(operator) in str(errors[0]))

    @parametrize(
        "expression,operator", [
            (f"a{op1}{op2}b", OPERATION_TO_TOKEN_TYPE[op2])
            for op1, op2 in it.product("+-*/", repeat=2)
        ]
    )
    def test_expression_can_not_contain_double_algebraic_operations(
        self, expression: str, operator: TokenType
    ) -> None:
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(operator) in str(errors[0]))

    @parametrize(
        "expression,last_valid_token_type", [
            ("a+b(c-d)", TokenType.IDENTIFIER),
            ("a+4.31(c-d)", TokenType.NUMBER),
        ]
    )
    def test_expression_must_contain_operations_before_parentheses(
        self, expression: str, last_valid_token_type: TokenType
    ) -> None:
        # Except for start of expression, of course
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(last_valid_token_type) in str(errors[0]))

    @parametrize(
        "expression,operator", [
            (f"({op}a+b)", OPERATION_TO_TOKEN_TYPE[op])
            for op in "+*/"
        ]
    )
    def test_expression_can_not_contain_operations_right_after_opening_parenthesis(
        self, expression: str, operator: TokenType
    ) -> None:
        # Except for unary minus
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(operator) in str(errors[0]))

    @parametrize(
        "expression,operator", [
            (f"(a+b){op}", OPERATION_TO_TOKEN_TYPE[op])
            for op in "+-*/"
        ]
    )
    def test_end_of_expression_can_not_contain_operations_right_before_closing_parenthesis(
        self, expression: str, operator: TokenType
    ) -> None:
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(operator) in str(errors[0]))

    @parametrize(
        "expression,error_message",
        [
            ("(a+b))", CLOSING_PARENTHESIS_ERROR_MSG),
            ("((a+b)", OPENING_PARENTHESIS_ERROR_MSG)
        ]
    )
    def test_expression_can_not_contain_odd_number_of_parentheses(
        self, expression: str, error_message: str
    ) -> None:
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(error_message) in str(errors[0]))

    @parametrize(
        "expression,error_message",
        [
            (expression, EMPTY_PARENTHESES_ERROR_MSG)
            for expression in ["()", "a+()", "a+(b+())"]
        ]
    )
    def test_expression_can_not_contain_empty_parentheses(
        self, expression: str, error_message: str
    ) -> None:
        tokens, _ = tokenize(expression)
        errors = analyze(tokens)
        self.assertTrue(str(error_message) in str(errors[0]))

