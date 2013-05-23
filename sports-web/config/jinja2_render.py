#!/usr/bin/env python
# coding: utf-8

from jinja2 import Environment, FileSystemLoader

class RenderJinja2:

    postfix = ('.html', 'htm')

    def __init__(self, *a, **kwargs):
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})
        registers = kwargs.pop('registers', {})

        self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)
        self._lookup.globals.update(registers)

    def render(self, path, **kwargs):
        for fix in self.postfix:
            realpath = path + fix
            try:
                t = self._lookup.get_template(realpath)
                return t.render(**kwargs)
            except:
                pass
        raise TemplateNotFound

    def __getattr__(self, name):
        path = name + '.html'
        t = self._lookup.get_template(path)
        return t.render