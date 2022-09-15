# -*- coding: utf-8 -*-
#import of odoo
from odoo import api, models, _
from odoo.exceptions import UserError


class GSTDetailReportTax(models.AbstractModel):
    _name = 'report.report_inherit.gst_detail_report_tax1'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {
            'data': data['form'],
            'lines': self.get_lines(data.get('form')),
        }

    def _sql_from_amls_one(self):
        sql = """SELECT "account_move_line".tax_line_id, COALESCE(("account_move_line".debit-"account_move_line".credit), 0), "account_move_line".move_id
                    FROM %s
                    WHERE %s"""
        return sql

    def _sql_from_amls_two(self):
        sql = """SELECT r.account_tax_id, COALESCE(("account_move_line".debit-"account_move_line".credit), 0), "account_move_line".move_id
                 FROM %s
                 INNER JOIN account_move_line_account_tax_rel r ON ("account_move_line".id = r.account_move_line_id)
                 INNER JOIN account_tax t ON (r.account_tax_id = t.id)
                 WHERE %s"""
        return sql

    def _sql_from_amls_three(self):
        sql = """SELECT m.date, j.name, m.name, t.id, t.name, t.type_tax_use, m.amount_total_signed, m.amount_tax_signed, "account_move_line".move_id
                    FROM %s
                    INNER JOIN account_move m ON (m.id = "account_move_line".move_id)
                    INNER JOIN account_journal j ON (j.id = m.journal_id)
                    INNER JOIN account_move_line_account_tax_rel r ON ("account_move_line".id = r.account_move_line_id)
                    INNER JOIN account_tax t ON (r.account_tax_id = t.id)
                    WHERE %s"""
        return sql

    def _compute_from_amls(self, options, taxes):
        moves = {}
        i=0
        #get the move
        sql = self._sql_from_amls_three()
        tables, where_clause, where_params = self.env['account.move.line']._query_get()
        query = sql % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for result in results:
            moves[i] = {'date': result[0], 'journal': result[1], 'entry': result [2], 'tax': 0, 'net': 0, 'name': result[4], 'type': result[5], 'move_id' : result[8], 't_id': result[3]}
            i = i+1

        # compute the tax amount
        sql2 = self._sql_from_amls_one()
        query = sql2 % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for move in moves.values():
            for result in results:
                if str(move['move_id']) == str(result[2]) and str(move['t_id']) == str(result[0]):
                    move['tax'] += result[1]

        # compute the net amount
        sql3 = self._sql_from_amls_two()
        query = sql3 % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for move in moves.values():
            for result in results:
                if str(move['move_id']) == str(result[2]) and str(move['t_id']) == str(result[0]):
                    move['net'] += result[1]

        res = {}

        for key, value in moves.items():
            if value not in res.values():
                res[key] = value
        for result in res.values():
            if result['t_id'] in taxes:
                taxes[result['t_id']]['line'].append(result)



    @api.model
    def get_lines(self, options):
        taxes = {}
        input = {}
        output = {}
        input_total = {}
        output_total = {}

        for tax in self.env['account.tax'].search([('type_tax_use', '!=', 'none')]):
            if tax.children_tax_ids:
                for child in tax.children_tax_ids:
                    #taxes[child.id] = {'date': 'none', 'journal':'none', 'entry':'none', 'tax': 0, 'net': 0, 'name': child.name, 'type': tax.type_tax_use}
                    taxes[child.id] = {'line' :  [] }

            else:
                #taxes[tax.id]['line'] = {'date': 'none', 'journal':'none', 'entry':'none', 'tax': 0, 'net': 0, 'name': tax.name, 'type': tax.type_tax_use}
                taxes[tax.id] = {'line' : [] }
        self.with_context(date_from=options['date_from'], date_to=options['date_to'],state='posted', strict_range=True)._compute_from_amls(options, taxes)
        groups = dict((tp, []) for tp in ['sale', 'purchase', 'sale_tax', 'purchase_tax'])
        for tax in taxes.values():
            for journal_item in tax['line']:
                if journal_item['type'] == options['tax_type']:
                    groups[journal_item['type']].append(journal_item)

        sale_tax = self.env['account.tax'].search([('type_tax_use', '=', 'sale')])
        purchase_tax = self.env['account.tax'].search([('type_tax_use', '=', 'purchase')])
        for tax in sale_tax:
            val = {
                "id": tax.id,
                "name": tax.name,

            }
            groups['sale_tax'].append(val)

        for tax in purchase_tax:
            val = {
                "id": tax.id,
                "name": tax.name,

            }
            groups['purchase_tax'].append(val)

        return groups
