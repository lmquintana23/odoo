# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'summary': """
        First app in tutorial
    """,

    'description': """
        First App
    """,

    'author': "Leo Quintana",
    'category': 'Tutorials/Estate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'contacts'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_menus.xml',
        'views/estate_property_tree_view.xml',
        'views/estate_property_form.xml',
        'views/estate_property_search.xml',
        'views/estate_property_type_tree_view.xml',
        'views/estate_property_type_form.xml',
        'views/estate_property_type_search.xml',
        'views/estate_property_tag_tree_view.xml',
        'views/estate_property_tag_form.xml',
        'views/estate_property_tag_search.xml',
        'views/estate_property_offer_tree_view.xml',
        'views/estate_property_offer_form.xml',
        'views/estate_property_offer_search.xml',
        ],
    'license': 'AGPL-3'
}
