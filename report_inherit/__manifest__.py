# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'report_inherit',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Accounting Reports, Asset Management and Account Budget, Recurring Payments, '
               'Lock Dates, Fiscal Year For Odoo15 Community Edition, Accounting Dashboard, Financial Reports, '
               'Customer Follow up Management, Bank Statement Import, Odoo Budget',
    'description': 'Odoo 15 Financial Reports, Asset Management and '
                   'Account Budget, Financial Reports, Recurring Payments, '
                   'Customer Credit Limit, Bank Statement Import, Customer Follow Up Management,'
                   'Account Lock Date, Accounting Dashboard',
    'live_test_url': 'https://www.youtube.com/watch?v=6gB-05E5kNg',
    'sequence': '1',
    'website': 'https://www.odoomates.tech',
    'author': 'Casta, Myat Mon Cho',
    'maintainer': 'Casta, Myat Mon Cho',
    'license': 'LGPL-3',
    'support': 'khantsithuaung082@gmail.com',
    'depends': ['base','base_accounting_kit', 'account','skit_financial_form','skit_account_reports','account_fiscal_year_period',],

    'excludes': ['account_accountant'],
    'demo': [
        'demo/demo.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/account_report.xml',
        #'views/report_inherit.xml',
        'views/templates.xml',
        'wizard/account_report_tax_view.xml',
        'wizard/gst_account_report_tax_view.xml',
        'wizard/gst_detail_account_report_tax_view.xml',
        'views/report_tax.xml',
        'views/report_gst_tax.xml',
        'views/report_gst_detail_tax.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
}
