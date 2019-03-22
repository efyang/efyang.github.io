#!/usr/bin/python3
import jinja2
import sys

templateLoader = jinja2.FileSystemLoader(searchpath=sys.argv[1])
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "index.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render()  # this is where to put args to the template renderer

print(outputText)
