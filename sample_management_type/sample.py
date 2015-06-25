# -*- encoding: utf-8 -*-

from openerp import models, api, fields

class sample_type(models.Model):
    _name = 'sample.type'

    name = fields.Char(string='Leaves Behind')
    description = fields.Char(string='Description')
    active = fields.Boolean(string='Active', default=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: