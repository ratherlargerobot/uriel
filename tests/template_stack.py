import unittest

from .util import UrielContainer

class TestTemplateStack(unittest.TestCase):
    """
    Tests the TemplateStack class.

    """

    def test_simple(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()
        stack.push("default.html", "index", False)
        template = stack.pop()

        self.assertEqual("default.html", template)

    def test_pop(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()
        stack.push("a.html", "articles/index", False)
        stack.push("b.html", "articles/index", False)
        stack.push("c.html", "articles/index", False)

        self.assertEqual("c.html", stack.pop())
        self.assertEqual("b.html", stack.pop())
        self.assertEqual("a.html", stack.pop())
        self.assertRaises(Exception, stack.pop)

    def test_shift(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()
        stack.push("a.html", "articles/index", False)
        stack.push("b.html", "articles/index", False)
        stack.push("c.html", "articles/index", False)

        self.assertEqual("a.html", stack.shift())
        self.assertEqual("b.html", stack.shift())
        self.assertEqual("c.html", stack.shift())
        self.assertRaises(Exception, stack.shift)

    def test_node_body_includes_templates(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()
        stack.push("a.html", "articles/index", False)
        stack.push("b.html", "articles/index", False)
        stack.push("c.html", "articles/index", True)
        stack.push("d.html", "articles/index", True)

        self.assertEqual("d.html", stack.pop())
        self.assertEqual("c.html", stack.pop())
        self.assertEqual("b.html", stack.pop())
        self.assertEqual("a.html", stack.pop())
        self.assertRaises(Exception, stack.pop)

    def test_has_more_elements(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()

        self.assertFalse(stack.has_more_elements())
        stack.push("a.html", "articles/index", False)
        self.assertTrue(stack.has_more_elements())
        stack.push("b.html", "articles/index", False)
        self.assertTrue(stack.has_more_elements())
        stack.push("c.html", "articles/index", False)
        self.assertTrue(stack.has_more_elements())

        self.assertEqual("c.html", stack.pop())
        self.assertTrue(stack.has_more_elements())
        self.assertEqual("b.html", stack.pop())
        self.assertTrue(stack.has_more_elements())
        self.assertEqual("a.html", stack.pop())
        self.assertFalse(stack.has_more_elements())

    def test_basic_template_loop(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()

        stack.push("a.html", "articles/index", False)
        stack.push("b.html", "articles/index", False)

        self.assertRaises(uriel.UrielError,
                          stack.push,
                          "a.html", "articles/index", False)

        self.assertEqual(5, len(c.stderr))
        self.assertEqual("include loop error:", c.stderr[0])
        self.assertEqual("  nodes/articles/index", c.stderr[1])
        self.assertEqual(">>> templates/a.html <<< LOOP STARTS HERE", c.stderr[2])
        self.assertEqual("  > templates/b.html", c.stderr[3])
        self.assertEqual(">>> templates/a.html <<< WOULD REPEAT FOREVER", c.stderr[4])

    def test_deep_template_loop(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()

        stack.push("a.html", "articles/index", False)
        stack.push("b.html", "articles/index", False)
        stack.push("c.html", "articles/index", False)
        stack.push("d.html", "articles/index", False)
        stack.push("e.html", "articles/index", False)

        self.assertRaises(uriel.UrielError,
                          stack.push,
                          "b.html", "articles/index", False)

        self.assertEqual(8, len(c.stderr))
        self.assertEqual("include loop error:", c.stderr[0])
        self.assertEqual("  nodes/articles/index", c.stderr[1])
        self.assertEqual("    templates/a.html", c.stderr[2])
        self.assertEqual(">>> templates/b.html <<< LOOP STARTS HERE", c.stderr[3])
        self.assertEqual("  > templates/c.html", c.stderr[4])
        self.assertEqual("  > templates/d.html", c.stderr[5])
        self.assertEqual("  > templates/e.html", c.stderr[6])
        self.assertEqual(">>> templates/b.html <<< WOULD REPEAT FOREVER", c.stderr[7])

    def test_basic_node_body_template_loop(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()

        stack.push("a.html", "articles/index", False)
        stack.push("b.html", "articles/index", False)

        self.assertRaises(uriel.UrielError,
                          stack.push,
                          "b.html", "articles/index", True)

        self.assertEqual(8, len(c.stderr))
        self.assertEqual("include loop error:", c.stderr[0])
        self.assertEqual("  nodes/articles/index", c.stderr[1])
        self.assertEqual("    templates/a.html", c.stderr[2])
        self.assertEqual(">>> templates/b.html <<< LOOP STARTS HERE", c.stderr[3])
        self.assertEqual("  >   {{node:body}}", c.stderr[4])
        self.assertEqual("  >     nodes/articles/index", c.stderr[5])
        self.assertEqual("  >       {{include:b.html}}", c.stderr[6])
        self.assertEqual(">>>         templates/b.html <<< WOULD REPEAT FOREVER", c.stderr[7])

    def test_deep_node_body_template_loop(self):
        c = UrielContainer()
        uriel = c.uriel

        stack = uriel.TemplateStack()

        stack.push("a.html", "articles/index", False)
        stack.push("b.html", "articles/index", False)
        stack.push("c.html", "articles/index", False)
        stack.push("d.html", "articles/index", False)
        stack.push("e.html", "articles/index", False)

        self.assertRaises(uriel.UrielError,
                          stack.push,
                          "b.html", "articles/index", True)

        self.assertEqual(11, len(c.stderr))
        self.assertEqual("include loop error:", c.stderr[0])
        self.assertEqual("  nodes/articles/index", c.stderr[1])
        self.assertEqual("    templates/a.html", c.stderr[2])
        self.assertEqual(">>> templates/b.html <<< LOOP STARTS HERE", c.stderr[3])
        self.assertEqual("  > templates/c.html", c.stderr[4])
        self.assertEqual("  > templates/d.html", c.stderr[5])
        self.assertEqual("  > templates/e.html", c.stderr[6])
        self.assertEqual("  >   {{node:body}}", c.stderr[7])
        self.assertEqual("  >     nodes/articles/index", c.stderr[8])
        self.assertEqual("  >       {{include:b.html}}", c.stderr[9])
        self.assertEqual(">>>         templates/b.html <<< WOULD REPEAT FOREVER", c.stderr[10])

