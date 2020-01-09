# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from lxml import etree

from odoo import tools
from odoo.tools import view_validation


orig_relaxng = view_validation.relaxng


def relaxng_colors(view_type):
    if view_type == 'tree':
        with tools.file_open(os.path.join('base', 'rng', '%s_view.rng' % view_type)) as frng:
            relaxng_doc = etree.parse(frng)
            namespaces = relaxng_doc.getroot().nsmap
            tree_doc = relaxng_doc.xpath('//rng:element[@name="tree"]', namespaces=namespaces)[0]
            optional = etree.SubElement(
                tree_doc,
                "{http://relaxng.org/ns/structure/1.0}optional"
            )
            etree.SubElement(
                optional,
                "{http://relaxng.org/ns/structure/1.0}attribute",
                name="colors"
            )
            view_validation._relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
    else:
        orig_relaxng(view_type)


view_validation.relaxng = relaxng_colors
