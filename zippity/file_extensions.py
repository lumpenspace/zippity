import os
import mimetypes

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


def get_file_extension(path: str) -> str or None:
    try:
        return os.path.splitext(path)[1].lower()
    except:
        return None


def get_mime_matcher(extensions=file_extensions) -> callable:
    def get_mime(x):
        mime = (
            mimetypes.guess_type(x, strict=True)[0]
            if get_file_extension(x) in extensions
            else None
        )
        return mime

    return get_mime
