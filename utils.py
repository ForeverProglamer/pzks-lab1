from tokenizer import Token


def format_tokens(tokens: list[Token]) -> str:
    result = []
    for token in tokens:
        token_type = str(token.type).upper()
        words = token_type.split('_')
        if len(words) == 1:
            result.append(f"{words[0]}('{token.lexeme}')")
            continue
        if token_type == 'MINUS_SIGN':
            result.append(f"{words[0]}('{token.lexeme}')")
        if words[1] == 'OPERATOR':
            result.append(f"{words[0][:3]}('{token.lexeme}')")
        if words[1] == 'PARENTHESIS':
            result.append(f"{words[0][0]}{words[1][0]}('{token.lexeme}')")
    return ' '.join(result)

