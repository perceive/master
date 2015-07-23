# -*- encoding: utf-8 -*-
{
    'name': 'Sample Management Type',
    'version': '2.0',
    'author': 'Perceive ERP',
    'category': 'Sale Management',
    'description': """
    Sample Type Master for both inventory sample and non-inventory sample
    """,
    'depends': ['sale'],
    'data': [
        'sample_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
