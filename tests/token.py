import unittest

from .util import UrielContainer

class TestToken(unittest.TestCase):
    """
    Tests the Token class.

    """

    def test_empty_string_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        s = ""
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_simple_string_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "foo"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_multi_line_string_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "foo\nbar\nbaz\nquux\n"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_html_string_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "<h1>HTML string</h1>\n<p>Foo</p>\n"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_unidentified_parameter(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{blah}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertTrue(token.has_unidentified_parameter())

    def test_literal_if_tags_not_at_leading_edge(self):
        c = UrielContainer()
        uriel = c.uriel

        s = " {{   value   :   foo   }}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_literal_if_tags_not_at_trailing_edge(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{   value   :   foo   }} "
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_literal_if_tags_not_at_edges(self):
        c = UrielContainer()
        uriel = c.uriel

        s = " {{   value   :   foo   }} "
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("literal", token.type)
        self.assertEqual(s, token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_spaces_inside_tags_ok(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{   value   :   foo   }}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("value", token.type)
        self.assertEqual("foo", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_value(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{value:foo}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("value", token.type)
        self.assertEqual("foo", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_value_unescaped(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{value-unescaped:foo}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("value-unescaped", token.type)
        self.assertEqual("foo", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_include(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{include:default.html}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("include", token.type)
        self.assertEqual("default.html", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_breadcrumbs(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{breadcrumbs:*}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("breadcrumbs", token.type)
        self.assertEqual("*", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_created(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{created:%B %d, %Y}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("created", token.type)
        self.assertEqual("%B %d, %Y", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_modified(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{modified:%B %d, %Y}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("modified", token.type)
        self.assertEqual("%B %d, %Y", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_static_url(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{static-url:foo.jpg}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("static-url", token.type)
        self.assertEqual("foo.jpg", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_static_hash_url(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{static-hash-url:foo.css}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("static-hash-url", token.type)
        self.assertEqual("foo.css", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_rss(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{rss:url}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("rss", token.type)
        self.assertEqual("url", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_node(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{node:blah}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("node", token.type)
        self.assertEqual("blah", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_node_url(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{node-url:foo/bar}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("node-url", token.type)
        self.assertEqual("foo/bar", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_node_name(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{node-name:foo/bar}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("node-name", token.type)
        self.assertEqual("foo/bar", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_node_title(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{node-title:foo/bar}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("node-title", token.type)
        self.assertEqual("foo/bar", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_node_link(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{node-link:foo/bar}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("node-link", token.type)
        self.assertEqual("foo/bar", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_node_list(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{node-list:*}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("node-list", token.type)
        self.assertEqual("*", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_tag_list(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{tag-list:*}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("tag-list", token.type)
        self.assertEqual("*", token.value)
        self.assertFalse(token.has_unidentified_parameter())

    def test_soju(self):
        c = UrielContainer()
        uriel = c.uriel

        s = "{{soju:hello(node)}}"
        token = uriel.Token(s)

        self.assertEqual(s, token.original_string)
        self.assertEqual("soju", token.type)
        self.assertEqual("hello(node)", token.value)
        self.assertFalse(token.has_unidentified_parameter())

