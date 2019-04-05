#!/usr/bin/env python
""" Make a new blog post given a title
"""

from os.path import join as pjoin, split as psplit, abspath, dirname, isfile
import re


def _get_conf(path):
    conf = {}
    conf_file = pjoin(path, 'pelicanconf.py')
    try:
        with open(conf_file, 'rt') as fobj:
            exec(fobj.read(), conf)
    except FileExistsError:
        raise FileExistsError(f'Expecting "pelicanconf.py" file in "{path}"')
    return conf


INPUTDIR = abspath(pjoin(dirname(__file__), '..'))
CONF = _get_conf(INPUTDIR)
OUTPUTDIR = pjoin(INPUTDIR, CONF['PATH'])


def title2slug(title):
    """ Transform title to filename
    """
    slug = title.lower()
    slug = re.sub(r'^[\W]', '', slug)
    slug = re.sub(r'[\W]$', '', slug)
    slug = re.sub(r"[';:\"]", '', slug)
    slug = re.sub(r'[\W]', '-', slug)
    return slug
