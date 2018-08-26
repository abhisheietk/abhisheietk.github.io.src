# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from utils import filters

JINJA_FILTERS = { 'sidebar': filters.sidebar }

AUTHOR = 'Abhishek Bajpai'
SITENAME = 'devnotes'
SITEURL = ''
PATH = 'content'
TIMEZONE = 'Asia/Kolkata'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Google+', 'https://plus.google.com/u/0/+AbhishekBajpaiJi'),
          ('Twitter', 'https://twitter.com/abhisheietk'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
THEME = "pelican-themes/nice-blog"
THEME_COLOR = 'red'
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets']

TYPOGRIFY = True
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'

SIDEBAR_DISPLAY = ['about', 'categories', 'tags']
SIDEBAR_ABOUT = "This is the place holder for my technical endivors."
COPYRIGHT = "Text Here "
