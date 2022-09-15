# -*- coding: utf-8 -*-

# from odoo import models, fields, api
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import datetime
from datetime import date

# class report_inherit(models.Model):
#     _name = 'report_inherit.report_inherit'
#     _description = 'report_inherit.report_inherit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
class TaxReport(models.Model):
    _name = 'financial.report.tax'
    _inherit = 'financial.report'
    tax = fields.Char(string="Tax")

