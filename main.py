import sys

from analyzer import analyze
from tokenizer import tokenize
from utils import format_tokens


def main() -> None:
    expression = sys.argv[1]
    tokens, tokenization_errors = tokenize(expression)
    syntax_analysis_errors = analyze(tokens)
    errors = [*tokenization_errors, *syntax_analysis_errors]
    if errors:
        raise ExceptionGroup(
            f"Invalid expression given: '{expression}'\n\t" +
            f"Recognized tokens: {format_tokens(tokens)}\n\t",
            errors
        )
    print(
        f"Given expression is completely valid: '{expression}'\n"
        f"Recognized tokens: {format_tokens(tokens)}"
    )


if __name__ == "__main__":
    main()
