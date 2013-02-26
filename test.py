#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from io import StringIO
from html.parser import HTMLParseError
from minifyhtml import MinifyHandler

def minify(html):
    with StringIO('') as out:
        handler = MinifyHandler(out)
        handler.feed(html)
        handler.close()
        return out.getvalue()

class TestMinify(unittest.TestCase):
    def test_empty(self):
        self._same('')

    def test_tag_only(self):
        self._same('<foo></foo>')
        self._same('<foo>')
        self._same('<foo/>')
        self._assert('<foo>', '<foo >')
        self._assert('<foo>', '<foo\n\t >')

    def test_bad_format(self):
        def bad_format(html):
            with self.assertRaises(HTMLParseError):
                minify(html)

        bad_format('foo>')
        bad_format('<')
        bad_format('>')
        bad_format('<>')
        bad_format('<>>')
        bad_format('<foo')
        bad_format('&')
        bad_format('&nbsp')
        bad_format('<!-- no comment ending')
        bad_format('no commend begging -->')

    def test_text(self):
        self._same('abc')

    def test_entityref(self):
        self._same('ab&nbsp;c')
        self._same('&nbsp;')
        self._same('&#62;')
        self._same('&#x3E;')

    def test_comment(self):
        self._assert('', '<!-- comment -->')

    def test_decl(self):
        self._same('<!DOCTYPE html>')

    def test_attribute(self):
        self._same('<foo foo="bar">')
        self._same('<foo foo>')
        self._same('<foo foo foo="bar">')

    def _assert(self, expected, html):
        self.assertEqual(expected, minify(html))

    def _same(self, html):
        self._assert(html, html)

if __name__ == '__main__':
    unittest.main()
