#!python
# coding:utf-8

import re
import time
from os import path
from collections import OrderedDict

content_folder = 'content'

article_tmpl = '''Title: %(title)s
Date: %(date)s
Tags: %(tags)s
Category: %(category)s
Slug: %(slug)s
Author: %(author)s
Summary: %(summary)s

%(body)s
'''


def check_and_append_new_items(orig_items, new_item_text, list_file):
    new_items = set(new_item_text.split(', ')) - set(orig_items)
    if not new_items:
        return
    with file(list_file, 'a+') as fd:
        for item in new_items:
            print >> fd, '\n%s' % item


def load_list_from_file(filename):
    items = set()
    if path.exists(filename):
        with file(filename, 'r') as fd:
            for ln in fd:
                ln = ln.strip()
                if ln:
                    items.add(ln)
    items = list(items)
    items.sort()
    return items


class HiddenField:
    # A marker for hidden field.
    pass

class Validators:
    @staticmethod
    def can_be_anything(x):
        return

    @staticmethod
    def is_not_empty(x):
        if not x.strip():
            return 'Error: Cannot be empty.'

    @staticmethod
    def is_single_word(x):
        if not re.match('^[0-9a-zA-Z_]+$', x):
            return 'Error: is not single word.'

class Formatters:
    @staticmethod
    def nothing(text):
        return text

    @staticmethod
    def reformat_csv(text):
        seperator_pattern = re.compile(r'[, \t]+')
        items = seperator_pattern.split(text)
        return ', '.join(items)

    @staticmethod
    def strip_spaces(text):
        return text.strip()

article_fields = OrderedDict()
article_fields['title'] = None
article_fields['date'] = None
article_fields['tags'] = None
article_fields['category'] = None
article_fields['slug'] = None
article_fields['author'] = None
article_fields['summary'] = None
article_fields['body'] = None

categories = load_list_from_file('category.list')
tags = load_list_from_file('tags.list')
author = load_list_from_file('author.list')
now =  time.localtime(time.time())

default_hints = dict(
    title=('', '<set title here>', Validators.is_not_empty, Formatters.strip_spaces),
    date=(HiddenField, time.strftime('%Y-%m-%d %H:%M:%S', now), Validators.is_not_empty, Formatters.strip_spaces),
    tags=(', '.join(tags), '', Validators.can_be_anything, Formatters.reformat_csv),
    category=(', '.join(categories), '', Validators.is_single_word, Formatters.strip_spaces),
    slug=(HiddenField, time.strftime('article-%Y%m%d%H%M%S', now), Validators.is_not_empty, Formatters.strip_spaces),
    author=('',author[0], Validators.is_not_empty, Formatters.strip_spaces),
    summary=('', '<set title here>', Validators.can_be_anything, Formatters.strip_spaces),
    body=('', '<set body here>', Validators.can_be_anything, Formatters.strip_spaces),
)


print 'Input article items:'
for k in article_fields:
    hint_info = default_hints.setdefault(k, ('', ''))    
    hint = hint_info[0]
    default_value = hint_info[1]
    validator = hint_info[2]
    formatter = hint_info[3]
    exit_input = False
    while not exit_input:        
        if hint is HiddenField:
            article_fields[k] = default_value
            exit_input = True
            continue
        elif hint:
            if len(default_value) == 0:
                ans = raw_input('\nhint> %s\n%s: ' % (hint, k))
            else:
                ans = raw_input('\nhint> %s\n%s(%s): ' % (hint, k, default_value)) 
        else:
            if len(default_value) == 0:
                ans = raw_input('\n%s: ' % k)
            else:
                ans = raw_input('\n%s(%s): ' % (k, default_value))
        ans = ans.strip()
        if len(ans) == 0:
            ans = default_value
        ans = formatter(ans)
        print ans
        err = validator(ans)
        if err:
            print err
        else:
            article_fields[k] = ans
            exit_input = True        

check_and_append_new_items(categories, article_fields['category'], 'category.list')
check_and_append_new_items(tags, article_fields['tags'], 'tags.list')

article = article_tmpl % article_fields
article_file = path.join(content_folder, time.strftime('article-%Y%m%d%H%M%S.md', now))
print 'Output File: %s' % article_file
if path.exists(article_file):
    print 'Error: file already exists.'

else:
    print '------------------------------------------------------------'
    print article
    print '------------------------------------------------------------'
    print 'Above content will be saved to', article_file
    ans = ''
    while ans not in ('y', 'n'):
        ans = raw_input('Press \'y\' to save. \'n\' to exit: ').lower()

    if ans == 'y':
        with file(article_file, 'w+') as fd:
            fd.write(article)