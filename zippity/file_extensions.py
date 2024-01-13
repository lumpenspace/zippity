import os

def get_file_extension(path:str):
    return os.path.splitext(path)[1]

def get_language_from_file_extension(path:str):
    extension = get_file_extension(path)
    if extension not in file_extensions:
        return None

    if extension == '.php':
        # except and exit
        raise Exception('PHP is not supported. You don\'t have to live this way.')
    return file_extensions[get_file_extension(path)]

file_extensions = {
    '.py': 'python', '.js': 'javascript', '.jsx': 'jsx', '.ts': 'typescript', '.tsx': 'tsx', '.c': 'c', '.cpp': 'cpp', '.h': 'cpp', '.hpp': 'cpp', '.cs': 'csharp',
    '.go': 'go', '.java': 'java', '.php': 'php', '.rb': 'ruby', '.rs': 'rust', '.swift': 'swift', '.vb': 'vb', '.vue': 'vue', '.html': 'html', '.css': 'css',
    '.scss': 'scss', '.sass': 'sass', '.less': 'less', '.styl': 'stylus','.sql': 'sql','.sh': 'shell','.ps1': 'powershell','.bat': 'batch','.cmd': 'batch',
    '.psm1': 'powershell','.psd1': 'powershell','.ps1xml': 'powershell','.clj': 'clojure','.toml': 'toml','.json': 'json', '.json5': 'json',
    '.cljc': 'clojure','.cljs': 'clojure','.edn': 'clojure','.lua': 'lua','.r': 'r','.dart': 'dart','.erl': 'erlang','.ex': 'elixir','.exs': 'elixir', 
    '.elm': 'elm','.hrl': 'erlang','.yaml': 'yaml','.yml': 'yaml', '.hs': 'haskell','.sml': 'sml','.ml': 'ocaml','.mli': 'ocaml','.cmi': 'ocaml',
    '.cmo': 'ocaml','.cma': 'ocaml','.cmx': 'ocaml','.cmt': 'ocaml','.cmti': 'ocaml','.re': 'reason'
}

