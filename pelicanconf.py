#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'Notizen zur Transformation in anarchistische Gesellschaften'
SITEURL = ''

PATH = 'content'

FORMATTED_FIELDS = []  # summary is default
PAGES_PATHS = ['pages']
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = 'texte/{slug}.html'
ARTICLE_SAVE_AS = 'texte/{slug}/index.html'
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
TAG_SAVE_AS = ''

STATIC_PATHS = ['images', 'css', 'javascript', 'documents', 'extra']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

TIMEZONE = 'Europe/Berlin'
DEFAULT_DATE_FORMAT = '%Y/%m'

LOCALE = ('en')
DEFAULT_LANG = 'en'


TYPOGRIFY = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Blogroll
LINKS = ()

SOCIAL = ()

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
