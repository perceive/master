# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools import html2plaintext
from openerp import tools
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
import pytz
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp import netsvc

class crm_phonecall(osv.osv):
    """ Model for CRM phonecalls """
    _inherit = "crm.phonecall"
    _columns = {
        'reminder_date': fields.datetime('Follow Up', help="Follow up data should be greater then current date."),
        'alarm_id': fields.many2one('calendar.alarm', 'Reminder', help="Set an alarm at this time, before TODO call occurs" ),
    }
    def scheduler_manage_activity(self, cr, uid, domain=[], model_name=False, context=None):
        #This method is called by a cron task
        if context is None:
            context = {}
        time_now = (fields.datetime.context_timestamp(cr, uid, datetime.now(), context=context).strftime('%H:%M'))
        time_now2 = (fields.datetime.context_timestamp(cr, uid, datetime.now(), context=context)).date()
        
        template_id = 'email_template_schedule_reminder'
        
        ids = self.search(cr, uid, domain, offset=0, limit=None, order=None, context=context, count=False)
        alarm_object = self.pool.get('calendar.alarm')
        default_time = "{0:0=2d}".format(23) + ':' + "{0:0=2d}".format(59) + ':' + "{0:0=2d}".format(59)
        user = self.pool.get('res.users').browse(cr, uid, uid)
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        for activity_id in self.browse(cr, uid, ids, context=context):
            if activity_id.alarm_id:
                alarm_data = alarm_object.read(cr, uid, activity_id.alarm_id.id, context=context)
                interval = alarm_data['interval']
                duration = alarm_data['duration']

                if interval == 'hours':
                    delta = timedelta(hours=duration)
                if interval == 'minutes':
                    delta = timedelta(minutes=duration)

                remind_vals = self.handle_timedelta(cr, uid, delta, context=context)
                reminder_time = "{0:0=2d}".format(abs(remind_vals['hours'])) + ':' + "{0:0=2d}".format(remind_vals['minutes']) + ':' + "{0:0=2d}".format(remind_vals['seconds'])
                time_diff = datetime.strptime(default_time, tools.DEFAULT_SERVER_TIME_FORMAT) - datetime.strptime(reminder_time, tools.DEFAULT_SERVER_TIME_FORMAT)
                scheduled_time = datetime.strptime(activity_id.reminder_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
                scheduled_time_date = (pytz.utc.localize(scheduled_time).astimezone(tz)).date()
                scheduled_time = pytz.utc.localize(scheduled_time).astimezone(tz)     # convert date in user's timezone
                scheduled_time = scheduled_time.strftime(tools.DEFAULT_SERVER_TIME_FORMAT)
                actual_reminder_time = datetime.strptime(str(scheduled_time), tools.DEFAULT_SERVER_TIME_FORMAT) - datetime.strptime(str(reminder_time), tools.DEFAULT_SERVER_TIME_FORMAT)
                actual_vals = self.handle_timedelta(cr, uid, actual_reminder_time, context=context)
                actual_time = "{0:0=2d}".format(abs(actual_vals['hours'])) + ':' + "{0:0=2d}".format(actual_vals['minutes'])
                
                if time_now2 == scheduled_time_date and actual_time == time_now:
                    self.do_mail(cr, uid, activity_id.id, template_id, context=context)

    def handle_timedelta(self, cr, uid, datetime_val, context=None):
        if context is None:
            context = {}
        if datetime_val:
            vals = {}
            vals['seconds'] = datetime_val.seconds
            vals['hours'] = vals['seconds'] // 3600
            vals['minutes'] = vals['seconds'] % 3600 // 60
            vals['seconds'] = vals['seconds'] % 60
            return vals
        return False

    def do_mail(self, cr, uid, id, template, context=None):
        if context is None:
            context = {}
        activity_id = id
        email_template = self.pool.get('email.template')
        res_partner_obj = self.pool.get('res.partner')
        ir_model_data = self.pool.get('ir.model.data')
        
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'crm', template)[1]
        except ValueError:
            template_id = False
        
        for leads in self.browse(cr, uid, activity_id, context=context):
            leads_id = leads.user_id
            if leads_id:
                email_to = leads_id.email
                
                email_template.write(cr, uid, template_id, {'email_to': email_to, 'reply_to': email_to, 'auto_delete': False}, context=context)
                email_template.send_mail(cr, uid, template_id, leads.id, force_send=True)
#                self.write(cr, uid, sample.id, {'is_notify': True}, context=context)
        return True
    
    def run_scheduler(self, cr, uid, context=None):
        date_today = datetime.strptime(fields.date.context_today(self, cr, uid, context=context), tools.DEFAULT_SERVER_DATE_FORMAT)
        limit_date = (date_today + relativedelta(days=+15)).strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
        domain = [('reminder_date', '<', limit_date)]
        self.scheduler_manage_activity(cr, uid, domain=domain,context=context)
        return True
    
