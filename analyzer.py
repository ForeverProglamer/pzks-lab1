import functools as ft

from tokenizer import Token, TokenType

VALID_START_OF_EXPRESSION = {
    TokenType.IDENTIFIER,
    TokenType.NUMBER,
    TokenType.MINUS_SIGN,
    TokenType.OPENING_PARENTHESIS
}

VALID_END_OF_EXPRESSION = {
    TokenType.IDENTIFIER,
    TokenType.NUMBER,
    TokenType.CLOSING_PARENTHESIS
}

OPERATORS = {
    TokenType.ADDITION_OPERATOR,
    TokenType.MINUS_SIGN,
    TokenType.MULTIPLICATION_OPERATOR,
    TokenType.DIVISION_OPERATOR
}

FOLLOWS_OPERAND = {*OPERATORS, TokenType.CLOSING_PARENTHESIS}
FOLLOWS_OPERATOR = {
    TokenType.IDENTIFIER,
    TokenType.NUMBER,
    TokenType.OPENING_PARENTHESIS
}

VALID_FOLLOW_SETS = {
    TokenType.IDENTIFIER: FOLLOWS_OPERAND,
    TokenType.NUMBER: FOLLOWS_OPERAND,
    TokenType.ADDITION_OPERATOR: FOLLOWS_OPERATOR,
    TokenType.MINUS_SIGN: FOLLOWS_OPERATOR,
    TokenType.MULTIPLICATION_OPERATOR: FOLLOWS_OPERATOR,
    TokenType.DIVISION_OPERATOR: FOLLOWS_OPERATOR,
    TokenType.OPENING_PARENTHESIS: {*FOLLOWS_OPERATOR, TokenType.MINUS_SIGN},
    TokenType.CLOSING_PARENTHESIS: {*FOLLOWS_OPERAND}
}


class SyntaxAnalysisError(Exception):
    """Invalid syntax encountered."""


def analyze(tokens: list[Token]) -> list[SyntaxAnalysisError]:
    return SyntaxAnalyzer(tokens).analyze()


class SyntaxAnalyzer:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.errors: list[SyntaxAnalysisError] = []

    def analyze(self) -> list[SyntaxAnalysisError]:
        self._analyze_start_of_expression()
        self._analyze_following_tokens()
        self._analyze_end_of_expression()
        self._analyze_parentheses_usage()
        return self.errors

    def _error(self, message: str) -> None:
        self.errors.append(SyntaxAnalysisError(message))

    def _analyze_start_of_expression(self) -> None:
        token = self.tokens[0]
        if token.type not in VALID_START_OF_EXPRESSION:
            self._error(f"Expression can't start with {token.type!r}")

    def _analyze_end_of_expression(self) -> None:
        token = self.tokens[-1]
        if token.type not in VALID_END_OF_EXPRESSION:
            self._error(f"Expression can't end with {token.type!r}")

    def _analyze_following_tokens(self) -> None:
        def func(prev: Token | None, curr: Token) -> Token:
            if prev and curr.type not in VALID_FOLLOW_SETS[prev.type]:
                self._error(
                    f"{curr.position}: {prev.type!r} can't be followed "
                    f"by {curr.type!r}"
                )
            return curr

        ft.reduce(func, self.tokens, None)

    def _analyze_parentheses_usage(self) -> None:
        stack: list[Token] = []
        for token in self.tokens:
            if token.type == TokenType.OPENING_PARENTHESIS:
                stack.append(token)
            elif token.type == TokenType.CLOSING_PARENTHESIS:
                if not stack:
                    self._error(
                        f"{token.position}: {TokenType.CLOSING_PARENTHESIS!r} "
                        "has never been openned with "
                        f"{TokenType.OPENING_PARENTHESIS!r}"
                    )
                else:
                    stack.pop()

        for token in stack:
            self._error(
                f"{token.position}: {TokenType.OPENING_PARENTHESIS!r} "
                f"has never been closed with {TokenType.CLOSING_PARENTHESIS!r}"
            )
