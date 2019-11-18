import os
from flask import Markup
# from flask_misaka import markdown

parent_dir = os.path.dirname(os.path.abspath(__file__))


def get_documentation():
    # # Add header
    # readme = ""
    # readme += Markup(
        # """
        # <meta charset=UTF-8>
        # <meta name=viewport content="width=device-width,shrink-to-fit=0,
        # user-scalable=no,minimum-scale=1,maximum-scale=1">
        # <meta name=author content="Tiger Nie">
        # <title>SSD API Docs</title>
        # <style> html{font-family:"Courier New", Courier, monospace}
        # body{padding-left:1rem;padding-right:1rem;} h3{font-weight:bold}
        # code{background-color:rgb(246,248,250);display:block;padding:10px;}
        # </style>
        # """
    # )

    # # Parse Documentation
    # with open(os.path.join(parent_dir, 'APIDocumentation.md'), 'r') as f:
        
        # readme += markdown(f.read())

    # return readme
    link = '''
        Link to the documentation: <a href='https://github.com/haolinnie/Self-Service-Database-Server/blob/master/ssd_api/APIDocumentation.md'>
        Click me :)</a>
    '''
    return link
