import re
from abc import ABC
from os import PathLike
from typing import Dict, Generator, Iterable, List, Tuple, Union


class ReportSection(ABC):
    EXECUTION_INPUTS = "Execution Inputs"
    EXECUTION_OUTPUTS = "Execution Outputs"
    EXECUTION_INFO = "Runtime info"
    ENVIRONMENT = "Environment"
    ORIGINAL_INPUTS = "Original Inputs"


rx_star_item = r"^\*\s(\S+)\s:\s(.*)$"


def _lex_report_rst(line_stream: Iterable[str]):
    """
    Lex NiPype report.rst data into tokens.

    Parameters
    ----------
    line_stream : Iterable of lines from report.rst

    Returns
    -------
    List of tuples (token_name, token_value)
    """

    tokens: List[Tuple[str, str]] = []

    line = ""
    last_line = line
    skip = 0

    for line in line_stream:
        if skip > 0:
            skip -= 1
            continue
        if not line:
            break
        line = line[:-1]

        # Headings
        # More efficient with this order of expressions
        # noinspection PyChainedComparisons
        if (
            len(line) > 3
            and line[0] in ("=", "-", "~")
            and line.count(line[0]) == len(line)
        ):
            tokens.append(("header" + line[0], last_line))
            skip = 2
            continue

        # Key value list
        match_star = re.search(rx_star_item, line)
        if match_star is not None:
            tokens.append(("key*", match_star.group(1)))
            tokens.append(("val*", match_star.group(2)))
            continue

        tokens.append(("text", line))

        last_line = line

    # remove last three text tokens before header
    tokens2: List[Tuple[str, str]] = []
    for i in range(len(tokens)):
        tok_name, tok_value = tokens[i]
        if tok_name.startswith("header") and len(tokens2) > 0:
            tokens2.pop()
            for _ in range(2):
                if len(tokens2) == 0:
                    break
                if tokens[-1][0].startswith("text"):
                    tokens2.pop()
        tokens2.append(tokens[i])
    tokens = tokens2

    # merge text tokens into preceding value tokens
    tokens2 = []
    for i in range(len(tokens)):
        tok_name, tok_value = tokens[i]
        if i > 0 and tok_name.startswith("text") and tokens[i - 1][0].startswith("val"):
            tokens2[i - 1] = (tokens2[i - 1][0], tokens2[i - 1][1] + "\n" + tok_value)
        tokens2.append(tokens[i])
    tokens = tokens2

    return tokens


def _parse_report_rst(
    token_stream: Iterable[Tuple[str, str]]
) -> Dict[str, Dict[str, str]]:
    """
    Parse token stream into nested dictionary.

    Parameters
    ----------
    token_stream : Iterable of tuples (token_name, token_value)

    Returns
    -------
    Nested dictionary of sections and key-value pairs.
    """
    document: Dict[str, Dict[str, str]] = {}
    section: Dict[str, str] = {}
    key = ""

    for tok_name, tok_value in token_stream:
        if tok_name.startswith("header"):
            section = {}
            document[tok_value] = section
            continue
        if tok_name.startswith("key"):
            key = tok_value
            continue
        if tok_name.startswith("val"):
            section[key] = tok_value
            continue

    return document


def read_report_rst_str(report_rst: str) -> Dict[str, Dict[str, str]]:
    """
    Read NiPype report.rst data.
    NiPypes RST 'dialect' does not work with any RST library I could find.
    For anyone tempted to make this better: Don't waste your time.

    Parameters
    ----------
    report_rst : report.rst as string.

    Returns
    -------
    Nested dictionary of sections and key-value pairs.
    """

    lines = report_rst.splitlines(True)
    tokens = _lex_report_rst(lines)
    document = _parse_report_rst(tokens)

    return document


def read_report_rst(filename: Union[str, PathLike]) -> Dict[str, Dict[str, str]]:
    """
    Read NiPype report.rst data.
    NiPypes RST 'dialect' does not work with any RST library I could find.
    For anyone tempted to make this better: Don't waste your time.

    Parameters
    ----------
    filename : Filepath to report.rst

    Returns
    -------
    Nested dictionary of sections and key-value pairs.
    """

    def _stream_file_lines(
        filename: Union[str, PathLike]
    ) -> Generator[str, None, None]:
        with open(filename, encoding="utf8") as file:
            while True:
                line = file.readline()
                if not line:
                    return
                yield line

    lines = _stream_file_lines(filename)
    tokens = _lex_report_rst(lines)
    document = _parse_report_rst(tokens)

    return document
