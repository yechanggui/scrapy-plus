from __future__ import print_function
import re
import string
from importlib import import_module
from os.path import join, exists, abspath, splitext
from shutil import copytree, ignore_patterns, move
import os
import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.utils.template import render_templatefile, string_camelcase
from scrapy.exceptions import UsageError


TEMPLATES_TO_RENDER = (
    ('scrapy.cfg',),
    ('','.gitignore.tmpl'),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'middlewares.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
)

IGNORE = ignore_patterns('*.pyc', '.svn')


class Command(ScrapyCommand):

    requires_project = False
    default_settings = {'LOG_ENABLED': False}

    def syntax(self):
        return "<project_name>"

    def short_desc(self):
        return "Create new project source of scrapy plus"

    def _is_valid_name(self, project_name):
        def _module_exists(module_name):
            try:
                import_module(module_name)
                return True
            except ImportError:
                return False

        if not re.search(r'^[_a-zA-Z]\w*$', project_name):
            print('Error: Project names must begin with a letter and contain'\
                    ' only\nletters, numbers and underscores')
        elif exists(project_name):
            print('Error: Directory %r already exists' % project_name)
        elif _module_exists(project_name):
            print('Error: Module %r already exists' % project_name)
        else:
            return True
        return False

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-l", "--list", dest="list", action="store_true",
            help="List available project templates")
        parser.add_option("-p", "--p_template", dest="p_template", default="project",
            help="Uses a custom project template.")

    def run(self, args, opts):
        if opts.list:
            self._list_templates()
            return

        project_name = args[0]
        if not self._is_valid_name(project_name):
            self.exitcode = 1
            return

        if len(args) != 1:
            raise UsageError()
        template_file = self._find_template(opts.p_template)
        copytree(template_file, project_name, ignore=IGNORE)
        move(join(project_name, 'module'), join(project_name, project_name))
        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(project_name,
                string.Template(path).substitute(project_name=project_name))
            render_templatefile(tplfile, project_name=project_name,
                ProjectName=string_camelcase(project_name))
        print("New Scrapy project %r, using template directory %r, created in:" % \
              (project_name, self.templates_dir))
        print("    %s\n" % abspath(project_name))
        print("You can start your first spider with:")
        print("    cd %s" % project_name)
        print("    scrapy genspider -t list news_full news.com")

    def _find_template(self, template):
        template_file = join(self.templates_dir, template)
        if exists(template_file):
            return template_file
        print("Unable to find template: %s\n" % template)
        print('Use "scrapy start-plus --list" to see all available templates.')

    def _list_templates(self):
        print("Available templates:")
        for filename in sorted(os.listdir(self.templates_dir)):
            print (filename)

    @property
    def templates_dir(self):
        _templates_base_dir = self.settings['PROJECT_TEMPLATES_DIR'] or \
            join(scrapy.__path__[0], 'templates')
        return join(_templates_base_dir, 'project_templates')
