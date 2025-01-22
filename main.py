import sys

from analyzer import analyze
from tokenizer import tokenize


def main() -> None:
    expression = sys.argv[1]
    tokens, tokenization_errors = tokenize(expression)
    syntax_analysis_errors = analyze(tokens)
    errors = [*tokenization_errors, *syntax_analysis_errors]
    if errors:
        recognized_tokens = ' '.join(f"TOKEN('{t.lexeme}')" for t in tokens)
        raise ExceptionGroup(
            f"Invalid expression given: '{expression}'\n\t" +
            f"Recognized tokens: {recognized_tokens}\n\t",
            errors
        )
    print(f"Given expression is completely valid: '{expression}'")


if __name__ == "__main__":
    main()
