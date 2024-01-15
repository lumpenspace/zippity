import os
from jinja2 import FileSystemLoader, Template

def default_template():
    with open(os.path.join(os.path.dirname(__file__), 'template.md.jinja'), 'r', encoding='utf-8') as file:
        return file.read()

def render(result, template_file=None):
    if template_file:
        template_loader = FileSystemLoader(searchpath=os.path.dirname(template_file))
        template_env = Template(template_loader)
        template = template_env.get_template(os.path.basename(template_file))
    else:
        template = Template(default_template())
    
    return template.render(result=result)