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


def fmt_error(msg, file_path, lineno, offset=0):
    return '{0}: line {1} {2}'.format(file_path, lineno - offset, msg)


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


def missing_href(root, file_path, lineno_offset):
    errors = []
    for link in root.xpath('//xhtml:a', namespaces=NSMAP):
        href = attribute(link, 'href')
        if href is None:
            errors.append(
                fmt_error(
                    '<a> element requires a non-empty href attribute',
                    file_path, link.sourceline, lineno_offset))
        elif href.strip() == '#':
            errors.append(
                fmt_error(
                    '<a> element href attribute should not be a single "#"',
                    file_path, link.sourceline, lineno_offset))
    return errors or None


def missing_link_content(root, file_path, lineno_offset):
    errors = []
    for link in root.xpath('//xhtml:a', namespaces=NSMAP):
        if link.xpath('.//text()'):
            continue
        if link.xpath('.//xhtml:img', namespaces=NSMAP):
            continue
        if attribute(link, 'aria-label'):
            continue
        errors.append(
            fmt_error(
                '<a> requires descriptive content in the form of text, '
                'an image or an "aria-label" attribute',
                file_path, link.sourceline, lineno_offset))
    return errors or None


def missing_alt(root, file_path, lineno_offset):
    errors = []
    for image in root.xpath('//xhtml:img', namespaces=NSMAP):
        alt = attribute(image, 'alt')
        if alt is None:
            errors.append(
                fmt_error(
                    '<img> element requires a non-empty alt attribute',
                    file_path, image.sourceline, lineno_offset))
    return errors or None


class A11yLint(ChameleonLint):

    name = 'a11y-lint'
    title = 'A1y (Accessibility) Lint'

    def cmd(self):
        # Please the ABC by faux-implementing the cmd.
        pass

    def lint(self, file_content, file_path):
        total_errors = []
        if '<!DOCTYPE' not in file_content:
            file_content = DOCTYPE_WRAPPER.format(file_content)
            offset = len(DOCTYPE_WRAPPER.splitlines()) - 1
        root = lxml.etree.parse(io.StringIO(unicode(file_content))).getroot()
        for check in (
                missing_href,
                missing_alt,
                missing_link_content):
            errors = check(root, file_path, offset)
            if errors is not None:
                total_errors.extend(errors)
        return total_errors


def console_script(options):
    console_factory(A11yLint, options)
