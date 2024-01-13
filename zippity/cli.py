import os
import click
from gitignore_parser import parse_gitignore
from .todo_utils import search_todos_in_directory
from .git_utils import find_gitignore
from .template import render

# TODO: fix tests

@click.command()
@click.argument('source_directory', type=click.Path(exists=True, file_okay=False, readable=True))
@click.option('--file_types', '-t', multiple=True, default=['.py', '.js', '.ts', '.tsx'])
@click.option('--result_file', '-r', type=click.Path(file_okay=True, writable=True), default='./TODO.md')
@click.option('--template_file', '-f', type=click.Path(exists=True, file_okay=True, readable=True))

def main(source_directory:str='./', file_types=['.py', '.js', '.ts', '.tsx'], result_file='./TODO.md', template_file=None):
    # Read the .gitignore file to get a list of patterns to ignore
    gitignore_file = find_gitignore(os.getcwd(), source_directory)
    matches_ignore = parse_gitignore(gitignore_file) if gitignore_file else lambda x: False

    # Search for TODO comments and build the document
    todos = search_todos_in_directory(source_directory, matches_ignore, file_types)

    if (len(todos) == 0):
        print("No TODOs found.")
        exit(0)

    print(f"Found {len(todos)} TODOs.")


    # Write the document to the result file
    with open(result_file, 'w', encoding='utf-8') as result:
        output = render(todos, template_file)
        result.write(output)
    
    exit(0)

if __name__ == '__main__':
    main()
