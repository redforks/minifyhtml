#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sys import argv
import sys
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

    def __convert_attrs(self, attrs):
        def convert_attr(k, v):
            return k if v is None else k + '="' + v + '"'
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
