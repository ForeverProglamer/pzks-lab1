from collections.abc import Sequence
from typing import Callable, ParamSpec
from unittest import TestCase

from tokenizer import (
    Token,
    TokenType,
    Position,
    UnsupportedLexemeError,
    tokenize,
    _map_source_code_to_identifier_token,
    _map_source_code_to_number_token
)

P = ParamSpec("P")


def parametrize(parameter_names: str, parameter_sets: Sequence[tuple]):
    def func_wrapper(func: Callable[..., None]):
        def test_wrapper(self: TestCase, *args: P.args, **_: P.kwargs) -> None:
            names = parameter_names.split(",")
            kw_sets = [dict(zip(names, param_set)) for param_set in parameter_sets]
            for idx, kws in enumerate(kw_sets, 1):
                with self.subTest(msg=f"Test #{idx}", **kws):
                    func(self, *args, **kws)
        return test_wrapper
    return func_wrapper


class TestTokenMappers(TestCase):
    @parametrize(
        "source_code,expected_result",
        [
            ("a", Token(TokenType.IDENTIFIER, "a", Position(0, 0))),
            ("b2", Token(TokenType.IDENTIFIER, "b2", Position(0, 1))),
            ("name1", Token(TokenType.IDENTIFIER, "name1", Position(0, 4))),
        ]
    )
    def test__map_source_code_to_identifier_token(
        self, source_code: str, expected_result: Token
    ) -> None:
        result = _map_source_code_to_identifier_token(source_code, 0)
        self.assertEqual(result.type, expected_result.type)
        self.assertEqual(result.lexeme, expected_result.lexeme)
        self.assertEqual(result.position.stop, expected_result.position.stop)

    @parametrize(
        "source_code,expected_result",
        [
            ("4", Token(TokenType.NUMBER, "4", Position(0, 0))),
            ("42", Token(TokenType.NUMBER, "42", Position(0, 1))),
            ("4.2", Token(TokenType.NUMBER, "4.2", Position(0, 2))),
            ("44.221", Token(TokenType.NUMBER, "44.221", Position(0, 5))),
        ]
    )
    def test__map_source_code_to_number_token(
        self, source_code: str, expected_result: Token,
    ) -> None:
        result = _map_source_code_to_number_token(source_code, 0)
        self.assertEqual(result.type, expected_result.type)
        self.assertEqual(result.lexeme, expected_result.lexeme)
        self.assertEqual(result.position.stop, expected_result.position.stop)

    @parametrize("source_code", [("4.",), ("12..34",)])
    def test__map_source_code_to_number_token_raises_error(
        self, source_code: str
    ) -> None:
        with self.assertRaises(UnsupportedLexemeError):
            _map_source_code_to_number_token(source_code, 0)


class TestTokenize(TestCase):
    def test_skips_whitespaces(self) -> None:
        expected_tokens_count = 3
        self.assertEqual(len(tokenize("  a + b ")), expected_tokens_count)

    @parametrize(
        "source_code,expected_result",
        [
            (
                "(a+b)/c*d",
                [
                    Token(TokenType.OPENING_PARENTHESIS, "(", Position(0,0)),
                    Token(TokenType.IDENTIFIER, "a", Position(1,1)),
                    Token(TokenType.ADDITION_OPERATOR, "+", Position(2,2)),
                    Token(TokenType.IDENTIFIER, "b", Position(3,3)),
                    Token(TokenType.CLOSING_PARENTHESIS, ")", Position(4,4)),
                    Token(TokenType.DIVISION_OPERATOR, "/", Position(5,5)),
                    Token(TokenType.IDENTIFIER, "c", Position(6,6)),
                    Token(TokenType.MULTIPLICATION_OPERATOR, "*", Position(7,7)),
                    Token(TokenType.IDENTIFIER, "d", Position(8,8)),
                ]
            ),
            (
                "sin(x*2)+f1(5.616*t)",
                [
                    Token(TokenType.IDENTIFIER, "sin", Position(0,2)),
                    Token(TokenType.OPENING_PARENTHESIS, "(", Position(3,3)),
                    Token(TokenType.IDENTIFIER, "x", Position(4,4)),
                    Token(TokenType.MULTIPLICATION_OPERATOR, "*", Position(5,5)),
                    Token(TokenType.NUMBER, "2", Position(6,6)),
                    Token(TokenType.CLOSING_PARENTHESIS, ")", Position(7,7)),
                    Token(TokenType.ADDITION_OPERATOR, "+", Position(8,8)),
                    Token(TokenType.IDENTIFIER, "f1", Position(9,10)),
                    Token(TokenType.OPENING_PARENTHESIS, "(", Position(11,11)),
                    Token(TokenType.NUMBER, "5.616", Position(12,16)),
                    Token(TokenType.MULTIPLICATION_OPERATOR, "*", Position(17,17)),
                    Token(TokenType.IDENTIFIER, "t", Position(18,18)),
                    Token(TokenType.CLOSING_PARENTHESIS, ")", Position(19,19)),
                ]
            )
        ]
    )
    def test_identifies_all_supported_lexemes(
        self, source_code: str, expected_result: list[Token]
    ) -> None:
        result = tokenize(source_code)
        for token, expected_token in zip(result, expected_result, strict=True):
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.lexeme, expected_token.lexeme)
            self.assertEqual(token.position.stop, expected_token.position.stop)

    @parametrize(
        "source_code,error_message", [
            ("a$+b", "position 1"),
            ("#-_", "position 0"),
        ]
    )
    def test_raises_error_when_encounters_unsupported_lexeme(
        self, source_code: str, error_message: str
    ) -> None:
        with self.assertRaisesRegex(UnsupportedLexemeError, error_message):
            tokenize(source_code)

