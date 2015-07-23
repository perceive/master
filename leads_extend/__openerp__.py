
{
    'name': 'Leads Management',
    'version': '1.1',
    'category': 'Sales',
    'author': 'Perceive ERP',
    'sequence': 18,
    'summary': 'Leads Management',
    'depends': ['crm','calendar'],
    'description': """

    """,
    'data': [
        'leads_extend.xml',
        'leads_reminder_cron.xml',
        'reminder_email_template.xml',
        'crm_lead_hide.xml',
        'partner_view.xml',
        ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

