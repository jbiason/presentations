#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Build the JSON with the list of presentions."""

import os
import re
import logging
import argparse
import datetime
import json

DATA_BACKGROUND = re.compile(r"data-background=['\"](.*?)['\"]")
PRES_TITLE = re.compile(r"<h1.*?>(.*?)</h1>")


def retrieve_presentation_info(filename):
    """Open a file and try to retrieve the presentation information, like
    background-image and title.
    """
    result = (None, None)
    content = ''
    with open(filename) as data:
        content = data.read()

    image = DATA_BACKGROUND.search(content)
    title = PRES_TITLE.search(content)

    if content and image and title:
        logging.debug('Image for %s = %s', filename, image.group(1))
        logging.debug('Title for %s = %s', filename, title.group(1))
        result = (image.group(1), title.group(1))
    elif not content:
        logging.debug('%s has no content', filename)
    elif not image:
        logging.debug('%s has no image', filename)
    else:
        logging.debug('%s has no title', filename)
    return result


def check_presentations(file_list):
    """Check if the any of the files in the file list are presentations."""
    result = []
    for filename in file_list:
        logging.debug('-->')
        if not filename.endswith('.html'):
            # presentations are HTML only
            logging.debug('%s ignored, not an HTML file', filename)
            continue

        (image, title) = retrieve_presentation_info(filename)
        if image and title:
            stat_info = os.stat(filename)
            date = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            logging.debug('Modified date = %s', date)

            result.append({'presentation': filename,
                           'title': title,
                           'image': image,
                           'changed': date.strftime('%Y-%m-%d %H:%M:%S')})
        else:
            logging.debug('Missing information on %s', filename)
    return result


def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug',
                        action='store_const',
                        dest='debug',
                        default=False,
                        const=True,
                        help='Enable debugging messages')
    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level)

    for (root, _, files) in os.walk('.'):
        if not root == '.':
            # only files in the current directly will be checked
            continue

        content = check_presentations(files)
        # holy shit, talk about abusing Python internals
        content.sort(cmp=lambda x, y: -1 if x['title'] < y['title'] else 1)
        with open('index.json', 'w') as output:
            output.write(json.dumps(content))

    return


if __name__ == "__main__":
    main()
