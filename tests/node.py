import os
import datetime
import unittest

from .util import UrielContainer
from .util import TempDir
from .util import TimeZone
from .util import get_datetime_from_date_str

class TestNode(unittest.TestCase):
    """
    Tests the Node class.

    Node is the class under test here.
    But since it is an abstract class, most of its features are tested
    using VirtualNode, which is a subclass that inherits all of the
    Node methods and calls the Node superconstructor, but is designed to
    actually be instantiated and used directly.

    """

    def test_get_node_type_not_implemented(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # we actually do instantiate Node here, since we're verifying that
            # the get_node_type() base method throws an Exception
            node = uriel.Node(project_root, "index")

            self.assertRaises(Exception, node.get_node_type)

    def test_basic_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual(0, len(root.headers))
            self.assertEqual(root, root.get_root_node())
            self.assertEqual("Index", root.get_title())
            self.assertEqual("index", root.get_name())
            self.assertEqual("index", root.get_path())
            self.assertEqual("/", root.get_url())

    def test_constructor_duplicate_path(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo", root)
            root.add_child(foo)

            try:
                uriel.VirtualNode(project_root, "foo", root)
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "can not create node, another node already exists " + \
                    "with this path: 'foo'",
                    str(e))

    def test_constructor_duplicate_path_in_subdirectory(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            root.add_child(articles)
            dog = uriel.VirtualNode(project_root, "articles/dog", articles)
            articles.add_child(dog)

            self.assertRaises(uriel.UrielError,
                              uriel.VirtualNode,
                              project_root, "articles/dog", root)

    def test_constructor_plus_header_no_inheritance(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("+foo", "bar")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertTrue(child.has_header("foo"))
            self.assertFalse(child.has_header("+foo"))
            self.assertEqual("bar", child.get_header("foo"))

    def test_constructor_plus_header_override_inheritance(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("+foo", "quux")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertTrue(child.has_header("foo"))
            self.assertFalse(child.has_header("+foo"))
            self.assertEqual("quux", child.get_header("foo"))

    def test_constructor_plus_plus_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("++foo", "bar")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertFalse(articles.has_header("++foo"))
            self.assertTrue(articles.has_header("+foo"))
            self.assertFalse(articles.has_header("foo"))

            self.assertFalse(article_dog.has_header("++foo"))
            self.assertFalse(article_dog.has_header("+foo"))
            self.assertTrue(article_dog.has_header("foo"))

            self.assertEqual("bar", article_dog.get_header("foo"))

    def test_constructor_minus_header_invalid_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")

            root.set_header("-foo", "blah")

            self.assertRaises(uriel.UrielError,
                              uriel.VirtualNode,
                              project_root, "child", root)

    def test_constructor_minus_header_invalid_value_message(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("-foo", "bogus")

            try:
                uriel.VirtualNode(project_root, "child", root)
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "invalid header in node 'child': " + \
                    "'-foo': 'bogus' (value must be '*')",
                    str(e))

    def test_constructor_minus_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("-foo", "*")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertFalse(child.has_header("foo"))
            self.assertFalse(child.has_header("-foo"))

    def test_constructor_minus_minus_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # a --header doesn't work the same way as a ++header
            # basically, a --foo header will just remove any -foo header,
            # and it doesn't cascade down beyond that
            # this test is here to highlight and document the difference,
            # but a --header isn't really very useful in practice

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("--foo", "*")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertFalse(articles.has_header("--foo"))
            self.assertFalse(articles.has_header("-foo"))
            self.assertTrue(articles.has_header("foo"))
            self.assertEqual("bar", articles.get_header("foo"))

            self.assertFalse(article_dog.has_header("--foo"))
            self.assertFalse(article_dog.has_header("-foo"))
            self.assertTrue(article_dog.has_header("foo"))
            self.assertEqual("bar", article_dog.get_header("foo"))

    def test_constructor_plus_minus_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # a +- header works the same was as a regular - header
            # included in the tests for completeness, and to document
            # the behavior

            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("+-foo", "*")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertFalse(articles.has_header("foo"))
            self.assertFalse(article_dog.has_header("foo"))

    def test_constructor_plus_plus_minus_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("++-foo", "*")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertFalse(articles.has_header("++-foo"))
            self.assertTrue(articles.has_header("+-foo"))
            self.assertFalse(articles.has_header("-foo"))
            self.assertTrue(articles.has_header("foo"))
            self.assertEqual("bar", articles.get_header("foo"))

            self.assertFalse(article_dog.has_header("++-foo"))
            self.assertFalse(article_dog.has_header("+-foo"))
            self.assertFalse(article_dog.has_header("-foo"))
            self.assertFalse(article_dog.has_header("foo"))

    def test_constructor_minus_plus_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("+foo", "quux")
            root.set_header("-+foo", "*")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertTrue(root.has_header("-+foo"))
            self.assertTrue(root.has_header("+foo"))
            self.assertTrue(root.has_header("foo"))
            self.assertEqual("bar", root.get_header("foo"))

            self.assertFalse(articles.has_header("-+foo"))
            self.assertFalse(articles.has_header("+foo"))
            self.assertTrue(articles.has_header("foo"))
            self.assertEqual("quux", articles.get_header("foo"))

            self.assertFalse(article_dog.has_header("-+foo"))
            self.assertFalse(article_dog.has_header("+foo"))
            self.assertTrue(article_dog.has_header("foo"))
            self.assertEqual("quux", articles.get_header("foo"))

    def test_constructor_header_inheritance(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertTrue(child.has_header("foo"))
            self.assertEqual("bar", child.get_header("foo"))

    def test_constructor_header_inheritance_removes_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("title", "Root Node")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertFalse(child.has_header("title"))
            self.assertEqual("Child", child.get_title())

    def test_constructor_header_inheritance_removes_created(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("created", "2025-08-24T17:08:37-04:00")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertFalse(child.has_header("created"))

    def test_constructor_header_inheritance_removes_modified(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("modified", "2025-08-24T17:08:37-04:00")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertFalse(child.has_header("modified"))

    def test_constructor_header_inheritance_removes_title_created_modified(
            self):

        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("title", "Root Node")
            root.set_header("created", "2025-08-24T17:08:37-04:00")
            root.set_header("modified", "2025-08-25T09:14:02-04:00")
            root.set_header("foo", "bar")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertFalse(child.has_header("title"))
            self.assertFalse(child.has_header("created"))
            self.assertFalse(child.has_header("modified"))

            self.assertTrue(child.has_header("foo"))
            self.assertEqual("bar", child.get_header("foo"))

    def test_constructor_header_inheritance_removes_created_and_modified(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("created", "2025-08-24T17:08:37-04:00")
            root.set_header("modified", "2025-08-25T09:14:02-04:00")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertFalse(child.has_header("created"))
            self.assertFalse(child.has_header("modified"))

    def test_constructor_plus_title_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("title", "Root Node")
            root.set_header("+title", "Pushed Title")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertEqual("Root Node", root.get_header("title"))

            self.assertFalse(child.has_header("+title"))
            self.assertTrue(child.has_header("title"))
            self.assertEqual("Pushed Title", child.get_header("title"))
            self.assertEqual("Pushed Title", child.get_title())

    def test_constructor_plus_created_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("created", "2025-08-24T17:08:37-04:00")
            root.set_header("+created", "2026-01-02T03:04:05-05:00")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertEqual("2025-08-24T17:08:37-04:00",
                             root.get_header("created"))

            self.assertFalse(child.has_header("+created"))
            self.assertTrue(child.has_header("created"))
            self.assertEqual("2026-01-02T03:04:05-05:00",
                             child.get_header("created"))

    def test_constructor_plus_modified_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("modified", "2025-08-24T17:08:37-04:00")
            root.set_header("+modified", "2026-01-02T03:04:05-05:00")
            child = uriel.VirtualNode(project_root, "child", root)

            self.assertEqual("2025-08-24T17:08:37-04:00",
                             root.get_header("modified"))

            self.assertFalse(child.has_header("+modified"))
            self.assertTrue(child.has_header("modified"))
            self.assertEqual("2026-01-02T03:04:05-05:00",
                             child.get_header("modified"))

    def test_constructor_plus_title_header_no_further_inheritance(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("+title", "Pushed Title")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root,
                                            "articles/dog",
                                            articles)

            self.assertEqual("Pushed Title", articles.get_header("title"))

            self.assertFalse(article_dog.has_header("title"))
            self.assertEqual("Dog", article_dog.get_title())

    def test_constructor_plus_plus_title_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("++title", "Pushed Title")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root,
                                            "articles/dog",
                                            articles)

            self.assertFalse(articles.has_header("++title"))
            self.assertTrue(articles.has_header("+title"))
            self.assertFalse(articles.has_header("title"))

            self.assertFalse(article_dog.has_header("+title"))
            self.assertTrue(article_dog.has_header("title"))
            self.assertEqual("Pushed Title", article_dog.get_header("title"))

    def test_get_parent_node(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertIsNone(root.get_parent_node())
            self.assertEqual(root, articles.get_parent_node())
            self.assertEqual(articles, article_dog.get_parent_node())

    def test_get_path(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("index", root.get_path())
            self.assertEqual("articles/index", articles.get_path())
            self.assertEqual("articles/dog", article_dog.get_path())

    def test_add_get_child_nodes(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            about = uriel.VirtualNode(project_root, "about", root)
            contact = uriel.VirtualNode(project_root, "contact", root)
            articles = uriel.VirtualNode(project_root, "articles/index", root)

            root.add_child(about)
            root.add_child(contact)
            root.add_child(articles)

            children = root.get_children()

            self.assertEqual(3, len(children))
            self.assertEqual("about", children[0].get_path())
            self.assertEqual("articles/index", children[1].get_path())
            self.assertEqual("contact", children[2].get_path())

            self.assertEqual(0, len(about.get_children()))
            self.assertEqual(0, len(articles.get_children()))
            self.assertEqual(0, len(contact.get_children()))

    def test_get_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)

            self.assertEqual("/", root.get_url())
            self.assertEqual("/foo/", foo.get_url())
            self.assertEqual("/foo/bar/", bar.get_url())
            self.assertEqual("/foo/bar/baz/", baz.get_url())
            self.assertEqual("/foo/bar/baz/quux/", quux.get_url())

    def test_get_url_flat_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("flat-url", "true")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)

            self.assertEqual("/", root.get_url())
            self.assertEqual("/foo/", foo.get_url())
            self.assertEqual("/bar/", bar.get_url())
            self.assertEqual("/baz/", baz.get_url())
            self.assertEqual("/quux/", quux.get_url())

    def test_get_url_flat_url_section(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # bar has a flat-url, but its child nodes don't

            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar/index", foo)
            bar.set_header("flat-url", "true")
            baz = uriel.VirtualNode(project_root, "foo/bar/baz/index", bar)
            baz.set_header("flat-url", "false")
            quux = uriel.VirtualNode(project_root, "foo/bar/baz/quux", baz)

            self.assertEqual("/", root.get_url())
            self.assertEqual("/foo/", foo.get_url())
            self.assertEqual("/bar/", bar.get_url())
            self.assertEqual("/bar/baz/", baz.get_url())
            self.assertEqual("/bar/baz/quux/", quux.get_url())

    def test_get_url_with_dash_index(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            foo = uriel.VirtualNode(project_root, "foo-index/index", root)
            bar = uriel.VirtualNode(project_root, "foo-index/bar-index/index", foo)
            baz = uriel.VirtualNode(project_root, "foo-index/bar-index/baz-index/index", bar)
            quux = uriel.VirtualNode(project_root, "foo-index/bar-index/baz-index/quux", baz)
            quux_index = uriel.VirtualNode(project_root, "foo-index/bar-index/baz-index/quux-index", baz)

            self.assertEqual("/", root.get_url())
            self.assertEqual("/foo-index/", foo.get_url())
            self.assertEqual("/foo-index/bar-index/", bar.get_url())
            self.assertEqual("/foo-index/bar-index/baz-index/", baz.get_url())
            self.assertEqual("/foo-index/bar-index/baz-index/quux/", quux.get_url())
            self.assertEqual("/foo-index/bar-index/baz-index/quux-index/", quux_index.get_url())

    def test_get_canonical_url_header_not_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertRaises(uriel.UrielError, root.get_canonical_url)

    def test_get_canonical_url_base(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")

            self.assertEqual("https://example.com",
                             root.get_canonical_url_base())

    def test_get_canonical_url_base_header_not_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertRaises(uriel.UrielError, root.get_canonical_url_base)

    def test_get_canonical_url_trailing_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com/")

            try:
                root.get_canonical_url()
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "invalid Canonical-URL header value in node " + \
                    "'index': 'https://example.com/' " + \
                    "(can not end with a '/')",
                    str(e))

    def test_get_canonical_url_deeper_path_is_allowed(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com/blog")

            self.assertEqual("https://example.com/blog/",
                             root.get_canonical_url())

    def test_get_canonical_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar", foo)

            self.assertEqual("https://example.com/", root.get_canonical_url())
            self.assertEqual("https://example.com/foo/", foo.get_canonical_url())
            self.assertEqual("https://example.com/foo/bar/", bar.get_canonical_url())

    def test_get_canonical_url_flat_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("flat-url", "true")
            foo = uriel.VirtualNode(project_root, "foo/index", root)
            bar = uriel.VirtualNode(project_root, "foo/bar", foo)

            self.assertEqual("https://example.com/", root.get_canonical_url())
            self.assertEqual("https://example.com/foo/", foo.get_canonical_url())
            self.assertEqual("https://example.com/bar/", bar.get_canonical_url())

    def test_get_name(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            # special case: root node is named index
            self.assertEqual("index", root.get_name())

            # common case for other index nodes:
            # name is the containing directory
            self.assertEqual("articles", articles.get_name())

            # common case for leaf nodes: name is the file name
            self.assertEqual("dog", article_dog.get_name())

    def test_get_display_name(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/the-best-dog", articles)

            # special case: root node is based on the node name, index
            self.assertEqual("Index", root.get_display_name())

            # common case for other index nodes:
            # name is based on the containing directory name
            self.assertEqual("Articles", articles.get_display_name())

            # common case for leaf nodes: name is based on the file name
            self.assertEqual("The Best Dog", article_dog.get_display_name())

    def test_get_title_no_headers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/the-best-dog", articles)

            self.assertEqual("Index", root.get_title())
            self.assertEqual("Articles", articles.get_title())
            self.assertEqual("The Best Dog", article_dog.get_title())

    def test_get_title_with_title_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "Home Page")
            articles.set_header("title", "A List of Articles")
            article_dog.set_header("title", "I Got to Pet the Perfect Dog")

            self.assertEqual("Home Page", root.get_title())
            self.assertEqual("A List of Articles", articles.get_title())
            self.assertEqual("I Got to Pet the Perfect Dog", article_dog.get_title())

    def test_get_escaped_title_no_title_headers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "false")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/the-best-dog", articles)

            self.assertEqual("Index", root.get_escaped_title())
            self.assertEqual("Articles", articles.get_escaped_title())
            self.assertEqual("The Best Dog", article_dog.get_escaped_title())

    def test_get_escaped_title_with_title_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "false")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)
            
            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("The 'Home' Page", root.get_escaped_title())
            self.assertEqual("Articles & Things", articles.get_escaped_title())
            self.assertEqual("I Got to Pet the <Perfect> Dog", article_dog.get_escaped_title())

    def test_get_escaped_title_with_escape_title_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/the-best-dog", articles)

            self.assertEqual("Index", root.get_escaped_title())
            self.assertEqual("Articles", articles.get_escaped_title())
            self.assertEqual("The Best Dog", article_dog.get_escaped_title())

    def test_get_escaped_title_with_both_headers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)
            
            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("The &apos;Home&apos; Page", root.get_escaped_title())
            self.assertEqual("Articles &amp; Things", articles.get_escaped_title())
            self.assertEqual("I Got to Pet the &lt;Perfect&gt; Dog", article_dog.get_escaped_title())

    def test_get_link_no_title_no_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"/\">Index</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles</a>", articles.get_link())
            self.assertEqual("<a href=\"/articles/dog/\">Dog</a>", article_dog.get_link())

    def test_get_link_no_title_no_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("escape-title", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"/\">Index</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles</a>", articles.get_link())
            self.assertEqual("<a href=\"/articles/dog/\">Dog</a>", article_dog.get_link())

    def test_get_link_no_title_with_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"/\">Index</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles</a>", articles.get_link())
            self.assertEqual("<a href=\"/dog/\">Dog</a>", article_dog.get_link())

    def test_get_link_no_title_with_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("escape-title", "true")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"/\">Index</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles</a>", articles.get_link())
            self.assertEqual("<a href=\"/dog/\">Dog</a>", article_dog.get_link())

    def test_get_link_with_title_no_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "false")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"/\">The 'Home' Page</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles & Things</a>", articles.get_link())
            self.assertEqual("<a href=\"/articles/dog/\">I Got to Pet the <Perfect> Dog</a>", article_dog.get_link())

    def test_get_link_with_title_no_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"/\">The &apos;Home&apos; Page</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles &amp; Things</a>", articles.get_link())
            self.assertEqual("<a href=\"/articles/dog/\">I Got to Pet the &lt;Perfect&gt; Dog</a>", article_dog.get_link())

    def test_get_link_with_title_with_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "false")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"/\">The 'Home' Page</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles & Things</a>", articles.get_link())
            self.assertEqual("<a href=\"/dog/\">I Got to Pet the <Perfect> Dog</a>", article_dog.get_link())

    def test_get_link_with_title_with_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            # "escape-title: true" is the default
            root.set_header("escape-title", "true")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"/\">The &apos;Home&apos; Page</a>", root.get_link())
            self.assertEqual("<a href=\"/articles/\">Articles &amp; Things</a>", articles.get_link())
            self.assertEqual("<a href=\"/dog/\">I Got to Pet the &lt;Perfect&gt; Dog</a>", article_dog.get_link())

    def test_get_canonical_link_no_title_no_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"https://example.com/\">Index</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/dog/\">Dog</a>", article_dog.get_canonical_link())

    def test_get_canonical_link_no_title_no_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("escape-title", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"https://example.com/\">Index</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/dog/\">Dog</a>", article_dog.get_canonical_link())

    def test_get_canonical_link_no_title_with_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"https://example.com/\">Index</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/dog/\">Dog</a>", article_dog.get_canonical_link())

    def test_get_canonical_link_no_title_with_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            root.set_header("escape-title", "true")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            self.assertEqual("<a href=\"https://example.com/\">Index</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/dog/\">Dog</a>", article_dog.get_canonical_link())

    def test_get_canonical_link_with_title_no_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            # "escape-title: true" is the default
            root.set_header("escape-title", "false")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"https://example.com/\">The 'Home' Page</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles & Things</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/dog/\">I Got to Pet the <Perfect> Dog</a>", article_dog.get_canonical_link())

    def test_get_canonical_link_with_title_no_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            # "escape-title: true" is the default
            root.set_header("escape-title", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"https://example.com/\">The &apos;Home&apos; Page</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles &amp; Things</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/dog/\">I Got to Pet the &lt;Perfect&gt; Dog</a>", article_dog.get_canonical_link())

    def test_get_canonical_link_with_title_with_flat_url_no_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            # "escape-title: true" is the default
            root.set_header("escape-title", "false")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"https://example.com/\">The 'Home' Page</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles & Things</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/dog/\">I Got to Pet the <Perfect> Dog</a>", article_dog.get_canonical_link())

    def test_get_canonical_link_with_title_with_flat_url_with_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("canonical-url", "https://example.com")
            # "escape-title: true" is the default
            root.set_header("escape-title", "true")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.set_header("title", "The 'Home' Page")
            articles.set_header("title", "Articles & Things")
            article_dog.set_header("title", "I Got to Pet the <Perfect> Dog")

            self.assertEqual("<a href=\"https://example.com/\">The &apos;Home&apos; Page</a>", root.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/articles/\">Articles &amp; Things</a>", articles.get_canonical_link())
            self.assertEqual("<a href=\"https://example.com/dog/\">I Got to Pet the &lt;Perfect&gt; Dog</a>", article_dog.get_canonical_link())

    def test_get_link_prefix_no_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual("<p>", root.get_link_prefix())

    def test_get_link_prefix_with_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("link-prefix", "<div class=\"foo\">")

            self.assertEqual("<div class=\"foo\">", root.get_link_prefix())

    def test_get_link_suffix_no_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual("</p>", root.get_link_suffix())

    def test_get_link_suffix_with_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("link-suffix", "</div>")

            self.assertEqual("</div>", root.get_link_suffix())

    def test_get_tags_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual(0, len(root.get_tags()))

    def test_get_tags_basic(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo, bar, baz-quux, 42")

            tags = root.get_tags()
            self.assertEqual(4, len(tags))
            self.assertTrue("foo" in tags)
            self.assertTrue("bar" in tags)
            self.assertTrue("baz-quux" in tags)
            self.assertTrue("42" in tags)

    def test_get_tags_duplicate(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo, foo, bar, baz, quux, quux")

            tags = root.get_tags()
            self.assertEqual(4, len(tags))
            self.assertTrue("foo" in tags)
            self.assertTrue("bar" in tags)
            self.assertTrue("baz" in tags)
            self.assertTrue("quux" in tags)

    def test_get_tags_empty_element(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo,,bar")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_whitespace_only_element(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo, , bar")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_trailing_separator(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo, bar, ")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_only_separators(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", " , , ")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_valid_capital(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "Aardvark")

            tags = root.get_tags()
            self.assertTrue("Aardvark" in tags)

    def test_get_tags_invalid_space(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo bar")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_invalid_hash(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "c#")

            try:
                root.get_tags()
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "invalid tag 'c#' in node 'index', " + \
                    "can not contain '#', '?' or '%'",
                    str(e))

    def test_get_tags_invalid_question_mark(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "what?")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_invalid_percent(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "100%pure")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_invalid_url_character_among_valid_tags(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo, c#, bar")

            self.assertRaises(uriel.UrielError, root.get_tags)

    def test_get_tags_valid_url_safe_punctuation(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "c++, a_b, 42, Aardvark, baz-quux")

            tags = root.get_tags()
            self.assertEqual(5, len(tags))
            self.assertTrue("c++" in tags)
            self.assertTrue("a_b" in tags)
            self.assertTrue("42" in tags)
            self.assertTrue("Aardvark" in tags)
            self.assertTrue("baz-quux" in tags)

    def test_get_tags_valid_underscore(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo_bar")

            tags = root.get_tags()
            self.assertTrue("foo_bar" in tags)

    def test_get_tags_invalid_slash(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "foo/bar")

            # a tag is used as a directory name
            try:
                root.get_tags()
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "invalid tag 'foo/bar' in node 'index', " + \
                    "can not contain '/'",
                    str(e))

    def test_get_tags_invalid_dot(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", ".")

            try:
                root.get_tags()
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "invalid tag '.' in node 'index', " + \
                    "can not be '.' or '..'",
                    str(e))

    def test_get_tags_invalid_double_dot(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "..")

            try:
                root.get_tags()
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "invalid tag '..' in node 'index', " + \
                    "can not be '.' or '..'",
                    str(e))

    def test_get_tags_valid_triple_dot(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "..., .hidden")

            tags = root.get_tags()
            self.assertEqual(2, len(tags))
            self.assertTrue("..." in tags)
            self.assertTrue(".hidden" in tags)

    def test_get_dest_dir_no_flat_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            expected_root_dir = os.path.join(project_root, "public")
            expected_articles_dir = os.path.join(project_root, "public/articles")
            expected_article_dog_dir = os.path.join(project_root, "public/articles/dog")

            self.assertEqual(expected_root_dir, root.get_dest_dir())
            self.assertEqual(expected_articles_dir, articles.get_dest_dir())
            self.assertEqual(expected_article_dog_dir, article_dog.get_dest_dir())

    def test_get_dest_dir_with_flat_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            expected_root_dir = os.path.join(project_root, "public")
            expected_articles_dir = os.path.join(project_root, "public/articles")
            expected_article_dog_dir = os.path.join(project_root, "public/dog")

            self.assertEqual(expected_root_dir, root.get_dest_dir())
            self.assertEqual(expected_articles_dir, articles.get_dest_dir())
            self.assertEqual(expected_article_dog_dir, article_dog.get_dest_dir())

    def test_get_dest_file_no_flat_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            expected_root_file = os.path.join(project_root, "public/index.html")
            expected_articles_file = os.path.join(project_root, "public/articles/index.html")
            expected_article_dog_file = os.path.join(project_root, "public/articles/dog/index.html")

            self.assertEqual(expected_root_file, root.get_dest_file())
            self.assertEqual(expected_articles_file, articles.get_dest_file())
            self.assertEqual(expected_article_dog_file, article_dog.get_dest_file())

    def test_get_dest_file_with_flat_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("flat-url", "true")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            expected_root_file = os.path.join(project_root, "public/index.html")
            expected_articles_file = os.path.join(project_root, "public/articles/index.html")
            expected_article_dog_file = os.path.join(project_root, "public/dog/index.html")

            self.assertEqual(expected_root_file, root.get_dest_file())
            self.assertEqual(expected_articles_file, articles.get_dest_file())
            self.assertEqual(expected_article_dog_file, article_dog.get_dest_file())

    def test_get_boolean_header_value_true_default_true(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "true")

            self.assertTrue(root.get_boolean_header_value("foo", True))

    def test_get_boolean_header_value_false_default_true(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "false")

            self.assertFalse(root.get_boolean_header_value("foo", True))

    def test_get_boolean_header_value_missing_default_true(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertTrue(root.get_boolean_header_value("foo", True))

    def test_get_boolean_header_value_invalid_default_true(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")

            self.assertRaises(uriel.UrielError,
                              root.get_boolean_header_value,
                              "foo", True)

    def test_get_boolean_header_value_true_default_false(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "true")

            self.assertTrue(root.get_boolean_header_value("foo", False))

    def test_get_boolean_header_value_false_default_false(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "false")

            self.assertFalse(root.get_boolean_header_value("foo", False))

    def test_get_boolean_header_value_missing_default_false(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertFalse(root.get_boolean_header_value("foo", False))

    def test_get_boolean_header_value_invalid_default_false(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")

            self.assertRaises(uriel.UrielError,
                              root.get_boolean_header_value,
                              "foo", False)

    def test_get_format_not_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            # html is the default when the Format header is not set
            self.assertEqual("html", root.get_format())

    def test_get_format_html(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("format", "html")

            self.assertEqual("html", root.get_format())

    def test_get_format_text(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("format", "text")

            self.assertEqual("text", root.get_format())

    def test_get_format_invalid(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("format", "bogus")

            self.assertRaises(uriel.UrielError, root.get_format)

    def test_get_format_inherited_invalid(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("format", "text")
            child = uriel.VirtualNode(project_root, "child", root)
            child.set_header("format", "bogus")

            # the parent is still valid, the child is not
            self.assertEqual("text", root.get_format())
            self.assertRaises(uriel.UrielError, child.get_format)

    def test_get_breadcrumb_separator_no_separator_no_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("breadcrumb-separator-spaces", "false")

            self.assertEqual("&raquo;", root.get_breadcrumb_separator())

    def test_get_breadcrumb_separator_with_separator_no_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("breadcrumb-separator", "/")
            root.set_header("breadcrumb-separator-spaces", "false")

            self.assertEqual("/", root.get_breadcrumb_separator())

    def test_get_breadcrumb_separator_no_separator_with_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual(" &raquo; ", root.get_breadcrumb_separator())

    def test_get_breadcrumb_separator_with_separator_with_spaces(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("breadcrumb-separator", "/")

            self.assertEqual(" / ", root.get_breadcrumb_separator())

    def test_find_node_by_path_with_exceptions_by_default(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.add_child(articles)
            articles.add_child(article_dog)

            self.assertEqual(root, root.find_node_by_path("index"))
            self.assertEqual(root, articles.find_node_by_path("index"))
            self.assertEqual(root, article_dog.find_node_by_path("index"))

            self.assertEqual(articles, root.find_node_by_path("articles/index"))
            self.assertEqual(articles, articles.find_node_by_path("articles/index"))
            self.assertEqual(articles, article_dog.find_node_by_path("articles/index"))

            self.assertEqual(article_dog, root.find_node_by_path("articles/dog"))
            self.assertEqual(article_dog, articles.find_node_by_path("articles/dog"))
            self.assertEqual(article_dog, article_dog.find_node_by_path("articles/dog"))

            self.assertRaises(uriel.UrielError, root.find_node_by_path, "does-not-exist")
            self.assertRaises(uriel.UrielError, articles.find_node_by_path, "does-not-exist")
            self.assertRaises(uriel.UrielError, article_dog.find_node_by_path, "does-not-exist")

    def test_find_node_by_path_no_exceptions(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.add_child(articles)
            articles.add_child(article_dog)

            self.assertEqual(root, root.find_node_by_path("index", raise_exceptions=False))
            self.assertEqual(root, articles.find_node_by_path("index", raise_exceptions=False))
            self.assertEqual(root, article_dog.find_node_by_path("index", raise_exceptions=False))

            self.assertEqual(articles, root.find_node_by_path("articles/index", raise_exceptions=False))
            self.assertEqual(articles, articles.find_node_by_path("articles/index", raise_exceptions=False))
            self.assertEqual(articles, article_dog.find_node_by_path("articles/index", raise_exceptions=False))

            self.assertEqual(article_dog, root.find_node_by_path("articles/dog", raise_exceptions=False))
            self.assertEqual(article_dog, articles.find_node_by_path("articles/dog", raise_exceptions=False))
            self.assertEqual(article_dog, article_dog.find_node_by_path("articles/dog", raise_exceptions=False))

            self.assertIsNone(root.find_node_by_path("does-not-exist", raise_exceptions=False))
            self.assertIsNone(articles.find_node_by_path("does-not-exist", raise_exceptions=False))
            self.assertIsNone(article_dog.find_node_by_path("does-not-exist", raise_exceptions=False))

    def test_find_node_by_path_with_exceptions(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.add_child(articles)
            articles.add_child(article_dog)

            self.assertEqual(root, root.find_node_by_path("index", raise_exceptions=True))
            self.assertEqual(root, articles.find_node_by_path("index", raise_exceptions=True))
            self.assertEqual(root, article_dog.find_node_by_path("index", raise_exceptions=True))

            self.assertEqual(articles, root.find_node_by_path("articles/index", raise_exceptions=True))
            self.assertEqual(articles, articles.find_node_by_path("articles/index", raise_exceptions=True))
            self.assertEqual(articles, article_dog.find_node_by_path("articles/index", raise_exceptions=True))

            self.assertEqual(article_dog, root.find_node_by_path("articles/dog", raise_exceptions=True))
            self.assertEqual(article_dog, articles.find_node_by_path("articles/dog", raise_exceptions=True))
            self.assertEqual(article_dog, article_dog.find_node_by_path("articles/dog", raise_exceptions=True))

            self.assertRaises(uriel.UrielError,
                              root.find_node_by_path,
                              "does-not-exist", raise_exceptions=True)
            self.assertRaises(uriel.UrielError,
                              articles.find_node_by_path,
                              "does-not-exist", raise_exceptions=True)
            self.assertRaises(uriel.UrielError,
                              article_dog.find_node_by_path,
                              "does-not-exist", raise_exceptions=True)

    def test_get_root_node(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)

            root.add_child(articles)
            articles.add_child(article_dog)

            self.assertEqual(root, root.get_root_node())
            self.assertEqual(root, articles.get_root_node())
            self.assertEqual(root, article_dog.get_root_node())

    def test_get_tag_node_not_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            tag = uriel.VirtualNode(project_root, "tag", root)
            root.add_child(tag)

            self.assertIsNone(root.get_tag_node())

    def test_get_tag_node_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            tag = uriel.VirtualNode(project_root, "tag", root)
            root.add_child(tag)

            self.assertEqual(tag, root.get_tag_node())

    def test_get_tag_node_set_incorrectly(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "does-not-exist")
            tag = uriel.VirtualNode(project_root, "tag", root)
            root.add_child(tag)

            self.assertRaises(uriel.UrielError, root.get_tag_node)

    def test_get_tag_node_index_not_set(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertRaises(uriel.UrielError, root.get_tag_node_index)

    def test_get_set_tag_node_index(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            tag = uriel.VirtualNode(project_root, "tag", root)
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)
            article_cat = uriel.VirtualNode(project_root, "articles/cat", articles)
            root.add_child(tag)
            root.add_child(articles)
            articles.add_child(article_cat)
            articles.add_child(article_dog)

            article_cat.set_header("tags", "pet, meow")
            article_dog.set_header("tags", "pet, woof")

            tag_node_index = {}
            tag_node_index["pet"] = set((article_cat, article_dog))
            tag_node_index["meow"] = set((article_cat,))
            tag_node_index["woof"] = set((article_dog,))

            articles.set_tag_node_index(tag_node_index)

            self.assertEqual(tag_node_index, root.get_tag_node_index())

    def test_create_tag_node_index(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            tag = uriel.VirtualNode(project_root, "tag", root)
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)
            article_cat = uriel.VirtualNode(project_root, "articles/cat", articles)
            root.add_child(tag)
            root.add_child(articles)
            articles.add_child(article_cat)
            articles.add_child(article_dog)

            article_cat.set_header("tags", "pet, meow")
            article_dog.set_header("tags", "pet, woof")

            root.create_tag_node_index()

            tag_node_index = root.get_tag_node_index()

            pet_tag_nodes = tag_node_index["pet"]
            meow_tag_nodes = tag_node_index["meow"]
            woof_tag_nodes = tag_node_index["woof"]

            self.assertEqual(3, len(tag_node_index))
            self.assertEqual(2, len(pet_tag_nodes))
            self.assertEqual(1, len(meow_tag_nodes))
            self.assertEqual(1, len(woof_tag_nodes))
            self.assertTrue(article_cat in pet_tag_nodes)
            self.assertTrue(article_dog in pet_tag_nodes)
            self.assertTrue(article_cat in meow_tag_nodes)
            self.assertTrue(article_dog in woof_tag_nodes)

    def test_get_vnode_for_tag(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tag-node", "tag")
            tag = uriel.VirtualNode(project_root, "tag", root)
            articles = uriel.VirtualNode(project_root, "articles/index", root)
            article_dog = uriel.VirtualNode(project_root, "articles/dog", articles)
            article_cat = uriel.VirtualNode(project_root, "articles/cat", articles)
            root.add_child(tag)
            root.add_child(articles)
            articles.add_child(article_cat)
            articles.add_child(article_dog)

            article_cat.set_header("tags", "pet, meow")
            article_dog.set_header("tags", "pet, woof")

            # create tag vnodes
            pet_tag = uriel.VirtualNode(project_root, "tag/pet", tag)
            meow_tag = uriel.VirtualNode(project_root, "tag/meow", tag)
            woof_tag = uriel.VirtualNode(project_root, "tag/woof", tag)
            tag.add_child(pet_tag)
            tag.add_child(meow_tag)
            tag.add_child(woof_tag)

            self.assertEqual(pet_tag, root.get_vnode_for_tag("pet"))
            self.assertEqual(meow_tag, root.get_vnode_for_tag("meow"))
            self.assertEqual(woof_tag, root.get_vnode_for_tag("woof"))
            self.assertIsNone(root.get_vnode_for_tag("does-not-exist"))

    def test_get_set_body(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertIsNone(root.get_body())
            self.assertIsNone(root.get_rendered_body())

            root.set_body(None)
            self.assertIsNone(root.get_body())

            root.set_body("<p>{{value:foo}}</p>")
            self.assertEqual("<p>{{value:foo}}</p>", root.get_body())

            self.assertIsNone(root.get_rendered_body())

    def test_get_set_rendered_body(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertIsNone(root.get_body())
            self.assertIsNone(root.get_rendered_body())

            root.set_rendered_body(None)
            self.assertIsNone(root.get_rendered_body())

            root.set_rendered_body("<p>bar</p>")
            self.assertEqual("<p>bar</p>", root.get_rendered_body())

            self.assertIsNone(root.get_body())

    def test_has_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            root.set_header("foo", "bar")

            self.assertTrue(root.has_header("foo"))
            self.assertTrue(root.has_header("Foo"))
            self.assertTrue(root.has_header("FOO"))

            self.assertFalse(root.has_header("quux"))
            self.assertFalse(root.has_header("Quux"))
            self.assertFalse(root.has_header("QUUX"))

    def test_get_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            root.set_header("foo", "bar")

            self.assertEqual("bar", root.get_header("foo"))
            self.assertEqual("bar", root.get_header("Foo"))
            self.assertEqual("bar", root.get_header("FOO"))

            self.assertRaises(Exception, root.get_header, "quux")
            self.assertRaises(Exception, root.get_header, "Quux")
            self.assertRaises(Exception, root.get_header, "QUUX")

    def test_invalidate_cache_by_header_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.title_cache = "Cached Title"
            root.url_cache = "/"
            root.invalidate_cache_by_header("title")

            self.assertIsNone(root.title_cache)
            self.assertEqual("/", root.url_cache)

    def test_invalidate_cache_by_header_escape_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.title_cache = "Cached Title"
            root.url_cache = "/"
            root.invalidate_cache_by_header("escape-title")

            self.assertIsNone(root.title_cache)
            self.assertEqual("/", root.url_cache)

    def test_invalidate_cache_by_header_flat_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.title_cache = "Cached Title"
            root.url_cache = "/"
            root.invalidate_cache_by_header("flat-url")

            self.assertEqual("Cached Title", root.title_cache)
            self.assertIsNone(root.url_cache)

    def test_invalidate_cache_by_header_tags(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("tags", "alpha")

            self.assertEqual(["alpha"], root.get_tags())

            root.set_header("tags", "beta, gamma")
            self.assertEqual(["beta", "gamma"], root.get_tags())

            root.delete_header("tags")
            self.assertEqual([], root.get_tags())

    def test_invalidate_cache_by_header_tag_node(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            one = uriel.VirtualNode(project_root, "one", root)
            root.add_child(one)
            two = uriel.VirtualNode(project_root, "two", root)
            root.add_child(two)

            root.set_header("tag-node", "one")
            self.assertEqual("one", root.get_tag_node().get_path())

            root.set_header("tag-node", "two")
            self.assertEqual("two", root.get_tag_node().get_path())

    def test_invalidate_cache_by_header_tag_node_clears_vnode_cache(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            root.tag_vnode_cache["stale"] = root

            root.set_header("tag-node", "tag")

            self.assertEqual({}, root.tag_vnode_cache)

    def test_invalidate_cache_by_header_flat_url_child_nodes(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            a = uriel.VirtualNode(project_root, "a/index", root)
            root.add_child(a)
            b = uriel.VirtualNode(project_root, "a/b/index", a)
            a.add_child(b)
            leaf = uriel.VirtualNode(project_root, "a/b/leaf", b)
            b.add_child(leaf)

            self.assertEqual("/a/b/", b.get_url())
            self.assertEqual("/a/b/leaf/", leaf.get_url())

            b.set_header("flat-url", "true")

            self.assertEqual("/b/", b.get_url())
            self.assertEqual("/b/leaf/", leaf.get_url())

    def test_invalidate_cache_by_header_flat_url_keeps_name(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            a = uriel.VirtualNode(project_root, "a/index", root)
            root.add_child(a)
            b = uriel.VirtualNode(project_root, "a/b/index", a)
            a.add_child(b)

            self.assertEqual("/a/b/", b.get_url())
            self.assertEqual("b", b.get_name())
            self.assertEqual("B", b.get_title())

            b.set_header("flat-url", "true")

            self.assertEqual("/b/", b.get_url())
            self.assertEqual("b", b.get_name())
            self.assertEqual("B", b.get_title())

    def test_set_header_basic(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            root.set_header("foo", "bar")
            root.set_header("Baz", "quux")

            self.assertEqual("bar", root.get_header("foo"))
            self.assertEqual("quux", root.get_header("baz"))

    def test_set_header_invalidates_cache(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.title_cache = "Cached Title"
            root.url_cache = "/"
            root.set_header("title", "A New Title")

            self.assertEqual("A New Title", root.get_header("title"))
            self.assertIsNone(root.title_cache)
            self.assertEqual("/", root.url_cache)

    def test_delete_header_basic(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            root.set_header("foo", "bar")
            root.set_header("baz", "quux")
            root.delete_header("foo")
            root.delete_header("Baz")

            self.assertFalse(root.has_header("foo"))
            self.assertFalse(root.has_header("baz"))

    def test_delete_header_invalidates_cache(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.title_cache = "Cached Title"
            root.url_cache = "/"
            root.set_header("title", "A New Title")
            root.delete_header("title")

            self.assertIsNone(root.title_cache)
            self.assertEqual("/", root.url_cache)

    def test_delete_header_that_doesnt_exist(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertRaises(Exception, root.delete_header, "foo")

    def test_get_header_keys_no_headers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual(0, len(root.get_header_keys()))

    def test_get_header_keys(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("title", "Home Page")
            root.set_header("flat-url", "true")

            header_keys = root.get_header_keys()

            self.assertEqual(3, len(header_keys))
            self.assertTrue("foo" in header_keys)
            self.assertTrue("title" in header_keys)
            self.assertTrue("flat-url" in header_keys)

    def test_get_header_key_values_no_headers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual(0, len(root.get_header_key_values()))

    def test_get_header_key_values(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")
            root.set_header("foo", "bar")
            root.set_header("title", "Home Page")
            root.set_header("flat-url", "true")

            header_key_values = root.get_header_key_values()

            self.assertEqual(3, len(header_key_values))
            self.assertTrue(("foo", "bar") in header_key_values)
            self.assertTrue(("title", "Home Page") in header_key_values)
            self.assertTrue(("flat-url", "true") in header_key_values)

    def test_get_datetime_from_date_str_none(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertRaises(uriel.UrielError,
                              root.get_datetime_from_date_str,
                              None)

    def test_get_datetime_from_date_str_invalid_string(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertRaises(uriel.UrielError,
                              root.get_datetime_from_date_str,
                              "now")

    def test_get_datetime_from_date_str_with_timezone(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            dt = root.get_datetime_from_date_str("2025-08-24T17:08:37-04:00")

            # date/time
            self.assertEqual(2025, dt.year)
            self.assertEqual(8, dt.month)
            self.assertEqual(24, dt.day)
            self.assertEqual(17, dt.hour)
            self.assertEqual(8, dt.minute)
            self.assertEqual(37, dt.second)

            # time zone (EDT -04:00 from UTC)
            self.assertEqual(
                datetime.timezone(datetime.timedelta(days=-1, seconds=72000)),
                dt.tzinfo)

    def test_get_datetime_from_date_str_without_timezone(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            dt = root.get_datetime_from_date_str("2025-08-24T17:08:37")

            # date/time
            self.assertEqual(2025, dt.year)
            self.assertEqual(8, dt.month)
            self.assertEqual(24, dt.day)
            self.assertEqual(17, dt.hour)
            self.assertEqual(8, dt.minute)
            self.assertEqual(37, dt.second)

            # whatever the local time zone is here
            self.assertEqual(type(dt.tzinfo), datetime.timezone)

    def test_get_datetime_from_date_str_without_timezone_dst(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            # a date without a time zone gets the UTC offset that was in
            # effect locally on that date, not the one in effect today.
            # a winter date and a summer date in the same time zone
            # therefore get different offsets.
            with TimeZone("America/Los_Angeles"):
                winter = root.get_datetime_from_date_str("2020-01-15T23:30:00")
                summer = root.get_datetime_from_date_str("2020-07-04T10:00:00")

            # the date/time written in the header is never shifted
            self.assertEqual(23, winter.hour)
            self.assertEqual(30, winter.minute)
            self.assertEqual(15, winter.day)

            self.assertEqual(10, summer.hour)
            self.assertEqual(0, summer.minute)
            self.assertEqual(4, summer.day)

            # PST in January, PDT in July
            self.assertEqual("-0800", winter.strftime("%z"))
            self.assertEqual("-0700", summer.strftime("%z"))

    def test_get_datetime_from_date_str_with_timezone_is_preserved(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            # an explicit UTC offset is kept exactly as written, and does
            # not depend on the local time zone at all
            with TimeZone("Asia/Tokyo"):
                dt = root.get_datetime_from_date_str(
                    "2020-07-04T10:00:00-04:00")

            self.assertEqual(10, dt.hour)
            self.assertEqual("-0400", dt.strftime("%z"))

    def test_node_sorting_created_with_the_same_time_zone(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            a = uriel.VirtualNode(project_root, "index")
            a.created = get_datetime_from_date_str("1970-01-02T00:00:00-04:00")

            b = uriel.VirtualNode(project_root, "index")
            b.created = get_datetime_from_date_str("1970-01-01T00:00:00-04:00")

            self.assertTrue(a < b)
            self.assertFalse(a > b)

    def test_node_sorting_created_with_the_local_time_zone(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # a date written without a UTC offset gets the local one
            # attached to it, so both of these end up with a time zone
            a = uriel.VirtualNode(project_root, "index")
            a.created = get_datetime_from_date_str("1970-01-02T00:00:00")

            b = uriel.VirtualNode(project_root, "index")
            b.created = get_datetime_from_date_str("1970-01-01T00:00:00")

            self.assertTrue(a < b)
            self.assertFalse(a > b)

    def test_node_sorting_created_with_different_time_zones(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            # a date written without a UTC offset gets the local one
            # attached to it, so both of these end up with a time zone,
            # but with different offsets
            #
            # the local offset varies with the machine running the test,
            # so the two dates are placed more than 24 hours apart, to
            # overcome any potential time zone slop
            a = uriel.VirtualNode(project_root, "index")
            a.created = get_datetime_from_date_str("1970-01-03T00:00:00")

            b = uriel.VirtualNode(project_root, "index")
            b.created = get_datetime_from_date_str("1970-01-01T00:00:00-04:00")

            self.assertTrue(a < b)
            self.assertFalse(a > b)

    def test_node_sorting_created_one_without_a_time_zone(self):
        c = UrielContainer()
        uriel = c.uriel

        with TimeZone("UTC"):
            with TempDir() as project_root:
                # a date without a time zone can not be compared against
                # one that has a time zone, so both are converted to
                # seconds since the epoch. the one with a time zone has
                # to keep its own UTC offset while that happens.
                a = uriel.VirtualNode(project_root, "a")
                a.created = datetime.datetime.fromisoformat(
                    "2020-01-01T00:00:00+09:00")

                b = uriel.VirtualNode(project_root, "b")
                b.created = datetime.datetime(2019, 12, 31, 20, 0, 0)

                # a is 2019-12-31T15:00Z, b is 2019-12-31T20:00Z, so b is
                # the more recent of the two, and sorts first
                self.assertTrue(b < a)
                self.assertFalse(a < b)

                self.assertEqual(["b", "a"],
                                 [n.get_path() for n in sorted([a, b])])

    def test_node_sorting_created_neither_with_a_time_zone(self):
        c = UrielContainer()
        uriel = c.uriel

        with TimeZone("UTC"):
            with TempDir() as project_root:
                a = uriel.VirtualNode(project_root, "a")
                a.created = datetime.datetime(2019, 12, 31, 15, 0, 0)

                b = uriel.VirtualNode(project_root, "b")
                b.created = datetime.datetime(2019, 12, 31, 20, 0, 0)

                self.assertEqual(["b", "a"],
                                 [n.get_path() for n in sorted([a, b])])

    def test_node_sorting_created_without_a_time_zone_sub_second(self):
        c = UrielContainer()
        uriel = c.uriel

        with TimeZone("UTC"):
            with TempDir() as project_root:
                # node modified times come from file mtimes, which carry
                # microseconds, so dates within the same second are
                # compared at full precision rather than being treated
                # as equal
                a = uriel.VirtualNode(project_root, "a")
                a.created = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)

                b = uriel.VirtualNode(project_root, "b")
                b.created = datetime.datetime(2020, 1, 1, 0, 0, 0, 1)

                self.assertEqual(["b", "a"],
                                 [n.get_path() for n in sorted([a, b])])

    def test_node_sorting_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            a = uriel.VirtualNode(project_root, "index")
            a.created = get_datetime_from_date_str("1970-01-01T00:00:00+00:00")
            a.set_header("title", "a")

            b = uriel.VirtualNode(project_root, "index")
            b.created = get_datetime_from_date_str("1970-01-01T00:00:00+00:00")
            b.set_header("title", "b")

            self.assertTrue(a < b)
            self.assertFalse(a > b)

    def test_node_sorting_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            a = uriel.VirtualNode(project_root, "a")
            a.created = get_datetime_from_date_str("1970-01-01T00:00:00+00:00")
            a.set_header("title", "foo")

            b = uriel.VirtualNode(project_root, "b")
            b.created = get_datetime_from_date_str("1970-01-01T00:00:00+00:00")
            b.set_header("title", "foo")

            self.assertTrue(a < b)
            self.assertFalse(a > b)

    def test_node_sorting_created_before_title(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            a = uriel.VirtualNode(project_root, "index")
            a.created = get_datetime_from_date_str("1970-01-02T00:00:00+00:00")
            a.set_header("title", "b")

            b = uriel.VirtualNode(project_root, "index")
            b.created = get_datetime_from_date_str("1970-01-01T00:00:00+00:00")
            b.set_header("title", "a")

            self.assertTrue(a < b)
            self.assertFalse(a > b)

    def test_node_sorting_title_before_url(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            a = uriel.VirtualNode(project_root, "zzzzz")
            a.created = get_datetime_from_date_str("1970-01-01T00:00:00+00:00")
            a.set_header("title", "a")

            b = uriel.VirtualNode(project_root, "aaaaa")
            b.created = get_datetime_from_date_str("1970-01-01T00:00:00+00:00")
            b.set_header("title", "b")

            self.assertTrue(a < b)
            self.assertFalse(a > b)


class TestFileNode(unittest.TestCase):
    """
    Tests the FileNode class.

    """

    def test_missing_node_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            self.assertRaises(uriel.UrielError,
                              uriel.FileNode,
                              project_root, "index")

    def test_empty_node_file(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root_dir = os.path.join(project_root, "nodes")
            node_index_file = os.path.join(nodes_root_dir, "index")

            os.mkdir(nodes_root_dir)

            with open(node_index_file, "w") as f:
                f.close()

            root = uriel.FileNode(project_root, "index")

            self.assertEqual(0, len(root.headers))

            self.assertIsNone(root.created)

            node_file_mtime = os.path.getmtime(node_index_file)
            node_modified = \
                datetime.datetime.fromtimestamp(
                    node_file_mtime,
                    datetime.datetime.now(
                        datetime.timezone.utc
                    ).astimezone().tzinfo
                )
            self.assertEqual(root.modified, node_modified)

            self.assertEqual("", root.body)

            self.assertEqual("Index", root.get_title())
            self.assertEqual("index", root.get_path())
            self.assertEqual("/", root.get_url())
            self.assertEqual(root, root.get_root_node())
            self.assertEqual(0, len(root.get_children()))

    def test_get_node_type(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("\n")
                f.close()

            root = uriel.FileNode(project_root, "index")

            self.assertEqual("file", root.get_node_type())

    def test_basic_headers_and_body(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Title: My Test Node\n")
                f.write("Created: 2020-10-24T23:19:38-05:00\n")
                f.write("Modified: 2021-07-08T02:26:08-04:00\n")
                f.write("Tags: aardvark, quokka, walrus\n")
                f.write("\n")
                f.write("<p>Words</p>\n")
                f.close()

            root = uriel.FileNode(project_root, "index")
            self.assertEqual("My Test Node", root.get_title())

            tags = root.get_tags()
            self.assertEqual(3, len(tags))
            self.assertTrue("aardvark" in tags)
            self.assertTrue("quokka" in tags)
            self.assertTrue("walrus" in tags)

            created = get_datetime_from_date_str("2020-10-24T23:19:38-05:00")
            modified = get_datetime_from_date_str("2021-07-08T02:26:08-04:00")
            
            self.assertEqual(created, root.created)
            self.assertEqual(modified, root.modified)

            self.assertEqual("<p>Words</p>", root.body)
            
    def test_no_headers_only_body(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("<p>Words</p>\n")
                f.close()

            root = uriel.FileNode(project_root, "index")

            self.assertEqual(0, len(root.headers))
            self.assertEqual("<p>Words</p>", root.body)

    def test_no_headers_blank_line_then_body(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("\n")
                f.write("<p>Words</p>\n")
                f.close()

            root = uriel.FileNode(project_root, "index")

            self.assertEqual(0, len(root.headers))
            self.assertEqual("\n<p>Words</p>", root.body)

    def test_headers_no_blank_line_then_body(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Title: My Test Node\n")
                f.write("<p>Words</p>\n")
                f.close()

            root = uriel.FileNode(project_root, "index")

            self.assertEqual(1, len(root.headers))
            self.assertEqual("My Test Node", root.get_title())
            self.assertEqual("<p>Words</p>", root.body)

    def test_header_inheritance_plus(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Template: root.html\n")
                f.write("+Template: child.html\n")
                f.close()

            with open(node_child, "w") as f:
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            self.assertTrue(root.has_header("template"))
            self.assertTrue(root.has_header("+template"))
            self.assertFalse(child.has_header("+template"))
            self.assertEqual("root.html", root.get_header("template"))
            self.assertEqual("child.html", child.get_header("template"))

    def test_header_inheritance_plus_plus(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            articles_dir = os.path.join(project_root, "nodes", "articles")
            node_index = os.path.join(nodes_root, "index")
            node_articles_index = os.path.join(nodes_root, "articles/index")
            node_articles_foo = os.path.join(nodes_root, "articles/foo")
            node_articles_bar = os.path.join(nodes_root, "articles/bar")

            os.mkdir(nodes_root)
            os.mkdir(articles_dir)

            with open(node_index, "w") as f:
                f.write("Template: root.html\n")
                f.write("+Template: articles-index.html\n")
                f.write("++Template: article.html\n")
                f.close()

            with open(node_articles_index, "w") as f:
                f.close()

            with open(node_articles_foo, "w") as f:
                f.close()

            with open(node_articles_bar, "w") as f:
                f.close()

            root = uriel.FileNode(project_root, "index")
            articles = uriel.FileNode(project_root, "articles/index", root)
            foo = uriel.FileNode(project_root, "articles/foo", articles)
            bar = uriel.FileNode(project_root, "articles/bar", articles)

            self.assertTrue(root.has_header("template"))
            self.assertTrue(root.has_header("+template"))
            self.assertTrue(root.has_header("++template"))

            self.assertTrue(articles.has_header("template"))
            self.assertTrue(articles.has_header("+template"))
            self.assertFalse(articles.has_header("++template"))

            self.assertTrue(foo.has_header("template"))
            self.assertFalse(foo.has_header("+template"))
            self.assertFalse(foo.has_header("++template"))

            self.assertTrue(bar.has_header("template"))
            self.assertFalse(bar.has_header("+template"))
            self.assertFalse(bar.has_header("++template"))

            self.assertEqual("root.html", root.get_header("template"))
            self.assertEqual("articles-index.html", articles.get_header("template"))
            self.assertEqual("article.html", foo.get_header("template"))
            self.assertEqual("article.html", bar.get_header("template"))

    def test_header_inheritance_title_created_modified(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            # the root node sets all three of the non-inherited headers,
            # alongside an ordinary header that is inherited normally
            with open(node_index, "w") as f:
                f.write("Title: Root Node\n")
                f.write("Created: 2020-10-24T23:19:38-05:00\n")
                f.write("Modified: 2021-07-08T02:26:08-04:00\n")
                f.write("Foo: bar\n")
                f.close()

            with open(node_child, "w") as f:
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            # none of Title, Created or Modified are inherited, even though
            # the root node sets all three of them at the same time
            self.assertFalse(child.has_header("title"))
            self.assertFalse(child.has_header("created"))
            self.assertFalse(child.has_header("modified"))

            # ordinary headers are still inherited
            self.assertEqual("bar", child.get_header("foo"))

            # the child title falls back to the node name
            self.assertEqual("Child", child.get_title())

            # the child has no created time at all
            self.assertIsNone(child.created)

            # the child modified time comes from its own file mtime,
            # not from the root node
            node_child_mtime = os.path.getmtime(node_child)
            child_modified = \
                datetime.datetime.fromtimestamp(
                    node_child_mtime,
                    datetime.datetime.now(
                        datetime.timezone.utc
                    ).astimezone().tzinfo
                )
            self.assertEqual(child_modified, child.modified)

    def test_header_inheritance_plus_created_and_modified(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Title: Root Node\n")
                f.write("Created: 2020-10-24T23:19:38-05:00\n")
                f.write("+Created: 2022-02-02T02:02:02-05:00\n")
                f.write("Modified: 2021-07-08T02:26:08-04:00\n")
                f.write("+Modified: 2023-03-03T03:03:03-05:00\n")
                f.close()

            with open(node_child, "w") as f:
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            root_created = \
                get_datetime_from_date_str("2020-10-24T23:19:38-05:00")
            root_modified = \
                get_datetime_from_date_str("2021-07-08T02:26:08-04:00")
            self.assertEqual(root_created, root.created)
            self.assertEqual(root_modified, root.modified)

            self.assertFalse(child.has_header("+created"))
            self.assertFalse(child.has_header("+modified"))

            child_created = \
                get_datetime_from_date_str("2022-02-02T02:02:02-05:00")
            child_modified = \
                get_datetime_from_date_str("2023-03-03T03:03:03-05:00")
            self.assertEqual(child_created, child.created)
            self.assertEqual(child_modified, child.modified)

    def test_invalid_format_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Format: bogus\n")
                f.write("\n")
                f.write("<p>Words</p>\n")
                f.close()

            self.assertRaises(uriel.UrielError,
                              uriel.FileNode,
                              project_root, "index")

    def test_invalid_canonical_url_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Canonical-URL: https://example.com/\n")
                f.close()

            self.assertRaises(uriel.UrielError,
                              uriel.FileNode,
                              project_root, "index")

    def test_valid_format_headers(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Format: html\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("Format: text\n")
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            self.assertEqual("html", root.get_format())
            self.assertEqual("text", child.get_format())

    def test_header_inheritance_minus_invalid_value(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Foo: bar\n")
                f.write("Baz: quux\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("-Foo: fail\n")
                f.close()

            root = uriel.FileNode(project_root, "index")

            self.assertRaises(uriel.UrielError,
                              uriel.FileNode,
                              project_root, "child", root)

    def test_header_inheritance_minus(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Foo: bar\n")
                f.write("Baz: quux\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("-Foo: *\n")
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            self.assertEqual("bar", root.get_header("foo"))
            self.assertEqual("quux", root.get_header("baz"))

            self.assertFalse(child.has_header("foo"))
            self.assertEqual("quux", child.get_header("baz"))


    def test_header_inheritance_minus_not_last_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Foo: bar\n")
                f.write("Baz: quux\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("-Foo: *\n")
                f.write("Title: Child\n")
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            self.assertFalse(child.has_header("foo"))
            self.assertEqual("quux", child.get_header("baz"))
            self.assertEqual("Child", child.get_header("title"))

    def test_header_inheritance_minus_invalid_value_not_last_header(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Foo: bar\n")
                f.write("Baz: quux\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("-Foo: fail\n")
                f.write("-Zzz: *\n")
                f.close()

            root = uriel.FileNode(project_root, "index")

            self.assertRaises(uriel.UrielError,
                              uriel.FileNode,
                              project_root, "child", root)

    def test_header_inheritance_minus_invalid_value_message(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Foo: bar\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("-Foo: bogus\n")
                f.close()

            root = uriel.FileNode(project_root, "index")

            try:
                uriel.FileNode(project_root, "child", root)
                self.assertTrue(False)
            except uriel.UrielError as e:
                self.assertEqual(
                    "invalid header in node 'child': " + \
                    "'-foo': 'bogus' (value must be '*')",
                    str(e))

    def test_header_inheritance_minus_key_is_removed(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Foo: bar\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("-Foo: *\n")
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            self.assertFalse(child.has_header("foo"))
            self.assertFalse(child.has_header("-foo"))

    def test_header_inheritance_minus_does_not_block_plus_plus_push(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            sub_dir = os.path.join(nodes_root, "sub")
            deep_dir = os.path.join(sub_dir, "deep")
            node_index = os.path.join(nodes_root, "index")
            node_sub = os.path.join(sub_dir, "index")
            node_deep = os.path.join(deep_dir, "index")

            os.mkdir(nodes_root)
            os.mkdir(sub_dir)
            os.mkdir(deep_dir)

            with open(node_index, "w") as f:
                f.write("++Foo: pushed\n")
                f.close()

            with open(node_sub, "w") as f:
                f.write("-Foo: *\n")
                f.close()

            with open(node_deep, "w") as f:
                f.close()

            root = uriel.FileNode(project_root, "index")
            sub = uriel.FileNode(project_root, "sub/index", root)
            deep = uriel.FileNode(project_root, "sub/deep/index", sub)

            self.assertFalse(root.has_header("foo"))
            self.assertFalse(sub.has_header("foo"))
            self.assertEqual("pushed", deep.get_header("foo"))

    def test_header_inheritance_minus_minus(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            nodes_root = os.path.join(project_root, "nodes")
            node_index = os.path.join(nodes_root, "index")
            node_child = os.path.join(nodes_root, "child")

            os.mkdir(nodes_root)

            with open(node_index, "w") as f:
                f.write("Foo: bar\n")
                f.close()

            with open(node_child, "w") as f:
                f.write("--Foo: *\n")
                f.write("-Foo: *\n")
                f.close()

            root = uriel.FileNode(project_root, "index")
            child = uriel.FileNode(project_root, "child", root)

            self.assertFalse(child.has_header("foo"))
            self.assertFalse(child.has_header("-foo"))
            self.assertFalse(child.has_header("--foo"))


class TestVirtualNode(unittest.TestCase):
    """
    Tests the VirtualNode class.

    """

    def test_constructor(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

    def test_get_node_type(self):
        c = UrielContainer()
        uriel = c.uriel

        with TempDir() as project_root:
            root = uriel.VirtualNode(project_root, "index")

            self.assertEqual("virtual", root.get_node_type())

    def test_root_node_created_modified_times(self):
        c = UrielContainer()
        uriel = c.uriel

        start_time = \
            datetime.datetime.fromtimestamp(
                datetime.datetime.now().timestamp(),
                datetime.datetime.now(
                    datetime.timezone.utc
                ).astimezone().tzinfo
            )

        with TempDir() as project_root:
            # this will use the current date/time when setting the
            # created/modified fields in the VirtualNode, since it does
            # not have a parent node
            root = uriel.VirtualNode(project_root, "index")

            self.assertTrue(type(root.created) is datetime.datetime)
            self.assertTrue(type(root.modified) is datetime.datetime)

            self.assertEqual(root.created, root.modified)

            self.assertTrue(root.created >= start_time)
            self.assertTrue(root.modified >= start_time)

    def test_child_node_inherited_created_modified_times(self):
        c = UrielContainer()
        uriel = c.uriel

        start_time = \
            datetime.datetime.fromtimestamp(
                datetime.datetime.now().timestamp(),
                datetime.datetime.now(
                    datetime.timezone.utc
                ).astimezone().tzinfo
            )

        with TempDir() as project_root:
            # this will use the current date/time when setting the
            # created/modified fields in the VirtualNode, since it does
            # not have a parent node
            root = uriel.VirtualNode(project_root, "index")

            # this will inherit the created/modified fields from the
            # root node
            child_node = uriel.VirtualNode(project_root, "foo", root)

            self.assertTrue(type(child_node.created) is datetime.datetime)
            self.assertTrue(type(child_node.modified) is datetime.datetime)

            self.assertEqual(root.created, child_node.created)
            self.assertEqual(root.modified, child_node.modified)

            self.assertTrue(child_node.created >= start_time)
            self.assertTrue(child_node.modified >= start_time)

