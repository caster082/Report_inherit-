# -*- coding: utf-8 -*-
#import of odoo
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTax(models.AbstractModel):
    _name = 'report.report_inherit.gst_report_tax'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {
            'data': data['form'],
            'lines': self.get_lines(data.get('form')),
        }

    def _sql_from_amls_one(self):
        sql = """SELECT "account_move_line".tax_line_id, COALESCE(SUM("account_move_line".debit-"account_move_line".credit), 0)
                    FROM %s
                    WHERE %s GROUP BY "account_move_line".tax_line_id"""
        return sql

    def _sql_from_amls_two(self):
        sql = """SELECT r.account_tax_id, COALESCE(SUM("account_move_line".debit-"account_move_line".credit), 0)
                 FROM %s
                 INNER JOIN account_move_line_account_tax_rel r ON ("account_move_line".id = r.account_move_line_id)
                 INNER JOIN account_tax t ON (r.account_tax_id = t.id)
                 WHERE %s GROUP BY r.account_tax_id"""
        return sql

    def _compute_from_amls(self, options, taxes):
        #compute the tax amount
        sql = self._sql_from_amls_two()
        tables, where_clause, where_params = self.env['account.move.line']._query_get()
        query = sql % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for result in results:
            if result[0] in taxes:
                taxes[result[0]]['net'] = result[1]

        #compute the net amount
        sql2 = self._sql_from_amls_one()
        query = sql2 % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for result in results:
            if result[0] in taxes:
                taxes[result[0]]['tax'] = result[1]

    @api.model
    def get_lines(self, options):
        taxes = {}
        gst_form={}
        gst_form[0] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'sale', 'description': 'Total Value of Zero Rated Supplies'}
        gst_form[1] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'sale', 'description': 'Total Value of Exempt Supplies'}
        gst_form[2] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'sale', 'description': 'Total value of Standard Rated Supplies', 'date_from' : 'none'}
        gst_form[3] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'purchase', 'description': 'Total Value of Tax purchasable'}
        gst_form[4] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'none','description': 'Total Value of (1) + (2) + (3)'}
        gst_form[5] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'none', 'description': 'Output tax due'}
        gst_form[6] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'none', 'description': 'Input tax and refund claimed'}
        gst_form[7] = {'tax': 0, 'net': 0, 'name': 'none', 'type': 'none', 'description': 'Net GST to be paid to IRAS'}
        for tax in self.env['account.tax'].search([('type_tax_use', '!=', 'none')]):
            if tax.children_tax_ids:
                for child in tax.children_tax_ids:
                    if (child.type_tax_use == 'sale' or child.type_tax_use == 'none') and ('Zero Rated' in child.name):
                        taxes[child.id] = {'tax': 0, 'net': 0, 'name': child.name, 'type': tax.type_tax_use, 'description' : 'Total Value of Zero Rated Supplies'}

                    if (child.type_tax_use == 'sale' or child.type_tax_use == 'none') and ('Exempt' in child.name):
                        taxes[child.id] = {'tax': 0, 'net': 0, 'name': child.name, 'type': tax.type_tax_use, 'description': 'Total Value of Exempt Supplies'}

                    if (child.type_tax_use == 'sale' or child.type_tax_use == 'none') and ('Zero Rated' not in child.name) and ('Exempt' not in child.name):
                        taxes[child.id] = {'tax': 0, 'net': 0, 'name': child.name, 'type': tax.type_tax_use, 'description': 'Total value of Standard Rated Supplies'}

                    if child.type_tax_use == 'purchase':
                        taxes[child.id] = {'tax': 0, 'net': 0, 'name': child.name, 'type': tax.type_tax_use,'description': 'Total value of Tax purchasable'}



            else:

                if (tax.type_tax_use == 'sale') and ('Zero Rated' in tax.name):
                    taxes[tax.id] = {'tax': 0, 'net': 0, 'name': tax.name, 'type': tax.type_tax_use,
                                       'description': 'Total Value of Zero Rated Supplies'}
                if (tax.type_tax_use == 'sale') and ('Exempt' in tax.name):
                    taxes[tax.id] = {'tax': 0, 'net': 0, 'name': tax.name, 'type': tax.type_tax_use,
                                       'description': 'Total Value of Exempt Supplies'}
                if (tax.type_tax_use == 'sale') and ('Zero Rated' not in tax.name) and ('Exempt' not in tax.name):
                    taxes[tax.id] = {'tax': 0, 'net': 0, 'name': tax.name, 'type': tax.type_tax_use,
                                       'description': 'Total value of Standard Rated Supplies'}
                if tax.type_tax_use == 'purchase':
                    taxes[tax.id] = {'tax': 0, 'net': 0, 'name': tax.name, 'type': tax.type_tax_use,
                                       'description': 'Total value of Tax purchasable'}


        self.with_context(date_from=options['date_from'], date_to=options['date_to'], state='posted', strict_range=True)._compute_from_amls(options, taxes)
        groups = dict((tp, []) for tp in ['sale', 'purchase', 'Total Value of Zero Rated Supplies', 'Total Value of Exempt Supplies', 'Total value of Standard Rated Supplies', 'Total value of Tax purchasable', 'Total Value of (1) + (2) + (3)', 'OTD', 'Input tax and refund claimed', 'Net GST to be paid to IRAS' ])
        for tax in taxes.values():
            groups[tax['type']].append(tax)

            if tax['description'] == 'Total Value of Zero Rated Supplies':
                gst_form[0]['tax'] += tax['tax'] #line 2 tax amount
                gst_form[0]['net'] += tax['net'] # line 2 total amount
                #gst_form[4]['net'] += gst_form[0]['net'] #line 4 total amount
                gst_form[5]['tax'] += tax['tax']  # line 6 total sales tax amount

            if tax['description'] == 'Total Value of Exempt Supplies':
                gst_form[1]['tax'] += tax['tax'] # line 3 tax amount
                gst_form[1]['net'] += tax['net'] # line 3 total amount
                #gst_form[4]['net'] += gst_form[1]['net']  # line 4 total amount
                gst_form[5]['tax'] += tax['tax']  # line 6 total sales tax amount

            if tax['description'] == 'Total value of Standard Rated Supplies':
                gst_form[2]['tax'] += tax['tax'] #line 1 tax amount
                gst_form[2]['net'] += tax['net'] #line 1 total amount
                gst_form[2]['date_from'] = options['date_from']
                #gst_form[4]['net'] += gst_form[2]['net']  # line 4 total amount
                gst_form[5]['tax'] += tax['tax'] # line 6 total sales tax amount

            if tax['description'] == 'Total value of Tax purchasable':
                gst_form[3]['tax'] += tax['tax'] #line 5 tax amount
                gst_form[3]['net'] += tax['net'] #line 5 total amount
                gst_form[6]['tax'] += tax['tax'] #line 7 total purchase tax amount
        gst_form[0]['net'] = (-1) * gst_form[0]['net']
        gst_form[1]['net'] = (-1) * gst_form[1]['net']
        gst_form[2]['net'] = (-1) * gst_form[2]['net']
        gst_form[5]['tax'] = (-1) * gst_form[5]['tax']
        gst_form[4]['net'] = gst_form[0]['net'] + gst_form[1]['net'] + gst_form[2]['net']
        gst_form[7]['tax'] = gst_form[5]['tax'] - gst_form[6]['tax']
        groups['Total Value of Zero Rated Supplies'].append(gst_form[0])
        groups['Total Value of Exempt Supplies'].append(gst_form[1])
        groups['Total value of Standard Rated Supplies'].append(gst_form[2])
        groups['Total value of Tax purchasable'].append(gst_form[3])
        groups['Total Value of (1) + (2) + (3)'].append(gst_form[4])
        groups['OTD'].append(gst_form[5])
        groups['Input tax and refund claimed'].append(gst_form[6])
        groups['Net GST to be paid to IRAS'].append(gst_form[7])

        return groups
