#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Gary Lee'
SITENAME = "Gary's blog"
SITEURL = 'http://garylee.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = 'tw'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Specify a customized theme, via path relative to the settings file
THEME = "themes/pure"
COVER_IMG_URL = "images/title.png"
PROFILE_IMAGE_URL = "images/head.png"
TAGLINE = "Gary's blah blah blah."

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('github', 'http://github.com/GaryLee/'),
          ('google-plus', 'https://plus.google.com/+GaryLee/'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False