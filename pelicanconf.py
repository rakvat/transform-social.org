#!/usr/bin/env python
# -*- coding: utf-8 -*- #


# THIS IS MOSTLY DEPRECATED as I use a custom script make_html.py to generate the static pages.

from __future__ import unicode_literals

SITENAME = 'Notizen zur Transformation in anarchistische Gesellschaften'
SITEURL='https://transform-social.org'

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
    'extra/android-chrome-192x192.png': {'path': 'android-chrome-192x192.png'},
    'extra/android-chrome-256x256.png': {'path': 'android-chrome-256x256.png'},
    'extra/apple-touch-icon.png': {'path': 'apple-touch-icon.png'},
    'extra/browserconfig.xml': {'path': 'browserconfig.xml'},
    'extra/favicon-16x16.png': {'path': 'favicon-16x16.png'},
    'extra/favicon-32x32.png': {'path': 'favicon-32x32.png'},
    'extra/mstile-150x150.png': {'path': 'mstile-150x150.png'},
    'extra/safari-pinned-tab.svg': {'path': 'safari-pinned-tab.svg'},
    'extra/site.webmanifest': {'path': 'site.webmanifest'},
}

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["sitemap"]

TIMEZONE = 'Europe/Berlin'
DEFAULT_DATE_FORMAT = '%Y/%m'

LOCALE = ('de')
DEFAULT_LANG = 'de'


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

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

