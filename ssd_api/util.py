import os
from flask import Markup
from flask_misaka import markdown

parent_dir = os.path.dirname(os.path.abspath(__file__))


def get_documentation():
    # Parse Documentation
    with open(os.path.join(parent_dir, '../APIDocumentation.md'), 'r') as f:
    
        content = f.read()
        readme = markdown(content)
        readme += Markup(
            """
            <meta charset=UTF-8>
            <meta name=viewport content="width=device-width,shrink-to-fit=0,
            user-scalable=no,minimum-scale=1,maximum-scale=1">
            <meta name=author content="Tiger Nie">
            <title>SSD API Docs</title>
            <style> html{font-family:"Courier New", Courier, monospace}
            body{padding-left:1rem;padding-right:1rem;} h3{font-weight:bold}
            code{background-color:rgb(246,248,250);display:block;padding:10px;}
            </style>
            """
        )
    return readme