""" Commands
"""

from os.path import join as pjoin
from datetime import datetime as dt
from argparse import ArgumentParser
from subprocess import check_call

from .putils import title2slug, OUTPUTDIR, CONF

POST_TEMPLATE = """{yaml_sep}\
Title: {title}
Date: {date}
Slug: {slug}
Author: {author}
{yaml_sep}

"""


def make_newpost(title, ext):
    date = dt.strftime(dt.today(), '%Y-%m-%d %H:%M')
    slug = title2slug(title)
    yaml_sep = '---\n' if ext == 'pdc' else ''
    post_fname = pjoin(OUTPUTDIR, f'{slug}.{ext}')
    author=CONF['AUTHOR']
    contents = POST_TEMPLATE.format(**locals())
    with open(post_fname, 'wt') as fobj:
        fobj.write(contents)
    return post_fname


def newpost_cmd():
    parser = ArgumentParser()
    parser.add_argument(
        "title", help="Title of post")
    parser.add_argument(
        "-e", "--edit", action='store_true',
        help="Whether to edit the file")
    parser.add_argument(
        "-s", "--stage", action='store_true',
        help="Whether to stage the file with Git")
    parser.add_argument(
        "-x", "--ext", default=CONF['DEFAULT_EXT'],
        help="Extension for post")
    args = parser.parse_args()
    out = make_newpost(args.title, args.ext)
    if args.stage:
        check_call(['git', 'add', out])
    if args.edit:
        if CONF['EDIT_CMD'] is None:
            raise RuntimeError(
                'Please set one of EDIT_CMD config var, '
                'GUI_EDITOR env var or EDITOR env var')
        check_call(CONF['EDIT_CMD'] + [out])
    else:
        print(out)
