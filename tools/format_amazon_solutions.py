"""Render compact generator literals as readable teaching solutions.

Only whitespace is changed in C++; Python is rendered from its existing AST.
No rewriting of algorithms or insertion of hints into starters takes place.
"""
from __future__ import annotations

import ast
import re


def python_solution(source: str) -> str:
    return ast.unparse(ast.parse(source)) + "\n"


def cpp_solution(source: str) -> str:
    tokens = re.findall(
        r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[^\n]*|\s+|[^\s{};()"\']+|[{};()]',
        source, re.MULTILINE,
    )
    lines: list[str] = []
    buffer = ""
    indent = 0
    parentheses = 0

    def flush() -> None:
        nonlocal buffer
        if buffer.strip():
            lines.append("    " * indent + buffer.strip())
        buffer = ""

    for token in tokens:
        if token.isspace():
            buffer += " "
        elif token.lstrip().startswith("#"):
            flush()
            lines.append(token.strip())
        elif token.startswith("//"):
            buffer += token
            flush()
        elif token == "(":
            parentheses += 1
            buffer += token
        elif token == ")":
            parentheses -= 1
            buffer += token
        elif token == "{":
            buffer = buffer.rstrip() + " {"
            flush()
            indent += 1
        elif token == "}":
            flush()
            indent = max(0, indent - 1)
            lines.append("    " * indent + "}")
        elif token == ";" and parentheses == 0:
            if not buffer.strip() and lines and lines[-1].endswith("}"):
                lines[-1] += ";"
            else:
                buffer += ";"
                flush()
        else:
            buffer += token
    flush()
    return "\n".join(lines) + "\n"
