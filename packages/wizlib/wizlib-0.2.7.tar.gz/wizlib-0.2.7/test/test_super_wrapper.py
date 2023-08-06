from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from wizlib.super_wrapper import SuperWrapper


class TestSuperWrapper(TestCase):

    def test_super_wrapper(self):

        class Parent(SuperWrapper):
            def execute(self, method, *args, **kwargs):
                print(f"Parent execute before")
                method(self, *args, **kwargs)
                print(f"Parent execute after")

        class InBetween(Parent):
            @Parent.wrap
            def execute(self, method, *args, **kwargs):
                print(f"IB execute before")
                method(self, *args, **kwargs)
                print(f"IB execute after")

        class NewChild(InBetween):
            @InBetween.wrap
            def execute(self, name):
                print(f"Hello {name}")

        with patch('sys.stdout', o:=StringIO()):
            c = NewChild()
            c.execute("Jane")
        o.seek(0)
        r = o.read()
        self.assertEqual(r, "Parent execute before\nIB execute before\nHello Jane\nIB execute after\nParent execute after\n")