class crm_lead(osv.Model):
    _inherit = "crm.lead"
    _columns = {
        'reminder_date': fields.datetime('Follow Up', help="Follow up data should be greater then current date."),
        'alarm_id': fields.many2one('calendar.alarm', 'Reminder', help="Set an alarm at this time, before TODO call occurs" ),
    }
    def scheduler_manage_activity(self, cr, uid, domain=[], model_name=False, context=None):
        #This method is called by a cron task
        if context is None:
            context = {}
        time_now = (fields.datetime.context_timestamp(cr, uid, datetime.now(), context=context).strftime('%H:%M'))
        time_now2 = (fields.datetime.context_timestamp(cr, uid, datetime.now(), context=context)).date()
        
        template_id = 'email_template_lead_reminder'
        
        ids = self.search(cr, uid, domain, offset=0, limit=None, order=None, context=context, count=False)
        alarm_object = self.pool.get('calendar.alarm')
        default_time = "{0:0=2d}".format(23) + ':' + "{0:0=2d}".format(59) + ':' + "{0:0=2d}".format(59)
        user = self.pool.get('res.users').browse(cr, uid, uid)
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        for activity_id in self.browse(cr, uid, ids, context=context):
            if activity_id.alarm_id:
                alarm_data = alarm_object.read(cr, uid, activity_id.alarm_id.id, context=context)
                interval = alarm_data['interval']
                duration = alarm_data['duration']

                if interval == 'hours':
                    delta = timedelta(hours=duration)
                if interval == 'minutes':
                    delta = timedelta(minutes=duration)

                remind_vals = self.handle_timedelta(cr, uid, delta, context=context)
                reminder_time = "{0:0=2d}".format(abs(remind_vals['hours'])) + ':' + "{0:0=2d}".format(remind_vals['minutes']) + ':' + "{0:0=2d}".format(remind_vals['seconds'])
                time_diff = datetime.strptime(default_time, tools.DEFAULT_SERVER_TIME_FORMAT) - datetime.strptime(reminder_time, tools.DEFAULT_SERVER_TIME_FORMAT)
                scheduled_time = datetime.strptime(activity_id.reminder_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
                scheduled_time_date = (pytz.utc.localize(scheduled_time).astimezone(tz)).date()
                scheduled_time = pytz.utc.localize(scheduled_time).astimezone(tz)     # convert date in user's timezone
                scheduled_time = scheduled_time.strftime(tools.DEFAULT_SERVER_TIME_FORMAT)
                actual_reminder_time = datetime.strptime(str(scheduled_time), tools.DEFAULT_SERVER_TIME_FORMAT) - datetime.strptime(str(reminder_time), tools.DEFAULT_SERVER_TIME_FORMAT)
                actual_vals = self.handle_timedelta(cr, uid, actual_reminder_time, context=context)
                actual_time = "{0:0=2d}".format(abs(actual_vals['hours'])) + ':' + "{0:0=2d}".format(actual_vals['minutes'])
                
                if time_now2 == scheduled_time_date and actual_time == time_now:
                    self.do_mail(cr, uid, activity_id.id, template_id, context=context)

    def handle_timedelta(self, cr, uid, datetime_val, context=None):
        if context is None:
            context = {}
        if datetime_val:
            vals = {}
            vals['seconds'] = datetime_val.seconds
            vals['hours'] = vals['seconds'] // 3600
            vals['minutes'] = vals['seconds'] % 3600 // 60
            vals['seconds'] = vals['seconds'] % 60
            return vals
        return False

    def do_mail(self, cr, uid, id, template, context=None):
        if context is None:
            context = {}
        activity_id = id
        email_template = self.pool.get('email.template')
        res_partner_obj = self.pool.get('res.partner')
        ir_model_data = self.pool.get('ir.model.data')
        
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'crm', template)[1]
        except ValueError:
            template_id = False
        
        for leads in self.browse(cr, uid, activity_id, context=context):
            leads_id = leads.user_id
            if leads_id:
                email_to = leads_id.email
                
                email_template.write(cr, uid, template_id, {'email_to': email_to, 'reply_to': email_to, 'auto_delete': False}, context=context)
                email_template.send_mail(cr, uid, template_id, leads.id, force_send=True)
#                self.write(cr, uid, sample.id, {'is_notify': True}, context=context)
        return True
    
    def run_scheduler(self, cr, uid, context=None):
        date_today = datetime.strptime(fields.date.context_today(self, cr, uid, context=context), tools.DEFAULT_SERVER_DATE_FORMAT)
        limit_date = (date_today + relativedelta(days=+15)).strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
#        domain = ['&', ('is_notify', '=', False), ('follow_up', '<', limit_date)]
        domain = [('reminder_date', '<', limit_date)]
        self.scheduler_manage_activity(cr, uid, domain=domain,context=context)
        return True


class res_partner(osv.Model):
    """ Model for Calendar Event """
    _inherit = 'res.partner'
    
    def message_post(self, cr, uid, thread_id, body='', subject=None, type='notification',
                     subtype=None, parent_id=False, attachments=None, context=None,
                     content_subtype='html', **kwargs):
        message_obj = self.pool.get('mail.message')
        res_partner_obj = self.pool.get('res.partner')
        values = {}
        if context is None:
            context = {}
        res = super(res_partner, self).message_post(cr, uid, thread_id, body=body, subject=subject, type=type, subtype=subtype, parent_id=parent_id, \
            attachments=attachments, context=context, content_subtype=content_subtype, **kwargs)
        if res:
            data = message_obj.browse(cr, uid, res, context=context)
            partner_data = self.browse(cr, uid, thread_id)
            if partner_data.is_company == False :
                values.update({
                    'model': 'res.partner',
                    'res_id': partner_data.parent_id.id,
                    'body' : data.body,
                    'parent_id': False,
                    'author_id': data.author_id.id
                })
                if values:
                    message_obj.create(cr, SUPERUSER_ID, values=values, context=context)
        return res
        