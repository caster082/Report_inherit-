# -*- coding: utf-8 -*-
#import of odoo
from odoo import api, fields, models
from odoo.tools.misc import get_lang

class AccountTaxReport(models.TransientModel):
    _name = 'gst.detail.account.tax.reports1'
    _description = 'Tax Report'



    #def _print_report(self, data):
        #return self.env.ref('report_inherit.action_gst_report_account_tax').report_action(self, data=data)

    fiscal_year_from = fields.Many2one("account.fiscal.year", String="Fiscal Year From", ondelete="set null" )
    fiscal_year_to = fields.Many2one("account.fiscal.year", String="Fiscal Year To", ondelete="set null")
    period_from = fields.Selection([
        ('all', 'All'),
        ('p1', 'Quarter1'),
        ('p2', 'Quarter2'),
        ('p3', 'Quarter3'),
        ('p4', 'Quarter4'),

    ], String='Period From', default='all')

    period_to = fields.Selection([
        ('all', 'All'),
        ('p1', 'Quarter1'),
        ('p2', 'Quarter2'),
        ('p3', 'Quarter3'),
        ('p4', 'Quarter4'),

    ], String='Period To', default='all')

    tax_type = fields.Selection([
        ('sale', 'Output Tax'),
        ('purchase', 'Input Tax'),

    ], String='Tax Type', default='sale')

    date_from = fields.Date(string="From", compute="_compute_date_from")
    date_to = fields.Date(string="To", compute="_compute_date_to")

    @api.depends('fiscal_year_from', 'period_from')
    def _compute_date_from(self):
        for record in self:
            period = self.env['account.fiscalyear.periods'].search(
                [('fiscal_year_id', '=', record.fiscal_year_from.id)])
            if record.period_from == "all" or record.period_from == "p1":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 1)])
                record.date_from = fiscal_period_month['date_start']

            if record.period_from == "p2":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 4)])
                record.date_from = fiscal_period_month['date_start']

            if record.period_from == "p3":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 7)])
                record.date_from = fiscal_period_month['date_start']

            if record.period_from == "p4":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 10)])
                record.date_from = fiscal_period_month['date_start']

    @api.depends('fiscal_year_to', 'period_to')
    def _compute_date_to(self):
        for record in self:
            period = self.env['account.fiscalyear.periods'].search(
                [('fiscal_year_id', '=', record.fiscal_year_from.id)])
            if record.period_to == "all" or record.period_to == "p4":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 12)])
                record.date_to = fiscal_period_month['date_stop']

            if record.period_to == "p1":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 3)])
                record.date_to = fiscal_period_month['date_stop']

            if record.period_to == "p2":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 6)])
                record.date_to = fiscal_period_month['date_stop']

            if record.period_to == "p3":
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', period['id']), ('sequence', '=', 9)])
                record.date_to = fiscal_period_month['date_stop']



    def check_report(self):
        data= {'model' : 'gst.account.tax.reports', 'form'  : self.read(['fiscal_year_from', 'fiscal_year_to','period_from','period_to','tax_type'])[0], 'date_from' : 'none', 'date_to': 'none','tax_type' : 'none'}
        if data['form']['fiscal_year_from']:
            fiscal_from = self.env['account.fiscal.year'].search(
                [('id', '=', data['form']['fiscal_year_from'][0])])
            data['form']['date_from'] = fiscal_from['date_from']
        if data['form']['fiscal_year_to']:
            fiscal_from = self.env['account.fiscal.year'].search(
                [('id', '=', data['form']['fiscal_year_to'][0])])
            data['form']['date_to'] = fiscal_from['date_to']
        if data['form']['period_from']:
            fiscal_period = self.env['account.fiscalyear.periods'].search(
                [('fiscal_year_id', '=', data['form']['fiscal_year_to'][0])])
            if data['form']['period_from'] == 'all' or data['form']['period_from'] == 'p1':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&',('fiscalyear_id', '=', fiscal_period['id']),('sequence', '=', 1)])
                data['form']['date_from'] = fiscal_period_month['date_start']
            if data['form']['period_from'] == 'p2':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', fiscal_period['id']), ('sequence', '=', 4)])
                data['form']['date_from'] = fiscal_period_month['date_start']
            if data['form']['period_from'] == 'p3':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', fiscal_period['id']), ('sequence', '=', 7)])
                data['form']['date_from'] = fiscal_period_month['date_start']
            if data['form']['period_from'] == 'p4':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', fiscal_period['id']), ('sequence', '=', 10)])
                data['form']['date_from'] = fiscal_period_month['date_start']

        if data['form']['period_to']:
            fiscal_period = self.env['account.fiscalyear.periods'].search(
                [('fiscal_year_id', '=', data['form']['fiscal_year_to'][0])])
            if data['form']['period_to'] == 'all' or data['form']['period_to'] == 'p4':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', fiscal_period['id']), ('sequence', '=', 12)])
                data['form']['date_to'] = fiscal_period_month['date_stop']
            if data['form']['period_to'] == 'p1':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', fiscal_period['id']), ('sequence', '=', 3)])
                data['form']['date_to'] = fiscal_period_month['date_stop']
            if data['form']['period_to'] == 'p2':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', fiscal_period['id']), ('sequence', '=',6 )])
                data['form']['date_to'] = fiscal_period_month['date_stop']
            if data['form']['period_to'] == 'p3':
                fiscal_period_month = self.env['account.month.period'].search(
                    ['&', ('fiscalyear_id', '=', fiscal_period['id']), ('sequence', '=', 9)])
                data['form']['date_to'] = fiscal_period_month['date_stop']


        return self.env.ref('report_inherit.action_gst_detail_report1_account_tax').with_context(landscape=True).report_action(
            self, data=data)



