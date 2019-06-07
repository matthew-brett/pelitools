""" Utilities to support commands working on Pelican files
"""

import sys
import os
from os import environ  as env
from os.path import join as pjoin, abspath
import shlex
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


def cmd2list(cmd):
    if sys.platform == 'win32':
        return [cmd]
    return shlex.split(cmd)


INPUTDIR = abspath(os.getcwd())
CONF = _get_conf(INPUTDIR)
OUTPUTDIR = pjoin(INPUTDIR, CONF['PATH'])
if not 'DEFAULT_EXT' in CONF:
    CONF['DEFAULT_EXT'] = 'md'
if not 'EDIT_CMD' in CONF:
    editor = env.get("GUI_EDITOR")
    if editor is None:
        editor = env.get("EDITOR")
    CONF['EDIT_CMD'] = None if editor is None else cmd2list(editor)


def title2slug(title):
    """ Transform title to filename
    """
    slug = title.lower()
    slug = re.sub(r'^[\W]', '', slug)
    slug = re.sub(r'[\W]$', '', slug)
    slug = re.sub(r"[';:\"]", '', slug)
    slug = re.sub(r'[\W]+', '-', slug)
    return slug
