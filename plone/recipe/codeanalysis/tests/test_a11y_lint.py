# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.a11y import A11yLint
from plone.recipe.codeanalysis.a11y import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os


LINK_MISSING_HREF = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a>Link</a>
  </body>
</html>
"""

LINK_SINGLE_FRAGMENT_IDENTIFIER = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="#">Link</a>
  </body>
</html>
"""

LINK_HREF = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html">Link</a>
  </body>
</html>
"""

LINK_TALATTR_HREF = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a tal:attributes="
        name 'Name';
        title 'Title';
        href 'link.html'">Link</a>
  </body>
</html>
"""

LINK_X_NG_ATTR = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a x-ng-href="expression">Link</a>
  </body>
</html>
"""

LINK_TEXT_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html">Link</a>
  </body>
</html>
"""

LINK_TAL_CONTENT_LINK_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html" tal:content="'Link'"></a>
  </body>
</html>
"""

LINK_TAL_CONTENT_CHILD_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><span tal:content="'Link'"></span></a>
  </body>
</html>
"""

LINK_TAL_REPLACE_CHILD_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><tal:block replace="'Link'"></tal:block></a>
  </body>
</html>
"""

LINK_TAL_REPLACE_CHILD_NODE2 = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><span tal:replace="'Link'"></span></a>
  </body>
</html>
"""

LINK_IMG_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"><img src="image.png" alt="Link"/></a>
  </body>
</html>
"""

LINK_ARIA_LABEL_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html" aria-label="Link"></a>
  </body>
</html>
"""

LINK_NO_TEXT_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <a href="link.html"></a>
  </body>
</html>
"""

IMG_MISSING_ALT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <img src="image.png"/>
  </body>
</html>
"""

BUTTON_TEXT_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button>Actionable</button>
  </body>
</html>
"""

BUTTON_NO_CONTENT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button><i class="fa-nice-button"></i></button>
  </body>
</html>
"""

BUTTON_TAL_CONTENT_BUTTON_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button tal:content="'Link'"></button>
  </body>
</html>
"""

BUTTON_TAL_CONTENT_CHILD_NODE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <button><span tal:content="'Link'"></span></button>
  </body>
</html>
"""

LABEL_WITHOUT_FOR_ATTRIBUTE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <label>Label text</label><input type="text"/>
  </body>
</html>
"""

LABEL_WITH_FOR_ATTRIBUTE = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <label for="inputid">Label text</label><input id="inputid" type="text"/>
  </body>
</html>
"""

LABEL_WRAPS_INPUT = """\
<html
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <label><input type="text"/>Label text</label>
  </body>
</html>
"""

# NOTE: tests to add:
#  attributes() for  allowed syntaxes of `tal:attributes`
# tal:replace


class TestA11yLint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestA11yLint, self).setUp()
        self.options.update({
            'a11y-lint': 'True',
        })

    def test_link_requires_href(self):
        self.given_a_file_in_test_dir('invalid.pt', LINK_MISSING_HREF)
        with OutputCapture():
            self.assertFalse(A11yLint(self.options).run())

    def test_link_href_fragment(self):
        self.given_a_file_in_test_dir(
            'invalid.pt', LINK_SINGLE_FRAGMENT_IDENTIFIER)
        with OutputCapture():
            self.assertFalse(A11yLint(self.options).run())

    def test_link_has_href(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_HREF)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_href_tal_attributes(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_TALATTR_HREF)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_href_angular_attribute(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_X_NG_ATTR)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_img_content(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_IMG_CONTENT)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_aria_label_content(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_ARIA_LABEL_CONTENT)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_text_content(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_TEXT_CONTENT)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_tal_content_link_node(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_TAL_CONTENT_LINK_NODE)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_tal_content_child_node(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_TAL_CONTENT_CHILD_NODE)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_tal_replace_child_node(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_TAL_REPLACE_CHILD_NODE)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())
        self.given_a_file_in_test_dir(
            'valid.pt', LINK_TAL_REPLACE_CHILD_NODE2)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_link_has_no_text_content(self):
        self.given_a_file_in_test_dir('invalid.pt', LINK_NO_TEXT_CONTENT)
        with OutputCapture():
            self.assertFalse(A11yLint(self.options).run())

    def test_img_requires_alt(self):
        self.given_a_file_in_test_dir('invalid.pt', IMG_MISSING_ALT)
        with OutputCapture():
            self.assertFalse(A11yLint(self.options).run())

    def test_button_has_text_content(self):
        self.given_a_file_in_test_dir('valid.pt', BUTTON_TEXT_CONTENT)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_button_has_no_text_content(self):
        self.given_a_file_in_test_dir('invalid.pt', BUTTON_NO_CONTENT)
        with OutputCapture():
            self.assertFalse(A11yLint(self.options).run())

    def test_button_has_tal_content_link_node(self):
        self.given_a_file_in_test_dir(
            'valid.pt', BUTTON_TAL_CONTENT_BUTTON_NODE)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_button_has_tal_content_child_node(self):
        self.given_a_file_in_test_dir(
            'valid.pt', BUTTON_TAL_CONTENT_CHILD_NODE)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_label_has_no_for_attribute(self):
        self.given_a_file_in_test_dir(
            'invalid.pt', LABEL_WITHOUT_FOR_ATTRIBUTE)
        with OutputCapture():
            self.assertFalse(A11yLint(self.options).run())

    def test_label_has_for_attribute(self):
        self.given_a_file_in_test_dir(
            'valid.pt', LABEL_WITH_FOR_ATTRIBUTE)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_label_wraps_input(self):
        self.given_a_file_in_test_dir(
            'valid.pt', LABEL_WRAPS_INPUT)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_HREF)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            A11yLint(self.options).run()

        file_exists = os.path.isfile(
            os.path.join(parts_dir, 'a11y-lint.log'))
        rmtree(parts_dir)
        self.assertTrue(file_exists)

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.pt', LINK_HREF)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.pt', LINK_MISSING_HREF)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
