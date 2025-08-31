import os
import sys
import importlib
import unittest

from .util import UrielContainer
from .util import TempDir
from .util import get_datetime_from_date_str

class TestPage(unittest.TestCase):
    """
    Tests the Page class.

    """

    def test_constructor_basic(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertFalse(page.use_canonical_url)

    def test_constructor_use_canonical_url_false(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root, use_canonical_url=False)

            self.assertFalse(page.use_canonical_url)

    def test_constructor_use_canonical_url_true(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root, use_canonical_url=False)

            self.assertFalse(page.use_canonical_url)

    def test_line_error_without_template(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.line_error(uriel.Token("{{value:foo}}"), "bar", raise_exception=False)

            self.assertEqual(4, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{value:foo}}'", c.stderr[2])
            self.assertEqual("      bar", c.stderr[3])

    def test_line_error_with_template(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("default.html", root.get_path(), False)

            page.line_error(uriel.Token("{{value:foo}}"), "bar", raise_exception=False)

            self.assertEqual(5, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/default.html", c.stderr[2])
            self.assertEqual("      '{{value:foo}}'", c.stderr[3])
            self.assertEqual("        bar", c.stderr[4])

    def test_line_error_with_multiple_templates(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("a.html", root.get_path(), False)
            page.template_stack.push("b.html", root.get_path(), False)
            page.template_stack.push("c.html", root.get_path(), False)

            page.line_error(uriel.Token("{{value:foo}}"), "bar", raise_exception=False)

            self.assertEqual(7, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/a.html", c.stderr[2])
            self.assertEqual("    templates/b.html", c.stderr[3])
            self.assertEqual("    templates/c.html", c.stderr[4])
            self.assertEqual("      '{{value:foo}}'", c.stderr[5])
            self.assertEqual("        bar", c.stderr[6])

    def test_line_error_without_template_with_node_body_semaphore(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.node_body_semaphore = 1
            page.line_error(uriel.Token("{{value:foo}}"), "bar", raise_exception=False)

            self.assertEqual(4, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{value:foo}}'", c.stderr[2])
            self.assertEqual("      bar", c.stderr[3])

    def test_line_error_with_template_with_node_body_semaphore(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("default.html", root.get_path(), False)

            page.node_body_semaphore = 1
            page.line_error(uriel.Token("{{value:foo}}"), "bar", raise_exception=False)

            self.assertEqual(6, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/default.html", c.stderr[2])
            self.assertEqual("      nodes/index", c.stderr[3])
            self.assertEqual("        '{{value:foo}}'", c.stderr[4])
            self.assertEqual("          bar", c.stderr[5])

    def test_line_error_with_multiple_templates_with_node_body_semaphore(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("a.html", root.get_path(), False)
            page.template_stack.push("b.html", root.get_path(), False)
            page.template_stack.push("c.html", root.get_path(), False)

            page.node_body_semaphore = 1
            page.line_error(uriel.Token("{{value:foo}}"), "bar", raise_exception=False)

            self.assertEqual(8, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/a.html", c.stderr[2])
            self.assertEqual("    templates/b.html", c.stderr[3])
            self.assertEqual("    templates/c.html", c.stderr[4])
            self.assertEqual("      nodes/index", c.stderr[5])
            self.assertEqual("        '{{value:foo}}'", c.stderr[6])
            self.assertEqual("          bar", c.stderr[7])

    def test_line_error_without_template_raise_exception(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertEqual(3, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{value:foo}}'", c.stderr[2])

    def test_line_error_with_template_raise_exception(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("default.html", root.get_path(), False)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertEqual(4, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/default.html", c.stderr[2])
            self.assertEqual("      '{{value:foo}}'", c.stderr[3])

    def test_line_error_with_multiple_templates_raise_exception(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("a.html", root.get_path(), False)
            page.template_stack.push("b.html", root.get_path(), False)
            page.template_stack.push("c.html", root.get_path(), False)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertEqual(6, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/a.html", c.stderr[2])
            self.assertEqual("    templates/b.html", c.stderr[3])
            self.assertEqual("    templates/c.html", c.stderr[4])
            self.assertEqual("      '{{value:foo}}'", c.stderr[5])

    def test_line_error_without_template_raise_exception_called_twice(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertEqual(3, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{value:foo}}'", c.stderr[2])

    def test_line_error_with_template_raise_exception_called_twice(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("default.html", root.get_path(), False)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertEqual(4, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/default.html", c.stderr[2])
            self.assertEqual("      '{{value:foo}}'", c.stderr[3])

    def test_line_error_with_multiple_templates_raise_exception_called_twice(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("a.html", root.get_path(), False)
            page.template_stack.push("b.html", root.get_path(), False)
            page.template_stack.push("c.html", root.get_path(), False)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertRaises(
                uriel.UrielError,
                page.line_error,
                uriel.Token("{{value:foo}}"),
                "bar",
                raise_exception=True)

            self.assertEqual(6, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/a.html", c.stderr[2])
            self.assertEqual("    templates/b.html", c.stderr[3])
            self.assertEqual("    templates/c.html", c.stderr[4])
            self.assertEqual("      '{{value:foo}}'", c.stderr[5])

    def test_node_body_loop_error_no_templates(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.node_body_loop_error,
                uriel.Token("{{node:body}}"))

            self.assertEqual(3, len(c.stderr))
            self.assertEqual("node body include loop error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{node:body}}'", c.stderr[2])

    def test_node_body_loop_error_one_template(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("default.html", root.get_path(), False)

            self.assertRaises(
                uriel.UrielError,
                page.node_body_loop_error,
                uriel.Token("{{node:body}}"))

            self.assertEqual(5, len(c.stderr))
            self.assertEqual("node body include loop error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/default.html", c.stderr[2])
            self.assertEqual("      nodes/index", c.stderr[3])
            self.assertEqual("        '{{node:body}}'", c.stderr[4])

    def test_node_body_loop_error_multiple_templates(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            page.template_stack.push("a.html", root.get_path(), False)
            page.template_stack.push("b.html", root.get_path(), False)
            page.template_stack.push("c.html", root.get_path(), False)

            self.assertRaises(
                uriel.UrielError,
                page.node_body_loop_error,
                uriel.Token("{{node:body}}"))

            self.assertEqual(7, len(c.stderr))
            self.assertEqual("node body include loop error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    templates/a.html", c.stderr[2])
            self.assertEqual("    templates/b.html", c.stderr[3])
            self.assertEqual("    templates/c.html", c.stderr[4])
            self.assertEqual("      nodes/index", c.stderr[5])
            self.assertEqual("        '{{node:body}}'", c.stderr[6])

    def test_tokenize_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(Exception, page.tokenize, None)

    def test_tokenize_empty_string(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            expected = []
            actual = page.tokenize("")

            self.assertEqual(expected, actual)

    def test_tokenize_literal_string(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            expected = [uriel.Token("lemon curry")]
            actual = page.tokenize("lemon curry")

            self.assertEqual(expected, actual)

    def test_tokenize_parameter(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            expected = [uriel.Token("{{value:foo}}")]
            actual = page.tokenize("{{value:foo}}")

            self.assertEqual(expected, actual)

    def test_tokenize_complex(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            expected = [
                uriel.Token(" <p>"),
                uriel.Token("{{ value : foo }}"),
                uriel.Token("</p> "),
                uriel.Token("{{ soju : hello() }}"),
                uriel.Token(" ")
            ]
            actual = page.tokenize(" <p>{{ value : foo }}</p> {{ soju : hello() }} ")

            self.assertEqual(expected, actual)

            self.assertEqual(uriel.Token.LITERAL, actual[0].type)
            self.assertEqual(" <p>", actual[0].value)

            self.assertEqual(uriel.Token.VALUE, actual[1].type)
            self.assertEqual("foo", actual[1].value)

            self.assertEqual(uriel.Token.LITERAL, actual[2].type)
            self.assertEqual("</p> ", actual[2].value)

            self.assertEqual(uriel.Token.SOJU, actual[3].type)
            self.assertEqual("hello()", actual[3].value)

            self.assertEqual(uriel.Token.LITERAL, actual[4].type)
            self.assertEqual(" ", actual[4].value)

    def test_tokenize_parameter_incomplete(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            expected = [uriel.Token("{{value:foo}")]
            actual = page.tokenize("{{value:foo}")

            self.assertEqual(expected, actual)

            self.assertEqual(uriel.Token.LITERAL, actual[0].type)
            self.assertEqual("{{value:foo}", actual[0].value)

    def test_text_to_html_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(Exception, page.text_to_html, None)

    def test_text_to_html_empty_string(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("", page.text_to_html(""))

    def test_text_to_html_simple_string(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("foo", page.text_to_html("foo"))

    def test_text_to_html_newline(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("<br>\n", page.text_to_html("\n"))

    def test_text_to_html_multiple_newlines(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<br>\n<br>\n<br>\n",
                page.text_to_html("\n\n\n"))

    def test_text_to_html_multiline(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "foo<br>\nbar<br>\nbaz<br>\nquux",
                page.text_to_html("foo\nbar\nbaz\nquux"))

    def test_get_node_by_path(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            child = uriel.VirtualNode(project_root, "child", root)

            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                root,
                page.get_node_by_path(
                    uriel.Token("{{node-url:index}}"),
                    "index"
                )
            )

            self.assertEqual(
                child,
                page.get_node_by_path(
                    uriel.Token("{{node-url:index}}"),
                    "child"
                )
            )

            self.assertRaises(
                uriel.UrielError,
                page.get_node_by_path,
                    uriel.Token("{{node-url:foo}}"),
                    "foo"
            )

    def test_create_breadcrumbs_default_separator_with_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)

            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            bar.add_child(foo)

            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            baz.add_child(bar)

            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            baz.add_child(quux)

            root_page = uriel.Page(project_root, root)
            foo_page = uriel.Page(project_root, foo)
            bar_page = uriel.Page(project_root, bar)
            baz_page = uriel.Page(project_root, baz)
            quux_page = uriel.Page(project_root, quux)

            self.assertEqual("", root_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>",
                foo_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> &raquo; " +
                "<a href=\"/foo/bar/\">Bar</a>",
                bar_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> &raquo; " +
                "<a href=\"/foo/bar/\">Bar</a> &raquo; " +
                "<a href=\"/foo/bar/baz/\">Baz</a>",
                baz_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> &raquo; " +
                "<a href=\"/foo/bar/\">Bar</a> &raquo; " +
                "<a href=\"/foo/bar/baz/\">Baz</a> &raquo; " +
                "<a href=\"/foo/bar/baz/quux/\">Quux</a>",
                quux_page.create_breadcrumbs())

    def test_create_breadcrumbs_default_separator_no_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("breadcrumb-separator-spaces", "false")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)

            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            bar.add_child(foo)

            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            baz.add_child(bar)

            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            baz.add_child(quux)

            root_page = uriel.Page(project_root, root)
            foo_page = uriel.Page(project_root, foo)
            bar_page = uriel.Page(project_root, bar)
            baz_page = uriel.Page(project_root, baz)
            quux_page = uriel.Page(project_root, quux)

            self.assertEqual("", root_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>",
                foo_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>&raquo;" +
                "<a href=\"/foo/bar/\">Bar</a>",
                bar_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>&raquo;" +
                "<a href=\"/foo/bar/\">Bar</a>&raquo;" +
                "<a href=\"/foo/bar/baz/\">Baz</a>",
                baz_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>&raquo;" +
                "<a href=\"/foo/bar/\">Bar</a>&raquo;" +
                "<a href=\"/foo/bar/baz/\">Baz</a>&raquo;" +
                "<a href=\"/foo/bar/baz/quux/\">Quux</a>",
                quux_page.create_breadcrumbs())

    def test_create_breadcrumbs_custom_separator_with_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("breadcrumb-separator", "/")
            root.set_header("breadcrumb-separator-spaces", "true")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)

            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            bar.add_child(foo)

            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            baz.add_child(bar)

            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            baz.add_child(quux)

            root_page = uriel.Page(project_root, root)
            foo_page = uriel.Page(project_root, foo)
            bar_page = uriel.Page(project_root, bar)
            baz_page = uriel.Page(project_root, baz)
            quux_page = uriel.Page(project_root, quux)

            self.assertEqual("", root_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>",
                foo_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> / " +
                "<a href=\"/foo/bar/\">Bar</a>",
                bar_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> / " +
                "<a href=\"/foo/bar/\">Bar</a> / " +
                "<a href=\"/foo/bar/baz/\">Baz</a>",
                baz_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> / " +
                "<a href=\"/foo/bar/\">Bar</a> / " +
                "<a href=\"/foo/bar/baz/\">Baz</a> / " +
                "<a href=\"/foo/bar/baz/quux/\">Quux</a>",
                quux_page.create_breadcrumbs())

    def test_create_breadcrumbs_custom_separator_no_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("breadcrumb-separator", "/")
            root.set_header("breadcrumb-separator-spaces", "false")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)

            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            bar.add_child(foo)

            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            baz.add_child(bar)

            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            baz.add_child(quux)

            root_page = uriel.Page(project_root, root)
            foo_page = uriel.Page(project_root, foo)
            bar_page = uriel.Page(project_root, bar)
            baz_page = uriel.Page(project_root, baz)
            quux_page = uriel.Page(project_root, quux)

            self.assertEqual("", root_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>",
                foo_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>/" +
                "<a href=\"/foo/bar/\">Bar</a>",
                bar_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>/" +
                "<a href=\"/foo/bar/\">Bar</a>/" +
                "<a href=\"/foo/bar/baz/\">Baz</a>",
                baz_page.create_breadcrumbs())

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>/" +
                "<a href=\"/foo/bar/\">Bar</a>/" +
                "<a href=\"/foo/bar/baz/\">Baz</a>/" +
                "<a href=\"/foo/bar/baz/quux/\">Quux</a>",
                quux_page.create_breadcrumbs())

    def test_get_soju_result(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # create a lib/soju.py file with a hello() function
            lib_root = os.path.join(project_root, "lib")
            soju_file = os.path.join(project_root, "lib", "soju.py")

            os.mkdir(lib_root)

            with open(soju_file, "w") as f:
                f.write("def hello():")
                f.write("    return \"hello from soju.py, 2 + 2 = \" + str(2 + 2)")
                f.close()

            # load the soju module, and add it to the uriel module namespace
            if "soju" in sys.modules:
                del(sys.modules["soju"])
            loader = importlib.machinery.SourceFileLoader("soju", soju_file)
            spec = importlib.util.spec_from_loader("soju", loader)
            uriel.soju = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(uriel.soju)

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            # execute the soju hello() function, and verify the result
            self.assertEqual(
                "hello from soju.py, 2 + 2 = 4",
                page.get_soju_result("hello()"))

    def test_get_node_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("/", page.get_node_url(root))

    def test_get_node_url_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            page = uriel.Page(project_root, root, use_canonical_url=True)

            self.assertEqual("https://example.com/", page.get_node_url(root))

    def test_get_node_link(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("<a href=\"/\">Index</a>", page.get_node_link(root))

    def test_get_node_link_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            page = uriel.Page(project_root, root, use_canonical_url=True)

            self.assertEqual(
                "<a href=\"https://example.com/\">Index</a>",
                page.get_node_link(root))

    def test_get_static_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("image.jpg", page.get_static_url(root, "image.jpg"))
            self.assertEqual("/image.jpg", page.get_static_url(root, "/image.jpg"))

    def test_get_static_url_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            page = uriel.Page(project_root, root, use_canonical_url=True)

            self.assertEqual(
                "https://example.com/image.jpg",
                page.get_static_url(root, "image.jpg"))

            self.assertEqual(
                "https://example.com/image.jpg",
                page.get_static_url(root, "/image.jpg"))

    def test_get_maybe_canonical_html_fragment_non_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("__node-list-html", "value of node list HTML")
            root.set_header("__node-list-html-canonical", "value of node list HTML canonical")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "value of node list HTML",
                page.get_maybe_canonical_html_fragment(
                    root, "__node-list-html"))

    def test_get_maybe_canonical_html_fragment_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("__node-list-html", "value of node list HTML")
            root.set_header("__node-list-html-canonical", "value of node list HTML canonical")
            page = uriel.Page(project_root, root, use_canonical_url=True)

            self.assertEqual(
                "value of node list HTML canonical",
                page.get_maybe_canonical_html_fragment(
                    root, "__node-list-html"))

    def test_merge_token_literal_empty_string(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("", page.merge_token_literal(uriel.Token("")))

    def test_merge_token_literal_basic(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("foo", page.merge_token_literal(uriel.Token("foo")))

    def test_merge_token_literal_unidentified_parameter(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(uriel.UrielError,
                              page.merge_token_literal, uriel.Token("{{blah:blah}}"))

    def test_merge_token_value_not_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(uriel.UrielError,
                              page.merge_token_value,
                              uriel.Token("{{value:foo}}"))

    def test_merge_token_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "Foo & Bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "Foo &amp; Bar",
                page.merge_token_value(
                    uriel.Token("{{value:foo}}")
                )
            )

    def test_merge_token_value_unescaped_not_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(uriel.UrielError,
                              page.merge_token_value_unescaped,
                              uriel.Token("{{value-unescaped:foo}}"))

    def test_merge_token_value_unescaped(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "Foo & Bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "Foo & Bar",
                page.merge_token_value_unescaped(
                    uriel.Token("{{value-unescaped:foo}}")
                )
            )

    def test_merge_token_include_missing_template(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            templates_root = os.path.join(project_root, "templates")
            template_a = os.path.join(project_root, "templates/a.html")

            os.mkdir(templates_root)

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_include,
                uriel.Token("{{include:a.html}}"))

    def test_merge_token_include(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            templates_root = os.path.join(project_root, "templates")
            template_a = os.path.join(project_root, "templates/a.html")
            template_b = os.path.join(project_root, "templates/b.html")

            os.mkdir(templates_root)

            with open(template_a, "w") as f:
                f.write("a {{include:b.html}}")
                f.close()

            with open(template_b, "w") as f:
                f.write("b {{value:foo}}")
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "a b bar",
                page.merge_token_include(
                    uriel.Token("{{include:a.html}}")
                )
            )

    def test_merge_token_created(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.created = get_datetime_from_date_str("2025-08-24T17:08:37-04:00")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "&lt;August 24, 2025&gt;",
                page.merge_token_created(
                    uriel.Token("{{created:<%B %d, %Y>}}")
                )
            )

    def test_merge_token_modified(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.modified = get_datetime_from_date_str("2025-08-24T17:08:37-04:00")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "&lt;August 24, 2025&gt;",
                page.merge_token_modified(
                    uriel.Token("{{modified:<%B %d, %Y>}}")
                )
            )

    def test_merge_token_breadcrumbs_invalid(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(uriel.UrielError,
                              page.merge_token_breadcrumbs,
                              uriel.Token("{{breadcrumbs:fail}}"))

    def test_merge_token_breadcrumbs(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)

            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            bar.add_child(foo)

            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            baz.add_child(bar)

            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            baz.add_child(quux)

            quux_page = uriel.Page(project_root, quux)

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> &raquo; " +
                "<a href=\"/foo/bar/\">Bar</a> &raquo; " +
                "<a href=\"/foo/bar/baz/\">Baz</a> &raquo; " +
                "<a href=\"/foo/bar/baz/quux/\">Quux</a>",
                quux_page.merge_token_breadcrumbs(
                    uriel.Token("{{breadcrumbs:*}}")
                )
            )

    def test_get_static_url_abspath(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")

            foo_path = os.path.abspath(os.path.join(public_dir, "foo"))
            bar_path = os.path.abspath(os.path.join(public_dir, "foo/bar.jpg"))

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                foo_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url:foo}}"),
                    "foo"
                )
            )

            self.assertEqual(
                foo_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url:/foo}}"),
                    "/foo"
                )
            )

            self.assertEqual(
                foo_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url:foo/}}"),
                    "foo/"
                )
            )

            self.assertEqual(
                foo_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url:/foo/}}"),
                    "/foo/"
                )
            )

            self.assertEqual(
                foo_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url://foo//}}"),
                    "//foo//"
                )
            )

            self.assertEqual(
                bar_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url:foo/bar.jpg}}"),
                    "foo/bar.jpg"
                )
            )

            self.assertEqual(
                bar_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url:/foo/bar.jpg}}"),
                    "/foo/bar.jpg"
                )
            )

            self.assertEqual(
                bar_path,
                page.get_static_url_abspath(
                    uriel.Token("{{static-url://foo//bar.jpg}}"),
                    "//foo//bar.jpg"
                )
            )

    def test_get_static_url_abspath_directory_traversal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.get_static_url_abspath,
                uriel.Token("{{static-url:../images}}"),
                "../")

            self.assertRaises(
                uriel.UrielError,
                page.get_static_url_abspath,
                uriel.Token("{{static-url:../images}}"),
                "../images")

            self.assertRaises(
                uriel.UrielError,
                page.get_static_url_abspath,
                uriel.Token("{{static-url:../../../some/file/outside/the/project.jpg}}"),
                "../../../some/file/outside/the/project.jpg")

    def test_merge_token_static_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            images_dir = os.path.abspath(os.path.join(public_dir, "images"))
            image_file = os.path.abspath(os.path.join(public_dir, "images/hello.jpg"))

            os.mkdir(public_dir)
            os.mkdir(images_dir)

            with open(image_file, "w") as f:
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            child = uriel.VirtualNode(project_root, "child/index", root)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "/images/hello.jpg",
                page.merge_token_static_url(
                    uriel.Token("{{static-url:/images/hello.jpg}}")
                )
            )

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_static_url,
                uriel.Token("{{static-url:/file/not/found.jpg}}")
            )

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_static_url,
                uriel.Token("{{static-url:../public/images/hello.jpg}}")
            )

    def test_merge_token_static_hash_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            css_dir = os.path.abspath(os.path.join(public_dir, "css"))
            css_file = os.path.abspath(os.path.join(public_dir, "css/main.css"))
            hashed_css_file = os.path.abspath(
                os.path.join(public_dir,
                             "css/d41d8cd98f00b204e9800998ecf8427e.css"))

            os.mkdir(public_dir)
            os.mkdir(css_dir)

            with open(css_file, "w") as f:
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            child = uriel.VirtualNode(project_root, "child/index", root)

            page = uriel.Page(project_root, root)

            # hashed file name is based on md5 hash of file contents,
            # and is created the first time this token is merged
            self.assertEqual(
                "/css/d41d8cd98f00b204e9800998ecf8427e.css",
                page.merge_token_static_hash_url(
                    uriel.Token("{{static-hash-url:/css/main.css}}")
                )
            )
            self.assertTrue(os.path.isfile(hashed_css_file))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_static_hash_url,
                uriel.Token("{{static-hash-url:/file/not/found.css}}")
            )

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_static_hash_url,
                uriel.Token("{{static-hash-url:../public/css/main.css}}")
            )

    def test_merge_token_rss_invalid_rvalue(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_rss,
                uriel.Token("{{rss:*}}"))

    def test_merge_token_rss_no_headers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_rss,
                uriel.Token("{{rss:url}}"))

    def test_merge_token_rss_no_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("rss-url", "/rss.xml")

            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_rss,
                uriel.Token("{{rss:url}}"))

    def test_merge_token_rss_no_rss_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")

            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_rss,
                uriel.Token("{{rss:url}}"))

    def test_merge_token_rss(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("rss-url", "/rss.xml")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "https://example.com/rss.xml",
                page.merge_token_rss(uriel.Token("{{rss:url}}")))

    def test_merge_token_node_body_empty(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_body("")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "",
                page.merge_token_node_body(uriel.Token("{{node:body}}")))

    def test_merge_token_node_body_html(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_body("<html>\n<body>\n{{value:foo}}\n</body>\n</html>")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<html>\n<body>\nbar\n</body>\n</html>",
                page.merge_token_node_body(uriel.Token("{{node:body}}")))

    def test_merge_token_node_body_text(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("format", "text")
            root.set_header("foo", "bar")
            root.set_body("line 1\nline 2\n{{value:foo}}\nline 4")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "line 1<br>\nline 2<br>\nbar<br>\nline 4",
                page.merge_token_node_body(uriel.Token("{{node:body}}")))

    def test_merge_token_node_body_semaphore_eq_1(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_body("<html>\n<body>\n{{value:foo}}\n</body>\n</html>")

            page = uriel.Page(project_root, root)
            page.node_body_semaphore = 1

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node_body,
                uriel.Token("{{node:body}}"))

            self.assertEqual(3, len(c.stderr))
            self.assertEqual("node body include loop error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{node:body}}'", c.stderr[2])

    def test_merge_token_node_colon_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)

            page = uriel.Page(project_root, foo)

            self.assertEqual(
                "/foo/",
                page.merge_token_node(uriel.Token("{{node:url}}")))

    def test_merge_token_node_colon_name(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)

            page = uriel.Page(project_root, foo)

            self.assertEqual(
                "foo",
                page.merge_token_node(uriel.Token("{{node:name}}")))

    def test_merge_token_node_colon_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)

            page = uriel.Page(project_root, foo)

            self.assertEqual(
                "Foo",
                page.merge_token_node(uriel.Token("{{node:title}}")))

    def test_merge_token_node_colon_link(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)

            page = uriel.Page(project_root, foo)

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a>",
                page.merge_token_node(uriel.Token("{{node:link}}")))

    def test_merge_token_node_invalid_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)

            page = uriel.Page(project_root, foo)

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node,
                uriel.Token("{{node:blah}}"))

    def test_merge_token_node_dash_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "/",
                page.merge_token_node_url(uriel.Token("{{node-url:index}}")))

            self.assertEqual(
                "/child/",
                page.merge_token_node_url(uriel.Token("{{node-url:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node_url,
                uriel.Token("{{node-url:does-not-exist}}"))

    def test_merge_token_node_dash_url_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root, use_canonical_url=True)

            self.assertEqual(
                "https://example.com/",
                page.merge_token_node_url(uriel.Token("{{node-url:index}}")))

            self.assertEqual(
                "https://example.com/child/",
                page.merge_token_node_url(uriel.Token("{{node-url:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node_url,
                uriel.Token("{{node-url:does-not-exist}}"))

    def test_merge_token_node_dash_name(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "index",
                page.merge_token_node_name(uriel.Token("{{node-name:index}}")))

            self.assertEqual(
                "child",
                page.merge_token_node_name(uriel.Token("{{node-name:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node_name,
                uriel.Token("{{node-name:does-not-exist}}"))

    def test_merge_token_node_dash_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("title", "Root Node")

            child = uriel.VirtualNode(project_root, "child/index", root)
            child.set_header("title", "Child Node")
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "Root Node",
                page.merge_token_node_title(uriel.Token("{{node-title:index}}")))

            self.assertEqual(
                "Child Node",
                page.merge_token_node_title(uriel.Token("{{node-title:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node_title,
                uriel.Token("{{node-title:does-not-exist}}"))

    def test_merge_token_node_dash_link(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<a href=\"/\">Index</a>",
                page.merge_token_node_link(uriel.Token("{{node-link:index}}")))

            self.assertEqual(
                "<a href=\"/child/\">Child</a>",
                page.merge_token_node_link(uriel.Token("{{node-link:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node_link,
                uriel.Token("{{node-link:does-not-exist}}"))

    def test_merge_token_node_dash_link_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")

            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root, use_canonical_url=True)

            self.assertEqual(
                "<a href=\"https://example.com/\">Index</a>",
                page.merge_token_node_link(uriel.Token("{{node-link:index}}")))

            self.assertEqual(
                "<a href=\"https://example.com/child/\">Child</a>",
                page.merge_token_node_link(uriel.Token("{{node-link:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_node_link,
                uriel.Token("{{node-link:does-not-exist}}"))

    def test_merge_token_node_dash_list_no_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                KeyError,
                page.merge_token_node_list,
                uriel.Token("{{node-list:*}}"))

    def test_merge_token_node_dash_list_not_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("__node-list-html", "foo")
            page = uriel.Page(project_root, root, use_canonical_url=False)

            self.assertEqual(
                "foo",
                page.merge_token_node_list(uriel.Token("{{node-list:*}}")))

    def test_merge_token_node_dash_list_canonical(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("__node-list-html-canonical", "foo")
            page = uriel.Page(project_root, root, use_canonical_url=True)

            self.assertEqual(
                "foo",
                page.merge_token_node_list(uriel.Token("{{node-list:*}}")))

    def test_merge_token_tag_dash_list_no_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.merge_token_tag_list,
                uriel.Token("{{tag-list:*}}"))

    def test_merge_token_tag_dash_list(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("__tag-list-html", "foo")
            page = uriel.Page(project_root, root, use_canonical_url=False)

            self.assertEqual(
                "foo",
                page.merge_token_tag_list(uriel.Token("{{tag-list:*}}")))

    def test_merge_token_soju(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # create a lib/soju.py file with a hello() function
            lib_root = os.path.join(project_root, "lib")
            soju_file = os.path.join(project_root, "lib", "soju.py")

            os.mkdir(lib_root)

            with open(soju_file, "w") as f:
                f.write("def hello():\n")
                f.write("    return \"hello from soju.py, 2 + 2 = \" + str(2 + 2)\n")
                f.close()

            # load the soju module, and add it to the uriel module namespace
            if "soju" in sys.modules:
                del(sys.modules["soju"])
            loader = importlib.machinery.SourceFileLoader("soju", soju_file)
            spec = importlib.util.spec_from_loader("soju", loader)
            uriel.soju = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(uriel.soju)

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "hello from soju.py, 2 + 2 = 4",
                page.merge_token_soju(uriel.Token("{{soju:hello()}}")))

    def test_merge_token_soju_raise_soju_error_with_reason(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # create a lib/soju.py file with a hello() function
            lib_root = os.path.join(project_root, "lib")
            soju_file = os.path.join(project_root, "lib", "soju.py")

            os.mkdir(lib_root)

            with open(soju_file, "w") as f:
                f.write("def raise_soju_error_with_reason():\n")
                f.write("    raise SojuError(\"oops\")\n")
                f.close()

            # load the soju module, and add it to the uriel module namespace
            if "soju" in sys.modules:
                del(sys.modules["soju"])
            loader = importlib.machinery.SourceFileLoader("soju", soju_file)
            spec = importlib.util.spec_from_loader("soju", loader)
            uriel.soju = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(uriel.soju)

            uriel.soju.SojuError = uriel.SojuError

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            errstr = None
            try:
                page.merge_token_soju(
                    uriel.Token("{{soju:raise_soju_error_with_reason()}}"))
            except uriel.SojuError as e:
                errstr = str(e)

            self.assertEqual(4, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{soju:raise_soju_error_with_reason()}}'", c.stderr[2])
            self.assertEqual("      'oops'", c.stderr[3])

            self.assertEqual(
                "error in function call to 'soju.raise_soju_error_with_reason()': 'oops'",
                errstr)

    def test_merge_token_soju_raise_soju_error_without_reason(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # create a lib/soju.py file with a hello() function
            lib_root = os.path.join(project_root, "lib")
            soju_file = os.path.join(project_root, "lib", "soju.py")

            os.mkdir(lib_root)

            with open(soju_file, "w") as f:
                f.write("def raise_soju_error_without_reason():\n")
                f.write("    raise SojuError()\n")
                f.close()

            # load the soju module, and add it to the uriel module namespace
            if "soju" in sys.modules:
                del(sys.modules["soju"])
            loader = importlib.machinery.SourceFileLoader("soju", soju_file)
            spec = importlib.util.spec_from_loader("soju", loader)
            uriel.soju = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(uriel.soju)

            uriel.soju.SojuError = uriel.SojuError

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            errstr = None
            try:
                page.merge_token_soju(
                    uriel.Token("{{soju:raise_soju_error_without_reason()}}"))
            except uriel.SojuError as e:
                errstr = str(e)

            self.assertEqual(4, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{soju:raise_soju_error_without_reason()}}'", c.stderr[2])
            self.assertEqual("      SojuError", c.stderr[3])

            self.assertEqual(
                "error in function call to 'soju.raise_soju_error_without_reason()': SojuError",
                errstr)

    def test_merge_token_soju_raise_exception_with_reason(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # create a lib/soju.py file with a hello() function
            lib_root = os.path.join(project_root, "lib")
            soju_file = os.path.join(project_root, "lib", "soju.py")

            os.mkdir(lib_root)

            with open(soju_file, "w") as f:
                f.write("def raise_exception_with_reason():\n")
                f.write("    raise Exception(\"oops\")\n")
                f.close()

            # load the soju module, and add it to the uriel module namespace
            if "soju" in sys.modules:
                del(sys.modules["soju"])
            loader = importlib.machinery.SourceFileLoader("soju", soju_file)
            spec = importlib.util.spec_from_loader("soju", loader)
            uriel.soju = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(uriel.soju)

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            errstr = None
            try:
                page.merge_token_soju(
                    uriel.Token("{{soju:raise_exception_with_reason()}}"))
            except Exception as e:
                errstr = str(e)

            self.assertEqual(6, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{soju:raise_exception_with_reason()}}'", c.stderr[2])
            self.assertEqual("      'oops'", c.stderr[3])
            self.assertEqual("Traceback (most recent call last):", c.stderr[4])
            self.assertEqual(
                "  File \"" + soju_file + "\", line 2, in raise_exception_with_reason\n" + \
                "    raise Exception(\"oops\")",
                c.stderr[5])

            self.assertEqual(
                "error in function call to 'soju.raise_exception_with_reason()': 'oops'",
                errstr)

    def test_merge_token_soju_raise_exception_without_reason(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # create a lib/soju.py file with a hello() function
            lib_root = os.path.join(project_root, "lib")
            soju_file = os.path.join(project_root, "lib", "soju.py")

            os.mkdir(lib_root)

            with open(soju_file, "w") as f:
                f.write("def raise_exception_without_reason():\n")
                f.write("    raise Exception()\n")
                f.close()

            # load the soju module, and add it to the uriel module namespace
            if "soju" in sys.modules:
                del(sys.modules["soju"])
            loader = importlib.machinery.SourceFileLoader("soju", soju_file)
            spec = importlib.util.spec_from_loader("soju", loader)
            uriel.soju = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(uriel.soju)

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            errstr = None
            try:
                page.merge_token_soju(
                    uriel.Token("{{soju:raise_exception_without_reason()}}"))
            except Exception as e:
                errstr = str(e)

            self.assertEqual(6, len(c.stderr))
            self.assertEqual("parameter error:", c.stderr[0])
            self.assertEqual("  nodes/index", c.stderr[1])
            self.assertEqual("    '{{soju:raise_exception_without_reason()}}'", c.stderr[2])
            self.assertEqual("      Exception", c.stderr[3])
            self.assertEqual("Traceback (most recent call last):", c.stderr[4])
            self.assertEqual(
                "  File \"" + soju_file + "\", line 2, in raise_exception_without_reason\n" + \
                "    raise Exception()",
                c.stderr[5])

            self.assertEqual(
                "error in function call to 'soju.raise_exception_without_reason()': Exception",
                errstr)

    def test_merge_token_with_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("foo", page.merge_token(uriel.Token("foo")))

    def test_merge_token_with_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "Foo & Bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "Foo &amp; Bar",
                page.merge_token(
                    uriel.Token("{{value:foo}}")
                )
            )

    def test_merge_token_with_value_unescaped(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "Foo & Bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "Foo & Bar",
                page.merge_token(
                    uriel.Token("{{value-unescaped:foo}}")
                )
            )

    def test_merge_token_with_include(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            templates_root = os.path.join(project_root, "templates")
            template_a = os.path.join(project_root, "templates/a.html")
            template_b = os.path.join(project_root, "templates/b.html")

            os.mkdir(templates_root)

            with open(template_a, "w") as f:
                f.write("a {{include:b.html}}")
                f.close()

            with open(template_b, "w") as f:
                f.write("b {{value:foo}}")
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "a b bar",
                page.merge_token(
                    uriel.Token("{{include:a.html}}")
                )
            )

    def test_merge_token_with_created(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.created = get_datetime_from_date_str("2025-08-24T17:08:37-04:00")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "&lt;August 24, 2025&gt;",
                page.merge_token(
                    uriel.Token("{{created:<%B %d, %Y>}}")
                )
            )

    def test_merge_token_with_modified(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.modified = get_datetime_from_date_str("2025-08-24T17:08:37-04:00")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "&lt;August 24, 2025&gt;",
                page.merge_token(
                    uriel.Token("{{modified:<%B %d, %Y>}}")
                )
            )

    def test_merge_token_with_breadcrumbs(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            foo = uriel.VirtualNode(project_root, "foo/index", root)
            root.add_child(foo)

            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            bar.add_child(foo)

            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            baz.add_child(bar)

            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)
            baz.add_child(quux)

            quux_page = uriel.Page(project_root, quux)

            self.assertEqual(
                "<a href=\"/foo/\">Foo</a> &raquo; " +
                "<a href=\"/foo/bar/\">Bar</a> &raquo; " +
                "<a href=\"/foo/bar/baz/\">Baz</a> &raquo; " +
                "<a href=\"/foo/bar/baz/quux/\">Quux</a>",
                quux_page.merge_token(
                    uriel.Token("{{breadcrumbs:*}}")
                )
            )

    def test_merge_token_with_static_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            images_dir = os.path.abspath(os.path.join(public_dir, "images"))
            image_file = os.path.abspath(os.path.join(public_dir, "images/hello.jpg"))

            os.mkdir(public_dir)
            os.mkdir(images_dir)

            with open(image_file, "w") as f:
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            child = uriel.VirtualNode(project_root, "child/index", root)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "/images/hello.jpg",
                page.merge_token(
                    uriel.Token("{{static-url:/images/hello.jpg}}")
                )
            )

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{static-url:/file/not/found.jpg}}")
            )

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{static-url:../public/images/hello.jpg}}")
            )

    def test_merge_token_with_static_hash_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            public_dir = os.path.join(project_root, "public")
            css_dir = os.path.abspath(os.path.join(public_dir, "css"))
            css_file = os.path.abspath(os.path.join(public_dir, "css/main.css"))
            hashed_css_file = os.path.abspath(
                os.path.join(public_dir,
                             "css/d41d8cd98f00b204e9800998ecf8427e.css"))

            os.mkdir(public_dir)
            os.mkdir(css_dir)

            with open(css_file, "w") as f:
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            child = uriel.VirtualNode(project_root, "child/index", root)

            page = uriel.Page(project_root, root)

            # hashed file name is based on md5 hash of file contents,
            # and is created the first time this token is merged
            self.assertEqual(
                "/css/d41d8cd98f00b204e9800998ecf8427e.css",
                page.merge_token(
                    uriel.Token("{{static-hash-url:/css/main.css}}")
                )
            )
            self.assertTrue(os.path.isfile(hashed_css_file))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{static-hash-url:/file/not/found.css}}")
            )

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{static-hash-url:../public/css/main.css}}")
            )

    def test_merge_token_with_rss(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("rss-url", "/rss.xml")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "https://example.com/rss.xml",
                page.merge_token(uriel.Token("{{rss:url}}")))

    def test_merge_token_with_node(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_body("<html>\n<body>\n{{value:foo}}\n</body>\n</html>")

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<html>\n<body>\nbar\n</body>\n</html>",
                page.merge_token(uriel.Token("{{node:body}}")))

    def test_merge_token_with_node_dash_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "/",
                page.merge_token(uriel.Token("{{node-url:index}}")))

            self.assertEqual(
                "/child/",
                page.merge_token(uriel.Token("{{node-url:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{node-url:does-not-exist}}"))

    def test_merge_token_with_node_dash_name(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "index",
                page.merge_token(uriel.Token("{{node-name:index}}")))

            self.assertEqual(
                "child",
                page.merge_token(uriel.Token("{{node-name:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{node-name:does-not-exist}}"))

    def test_merge_token_with_node_dash_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("title", "Root Node")

            child = uriel.VirtualNode(project_root, "child/index", root)
            child.set_header("title", "Child Node")
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "Root Node",
                page.merge_token(uriel.Token("{{node-title:index}}")))

            self.assertEqual(
                "Child Node",
                page.merge_token(uriel.Token("{{node-title:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{node-title:does-not-exist}}"))

    def test_merge_token_with_node_dash_link(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            child = uriel.VirtualNode(project_root, "child/index", root)
            root.add_child(child)

            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<a href=\"/\">Index</a>",
                page.merge_token(uriel.Token("{{node-link:index}}")))

            self.assertEqual(
                "<a href=\"/child/\">Child</a>",
                page.merge_token(uriel.Token("{{node-link:child/index}}")))

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                uriel.Token("{{node-link:does-not-exist}}"))

    def test_merge_token_with_node_dash_list(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("__node-list-html", "foo")
            page = uriel.Page(project_root, root, use_canonical_url=False)

            self.assertEqual(
                "foo",
                page.merge_token(uriel.Token("{{node-list:*}}")))

    def test_merge_token_with_tag_dash_list(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("__tag-list-html", "foo")
            page = uriel.Page(project_root, root, use_canonical_url=False)

            self.assertEqual(
                "foo",
                page.merge_token(uriel.Token("{{tag-list:*}}")))

    def test_merge_token_with_soju(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # create a lib/soju.py file with a hello() function
            lib_root = os.path.join(project_root, "lib")
            soju_file = os.path.join(project_root, "lib", "soju.py")

            os.mkdir(lib_root)

            with open(soju_file, "w") as f:
                f.write("def hello():\n")
                f.write("    return \"hello from soju.py, 2 + 2 = \" + str(2 + 2)\n")
                f.close()

            # load the soju module, and add it to the uriel module namespace
            if "soju" in sys.modules:
                del(sys.modules["soju"])
            loader = importlib.machinery.SourceFileLoader("soju", soju_file)
            spec = importlib.util.spec_from_loader("soju", loader)
            uriel.soju = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(uriel.soju)

            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "hello from soju.py, 2 + 2 = 4",
                page.merge_token(uriel.Token("{{soju:hello()}}")))

    def test_merge_token_with_unknown_type(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("__tag-list-html", "foo")
            page = uriel.Page(project_root, root, use_canonical_url=False)

            invalid_token = uriel.Token("foo")
            invalid_token.type = "INVALID TYPE"

            self.assertRaises(
                uriel.UrielError,
                page.merge_token,
                invalid_token)

    def test_merge_line_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertIsNone(page.merge_line(None))

    def test_merge_line_blank(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("", page.merge_line(""))

    def test_merge_line_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("foo bar", page.merge_line("foo bar"))

    def test_merge_line_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<p>bar</p>",
                page.merge_line("<p>{{value:foo}}</p>"))

    def test_merge_lines_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                Exception,
                page.merge_lines,
                None)

    def test_merge_lines_no_lines(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("", page.merge_lines([]))

    def test_merge_lines_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "foo\nbar",
                page.merge_lines(["foo", "bar"]))

    def test_merge_lines_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<p>\nbar\n</p>",
                page.merge_lines(["<p>", "{{value:foo}}", "</p>"]))

    def test_merge_multiline_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                Exception,
                page.merge_multiline,
                None)

    def test_merge_multiline_blank(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual("", page.merge_multiline(""))

    def test_merge_multiline_literal(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "foo\nbar",
                page.merge_multiline("foo\nbar"))

    def test_merge_multiline_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<p>\nbar\n</p>",
                page.merge_multiline("<p>\n{{value:foo}}\n</p>"))

    def test_merge_template_null(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_body("<h1>\n{{value:foo}}\n</h1>\n")

            page = uriel.Page(project_root, root)
            page.template = "null"

            self.assertEqual(
                "<h1>\nbar\n</h1>\n",
                page.merge_template("null"))

    def test_merge_template(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            templates_dir = os.path.join(project_root, "templates")
            template_file = os.path.join(templates_dir, "default.html")

            os.mkdir(templates_dir)

            with open(template_file, "w") as f:
                f.write("<p>\n")
                f.write("{{value:foo}}\n")
                f.write("</p>\n")
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            page = uriel.Page(project_root, root)

            self.assertEqual(
                "<p>\nbar\n</p>",
                page.merge_template("default.html"))

    def test_merge_template_file_not_found(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            templates_dir = os.path.join(project_root, "templates")

            os.mkdir(templates_dir)

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            page = uriel.Page(project_root, root)

            self.assertRaises(
                uriel.UrielError,
                page.merge_template,
                "not-found.html")

    def test_render(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            templates_dir = os.path.join(project_root, "templates")
            template_file = os.path.join(templates_dir, "default.html")

            os.mkdir(templates_dir)

            with open(template_file, "w") as f:
                f.write("<p>\n")
                f.write("{{value:foo}}\n")
                f.write("</p>")
                f.close()

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")

            page = uriel.Page(project_root, root)
            page.template = "default.html"

            self.assertEqual("<p>\nbar\n</p>\n", page.render())

