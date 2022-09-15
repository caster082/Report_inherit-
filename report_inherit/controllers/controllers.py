# -*- coding: utf-8 -*-
# from odoo import http


# class ReportInherit(http.Controller):
#     @http.route('/report_inherit/report_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_inherit/report_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_inherit.listing', {
#             'root': '/report_inherit/report_inherit',
#             'objects': http.request.env['report_inherit.report_inherit'].search([]),
#         })

#     @http.route('/report_inherit/report_inherit/objects/<model("report_inherit.report_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_inherit.object', {
#             'object': obj
#         })
