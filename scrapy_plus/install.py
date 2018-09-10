import scrapy
from distutils.dir_util import copy_tree
print scrapy.__path__[0]
print '\n'.join(copy_tree('./commands/',scrapy.__path__[0]+'/commands/'))
print '\n'.join(copy_tree('./templates/',scrapy.__path__[0]+'/templates/'))

