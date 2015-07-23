# -*- encoding: utf-8 -*-
{
    'name': 'Sample Management',
    'version': '2.0',
    'author': 'Perceive ERP',
    'category': 'Sale Management',
    'description': """
    To keep track the quantity of how many sample of which sample type is sent to customer.And what would be the follow up date for that.
    """,
    'depends': ['sample_management_type', 'calendar', 'web_m2x_options', 'purchase'],
    'data': [
        'sale_view.xml',
        'purchase_view.xml',
        'sale_sample_email_template.xml',
        'purchase_sample_email_template.xml',
        'sample_followup_cron.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
