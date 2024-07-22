"""
File extensions and mime types.
"""

import os
import mimetypes
from typing import Callable

from zippity_py.cli_utils import p

file_extensions = [
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".java",
    ".php",
    ".rb",
    ".rs",
    ".swift",
    ".vb",
    ".vue",
    ".sql",
    ".sh",
    ".ps1",
    ".bat",
    ".cmd",
    ".psm1",
    ".psd1",
    ".ps1xml",
    ".clj",
    ".toml",
    ".json",
    ".json5",
    ".cljc",
    ".cljs",
    ".edn",
    ".lua",
    ".r",
    ".dart",
    ".erl",
    ".ex",
    ".exs",
    ".elm",
    ".hrl",
    ".yaml",
    ".yml",
    ".hs",
    ".sml",
    ".ml",
    ".mli",
    ".cmi",
    ".cmo",
    ".cma",
    ".cmx",
    ".cmt",
    ".cmti",
    ".re",
]


def get_file_extension(path: str) -> str | None:
    """
    Get the file extension of a file.
    """
    try:
        return os.path.splitext(path)[1].lower()
    except (AttributeError, TypeError, ValueError) as e:
        p(f"Error getting file extension for {path}: {e}")
        return None


def get_mime_matcher(extensions: list[str]) -> Callable[[str], str | None]:
    """
    Get a function that matches files against a list of extensions.
    """

    def get_mime(x: str) -> str | None:
        mime: str | None = None
        ext: str | None = get_file_extension(x)
        if ext not in extensions:
            return None
        if ext.endswith(".ts") or ext.endswith(".tsx"):
            # check if there is a const or let in the file
            try:
                with open(x, "r", encoding="utf-8") as f:
                    if "const" in f.read() or "let" in f.read():
                        return "text/typescript"
            except UnicodeDecodeError:
                pass
        else:
            mime = mimetypes.guess_type(x, strict=True)[0]
        return mime

    return get_mime
