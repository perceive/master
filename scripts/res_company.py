#!/usr/bin/env python
# coding: utf-8

import xmlrpclib
import xlrd

dbname = 'testdb'
username = 'admin'
pwd = 'a'
sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
uid = sock_common.login(dbname, username, pwd)

workbook = xlrd.open_workbook('/home/nimesh/workspace/scripts/Customer_simlx.xls')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1

user_id = 0
country_id = 0
state_id = 0
partner_id = 0

active_res_partner = {}
res_partner = {}

print "Importing companies..."
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)

    state_id = sock.execute(dbname, uid, pwd, 'res.country.state', 'search', [('code', '=', row[13].value)])
    if state_id:
        state_id = state_id[0]
        
    country_id = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('name', '=', row[15].value)])
    if country_id:
        country_id = country_id[0]

    new_user_id = sock.execute(dbname, uid, pwd, 'res.users', 'search', [('name', '=', row[19].value)])
    # if not new_user_id:
    #     res_user_vals = {'login': row[19].value, 'name': row[19].value}
    #     new_user_id = sock.execute(dbname, uid, pwd, 'res.users', 'create', res_user_vals)

    #partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('name', '=', row[2].value)])
    sales_team_id = sock.execute(dbname, uid, pwd, 'crm.case.section', 'search', [('name', '=', row[20].value)])
    if not sales_team_id:
        new_sales_team_id = sock.execute(dbname, uid, pwd, 'crm.case.section', 'create', {'name': row[20].value})
        sales_team_id = [new_sales_team_id]

    if row[0].value:
        active_company_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('ref', '=', row[0].value)])
        if not active_company_id:
            active_res_partner = {
                'is_company': True,
                'ref': row[0].value,
                'name':row[2].value,
                'phone': row[4].value,
                'fax': row[5].value,
                'email':row[8].value,
                'street': row[9].value,
                'street2': row[10].value,
                'city':row[12].value,
                'state_id':state_id,
                'zip':row[14].value,
                'country_id':country_id,
                # 'user_id': new_user_id,
                'customer': True,
                'note': row[17].value,
                'section_id': sales_team_id and sales_team_id[0] or False
            }
            partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', active_res_partner)
        else:
            active_res_partner.update({
                'name':row[3].value,
                'type': 'contact',
                'parent_id': active_company_id and active_company_id[0] or False
            })
            partner = sock.execute(dbname, uid, pwd, 'res.partner', 'create', active_res_partner)
    else:
        name_company_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search', [('name', '=', row[2].value)])
        if not name_company_id:
            res_partner = {
                    'is_company': True,
                    'ref': row[0].value,
                    'name':row[2].value,
                    'phone': row[4].value,
                    'fax': row[5].value,
                    'email':row[8].value,
                    'street': row[9].value,
                    'street2': row[10].value,
                    'city':row[12].value,
                    'state_id':state_id,
                    'zip':row[14].value,
                    'country_id':country_id,
                    # 'user_id': new_user_id,
                    'customer': False,
                    'note': row[17].value,
                    'section_id': sales_team_id and sales_team_id[0] or False
                    }
            partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', res_partner)
        else:
            res_partner.update({
                'name':row[3].value,
                'type': 'contact',
                'parent_id': name_company_id and name_company_id[0] or False
            })
            partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create', res_partner)

print "Companies uploaded Successfully...!"
