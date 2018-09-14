# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.chameleonlint import ChameleonLint
from plone.recipe.codeanalysis.chameleonlint import DOCTYPE_WRAPPER

import io
import lxml.etree
import sys


PY3 = sys.version_info > (3,)
if PY3:
    unicode = str


NSMAP = {
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'tal': 'http://xml.zope.org/namespaces/tal'}


TAL_ATTRIBUTES = '{{{0}}}attributes'.format(NSMAP['tal'])
TAL_CONTENT_XPATH = (
    './@tal:content|.//*/@tal:content|'
    './/*/@tal:replace|.//tal:block/@replace')


def attribute(node, name):
    found = node.attrib.get(name)
    if found is not None:
        return found
    tal_attributes = node.attrib.get(TAL_ATTRIBUTES)
    if tal_attributes is not None and name in tal_attributes:
        for attr in tal_attributes.split(';'):
            attr = attr.strip()
            key, value = attr.split(None, 1)
            return value
    x_ng_attribute = node.attrib.get('x-ng-{0}'.format(name))
    if x_ng_attribute is not None:
        return x_ng_attribute
    return None


class Context(object):

    _checks = None

    def __init__(self, file_content, file_path):
        self._errors = []
        if '<!DOCTYPE' not in file_content:
            file_content = DOCTYPE_WRAPPER.format(file_content)
            self.lineno_offset = len(DOCTYPE_WRAPPER.splitlines()) - 1
        else:
            self.lineno_offset = 0
        self.file_path = file_path
        self.node = lxml.etree.parse(
            io.StringIO(unicode(file_content))).getroot()

    @classmethod
    def add_check(cls, func):
        if cls._checks is None:
            cls._checks = []
        cls._checks.append(func)
        return func

    def report(self, node, msg):
        self._errors.append('{0}:{1} {2}'.format(
            self.file_path, node.sourceline - self.lineno_offset, msg))

    def run(self):
        for check in self._checks:
            check(self)
        return self._errors


@Context.add_check
def missing_href(context):
    for link in context.node.xpath('//xhtml:a|//a', namespaces=NSMAP):
        role = attribute(link, 'role')
        href = attribute(link, 'href')
        if href is None:
            context.report(
                link,
                'The <a> element is missing the href attribute. '
                'Without the href attribute an anchor represents '
                'a placeholder for where a link might otherwise have '
                'been placed and is invisible for screen readers. '
                'If the <a> is used to create interactive clickable '
                'elements, consider using the <button type=“button”> '
                'element instead for this.')
        elif href.strip() == '#' and role is not 'button':
            context.report(
                link,
                'The <a> element href attribute should not be a single "#", '
                'it can cause the page to scroll back to the top and it adds '
                'an entry to the browser history, so it takes an additional '
                'click of the back button to go to the previous page. '
                'Consider using a <button type=“button”> element to create '
                'interactive clickable elements.')


@Context.add_check
def missing_alt(context):
    for image in context.node.xpath('//xhtml:img|//img', namespaces=NSMAP):
        alt = attribute(image, 'alt')
        if alt is None:
            context.report(
                image,
                'The <img> element requires an alt attribute. The alt '
                'attribute provides descriptive information for an image if a '
                'user for some reason cannot view it (because of slow '
                'connection, an error, or if the user uses a screen reader). '
                'If the image is considered decorative, the alt attribute '
                'should be left empty, but not removed, so screen readers '
                'will ignore the image.')


@Context.add_check
def missing_link_content(context):
    for link in context.node.xpath('//xhtml:a|//a', namespaces=NSMAP):
        if link.xpath('.//text()'):
            continue
        if link.xpath('.//xhtml:img|.//img', namespaces=NSMAP):
            continue
        if link.xpath(TAL_CONTENT_XPATH, namespaces=NSMAP):
            continue
        if attribute(link, 'aria-label'):
            continue
        context.report(
            link,
            'The <a> element requires descriptive content that help users '
            'better understand what they can expect if they click the link. '
            'An <a> element without descriptive text will only announce the '
            'href path to screen reader users. Keep in mind that users of '
            'screen readers have trouble distinguishing icons and need '
            'descriptive text to understand the context of the <button>. '
            'Consider adding descriptive content in the form of text, an '
            'aria-label attribute or an image.')


@Context.add_check
def missing_button_content(context):
    for button in context.node.xpath(
            '//xhtml:button|//button', namespaces=NSMAP):
        if button.xpath('.//text()'):
            continue
        if button.xpath(TAL_CONTENT_XPATH, namespaces=NSMAP):
            continue
        if attribute(button, 'aria-label'):
            continue
        context.report(
            button,
            'The <button> element requires descriptive text that helps users '
            'understand what they can expect when they click it. Keep in mind '
            'that users of screen readers have trouble distinguishing icons '
            'and need descriptive text to understand the context of the '
            '<button>. Consider adding descriptive text in the form of text '
            'or an aria-label attribute.')


@Context.add_check
def missing_for(context):
    for label in context.node.xpath('//xhtml:label|//label', namespaces=NSMAP):
        if label.xpath('.//xhtml:input|.//input', namespaces=NSMAP):
            continue
        label_for = attribute(label, 'for')
        if label_for is None:
            context.report(
                label,
                'The <label> element needs to be explicitly associated with a '
                'form control through the use of the for attribute, whose '
                'value needs to correspond to the value of the id attribute '
                'of the associated form control element (<input>, <textarea> '
                'and <select>).')


class A11yLint(ChameleonLint):
    name = 'a11y-lint'
    title = 'Accessibility Lint'

    def cmd(self):
        # Please the ABC by faux-implementing the cmd.
        pass

    def lint(self, file_content, file_path):
        return Context(file_content, file_path).run()


def console_script(options):
    console_factory(A11yLint, options)
