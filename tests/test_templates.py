# -*- coding: utf-8 -*-
"""Test the templates module of intelmqmail.

Basic test.

Dependencies:
    (none)
Authors:
 *  Bernhard E. Reiter <bernhard@intevation.de>
"""

import os
import string
from tempfile import TemporaryDirectory
import unittest


from intelmqmail import templates

class TemplatesTest(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        "Sets up a directory structure for all template tests."
        self.top_dir_obj = TemporaryDirectory() # will clean itself up
        self.template_dir = os.path.join(self.top_dir_obj.name, 'templates')
        os.mkdir(self.template_dir)

        self.test_contents = """Subject

Bodyline
Bodyline"""

        with open(os.path.join(self.template_dir, "test-template"), "xt") as f:
            f.write(self.test_contents)



    def assertStringTemplatesEqual(self, a, b, msg=None):
        "Assert that string.Templates are equal."
        return self.assertEqual(a.template, b.template, msg=msg)


    def test_full_template_filename(self):
        self.assertEqual(
          templates.full_template_filename(self.template_dir, "test-template"),
          os.path.join(self.template_dir, "test-template"))

        self.assertRaises(ValueError,
                          templates.full_template_filename,
                          self.template_dir,
                          "../test-template")

    def test_read_template(self):
        self.addTypeEqualityFunc(string.Template, 'assertStringTemplatesEqual')

        subject, body = templates.read_template(self.template_dir,
                                                "test-template")
        self.assertEqual(subject, string.Template("Subject"))
        self.assertEqual(body, string.Template("Bodyline\nBodyline\n"))