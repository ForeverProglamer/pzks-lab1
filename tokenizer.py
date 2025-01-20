from __future__ import annotations
import re
from dataclasses import dataclass
from enum import StrEnum, auto

DIGIT = r"\d"
LETTER = r"[a-zA-Z]"

ADDITION_OPERATOR = "+"
MINUS_SIGN = "-"
MULTIPLICATION_OPERATOR = "*"
DIVISION_OPERATOR = "/"

OPENING_PARENTHESIS = "("
CLOSING_PARENTHESIS = ")"

WHITESPACE = r"\s"
DECIMAL_NUMBER_SEPARATOR = "."


class TokenType(StrEnum):
    IDENTIFIER = auto()
    ADDITION_OPERATOR = auto()
    MINUS_SIGN = auto()
    MULTIPLICATION_OPERATOR = auto()
    DIVISION_OPERATOR = auto()
    NUMBER = auto()
    OPENING_PARENTHESIS = auto()
    CLOSING_PARENTHESIS = auto()


@dataclass(frozen=True)
class Position:
    start: int
    stop: int


@dataclass
class Token:
    """Object that describes a lexeme."""
    type: TokenType
    lexeme: str
    position: Position


class UnsupportedLexemeError(Exception):
    """Unsupported lexeme encountered."""
    def __init__(self, lexeme_value: str, position: int) -> None:
        super().__init__(
            f"Got unsupported lexeme at position {position}: '{lexeme_value}'"
        )


def tokenize(source_code: str) -> list[Token]:
    """Identify tokens in a source code.

    Raises the `UnsupportedLexemeError` if encounters an unknown or malformed 
    lexeme.
    """
    tokens = []
    pos = 0
    while pos != len(source_code):
        char = source_code[pos]
        if re.match(LETTER, char):
            token = _map_source_code_to_identifier_token(source_code, pos)
            tokens.append(token)
            pos = token.position.stop + 1
        elif re.match(DIGIT, char):
            token = _map_source_code_to_number_token(source_code, pos)
            tokens.append(token)
            pos = token.position.stop + 1
        elif char == OPENING_PARENTHESIS:
            tokens.append(Token(
                type=TokenType.OPENING_PARENTHESIS,
                lexeme=char,
                position=Position(pos,pos)
            ))
            pos += 1
        elif char == CLOSING_PARENTHESIS:
            tokens.append(Token(
                type=TokenType.CLOSING_PARENTHESIS,
                lexeme=char,
                position=Position(pos,pos)
            ))
            pos += 1
        elif char == ADDITION_OPERATOR:
            tokens.append(Token(
                type=TokenType.ADDITION_OPERATOR,
                lexeme=char,
                position=Position(pos,pos)
            ))
            pos += 1
        elif char == MINUS_SIGN:
            tokens.append(Token(
                type=TokenType.MINUS_SIGN,
                lexeme=char,
                position=Position(pos,pos)
            ))
            pos += 1
        elif char == MULTIPLICATION_OPERATOR:
            tokens.append(Token(
                type=TokenType.MULTIPLICATION_OPERATOR,
                lexeme=char,
                position=Position(pos,pos)
            ))
            pos += 1
        elif char == DIVISION_OPERATOR:
            tokens.append(Token(
                type=TokenType.DIVISION_OPERATOR,
                lexeme=char,
                position=Position(pos,pos)
            ))
            pos += 1
        elif re.match(WHITESPACE, char):
            pos += 1
        else:
            raise UnsupportedLexemeError(source_code[pos], pos)
    return tokens


def _map_source_code_to_identifier_token(
    source_code: str, current_position: int
) -> Token:
    pos = current_position + 1
    while pos != len(source_code):
        char = source_code[pos]
        if re.match(LETTER, char):
            pos += 1
        elif re.match(DIGIT, char):
            pos += 1
        else:
            break

    return Token(
        type=TokenType.IDENTIFIER,
        lexeme=source_code[current_position:pos],
        position=Position(start=current_position, stop=pos-1)
    )


def _map_source_code_to_number_token(
    source_code: str, current_position: int
) -> Token:
    pos = current_position + 1
    is_consuming_fractional_part = False
    fractional_digits_consumed_count = 0

    while pos != len(source_code):
        char = source_code[pos]
        if re.match(DIGIT, char):
            pos += 1
            if is_consuming_fractional_part:
                fractional_digits_consumed_count += 1
        elif (
            char == DECIMAL_NUMBER_SEPARATOR and
            not is_consuming_fractional_part
        ):
            pos += 1
            is_consuming_fractional_part = True
        else:
            break

    if (is_consuming_fractional_part and fractional_digits_consumed_count == 0):
        raise UnsupportedLexemeError(
            source_code[current_position:pos], current_position
        )

    return Token(
        type=TokenType.NUMBER,
        lexeme=source_code[current_position:pos],
        position=Position(start=current_position, stop=pos-1)
    )
