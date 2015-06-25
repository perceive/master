from openerp import models, fields, api, _
from openerp.exceptions import Warning

class test(models.Model):
    _inherit = "crm.lead"

    create_contact = fields.Boolean(string="Create Contact")

    @api.multi
    def create_contact_ext(self):
        partner_obj = self.env['res.partner']
        if self.partner_id:
            vals = {
                'name': self.contact_name,
                'user_id': self.user_id.id,
                'section_id': self.section_id.id or False,
                'parent_id': self.partner_id.id,
                'phone': self.phone,
                'mobile': self.mobile,
                'is_company': False,
                'customer': True,
                'type': 'contact'
                }
            part_id = partner_obj.create(vals)
        return {
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'res.partner',
            'res_id': part_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
