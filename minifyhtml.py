#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sys import argv
import sys, re
from html.parser import HTMLParser

class MinifyHandler(HTMLParser):
    def __init__(self, outfile):
        super(MinifyHandler, self).__init__(strict=True)
        self._outfile = outfile

    def close(self):
        self._outfile.flush()
        super(MinifyHandler, self).close()

    def handle_starttag(self, tag, attrs):
        self.p('<' + tag)
        if attrs:
            self.p(' ', self.__convert_attrs(attrs))
        self.p('>')

    def handle_endtag(self, tag):
        self.p('</', tag, '>')

    def handle_startendtag(self, tag, attrs):
        self.p('<' + tag)
        if attrs:
            self.p(' ', self.__convert_attrs(attrs))
        self.p('/>')

    def handle_data(self, data):
        if '<' in data or '>' in data:
            self.error('bad data, "<" or ">" should be entityref')
        if '&' in data:
            self.error('bad data or entityref, "&" should be use entityref')
        self.p(data)

    def handle_entityref(self, name):
        self.p('&', name, ';')

    def handle_charref(self, name):
        self.p('&#' + name + ';')

    def handle_decl(self, decl):
        self.p('<!', decl, '>')

    def handle_unknown_decl(self, data):
        self.error('Unknown decl')

    def handle_pi(self, data):
        self.error('not implement handle_pi: ' + repr(data))

    def p(self, *args, **kargs):
        print(file=self._outfile, end='', sep='', *args, **kargs)

    _SAFE_ATTR_VALUE = re.compile(r'^[a-z0-9\-.Z:]+$', re.I | re.M)

    def __convert_attrs(self, attrs):
        def convert_value(v):
            if MinifyHandler._SAFE_ATTR_VALUE.match(v):
                return v

            quote = ''
            has_single = "'" in v
            has_double = '"' in v
            if has_single ^ has_double:
                quote = '"' if has_single else "'"
                return quote + v + quote
            else:
                quote = '"'
                return quote + v.replace('"', '&#34;') + quote

        def convert_attr(k, v):
            return k if v is None else k + '=' + convert_value(v)
        return ' '.join(convert_attr(k, v) for k, v in attrs)

if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: {} input-file output-file'.format(argv[0]))
        exit(1)
    else:
        handler = MinifyHandler(open(argv[2], 'w') if len(argv) > 2 else
                sys.stdout)
        handler.feed(open(argv[1], 'r').read())
        handler.close()
