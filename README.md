# clld-morphology-plugin

A plugin for modelling morphology in CLLD apps.

![License](https://img.shields.io/github/license/fmatter/clld-morphology-plugin)
[![Tests](https://img.shields.io/github/actions/workflow/status/fmatter/clld-morphology-plugin/tests.yml?label=tests&branch=main)](https://github.com/fmatter/clld-morphology-plugin/actions/workflows/tests.yml)
[![Codecov](https://img.shields.io/codecov/c/github/fmatter/clld-morphology-plugin)](https://app.codecov.io/gh/fmatter/clld-morphology-plugin/)
[![PyPI](https://img.shields.io/pypi/v/clld-morphology-plugin.svg)](https://pypi.org/project/clld-morphology-plugin)
![Versions](https://img.shields.io/pypi/pyversions/clld-morphology-plugin)

## Models
The [models](/src/clld_morphology_plugin/models.py) largely reflect the structure of the morphological components of the [cldf-ldd](https://github.com/fmatter/cldf-ldd) collection.
Wordforms consist of morphologically segmentable `parts`.
These parts are in turn 


## Markdown
Since this plugin is primarily being developed for an [interactive digital corpus-based grammar](https://github.com/fmatter/indicogram), comments on models are rendered using markdown.
However, it is up to the app developer to choose what markdown you want to use; the templates here assume that the parent mako template provides a function `markdown(request, content)`.
If you want to use the [clld-markdown-plugin](https://github.com/clld/clld-markdown-plugin/), use the following code in your top-level `.mako`:

    <%def name="markdown(request, content)">
        <%from clld_markdown_plugin import markdown%>
        ${markdown(request, content)|n}
    </%def>

to use plain markdown instead:

    <%def name="markdown(request, content)">
        <%from markdown import Markdown%>
        ${Markdown(content)|n}
    </%def>
