""" Commands
"""

from os.path import join as pjoin
from datetime import datetime as dt
from argparse import ArgumentParser

from .putils import title2slug, OUTPUTDIR, CONF

POST_TEMPLATE = """{yaml_sep}
Title: {title}
Date: {date}
Slug: {slug}
Author: {author}{yaml_sep}


"""


def newpost():
    parser = ArgumentParser()
    parser.add_argument(
        "title", help="Title of post")
    parser.add_argument(
        "-e", "--ext", help="Extension for post")
    args = parser.parse_args()
    date = dt.strftime(dt.today(), '%Y-%m-%d %H:%M')
    slug = title2slug(args.title)
    yaml_sep = '\n---' if args.ext == 'pdc' else ''
    post_fname = pjoin(OUTPUTDIR, f'{slug}.{args.ext}')
    print(f"{post_fname}")
    contents = POST_TEMPLATE.format(
        dict(yml_sep=yaml_sep,
             title=args.title,
             date=date,
             slug=slug,
             author=CONF['AUTHOR']))
    with open(post_fname, 'wt') as fobj:
        fobj.write(contents)
    return post_fname
