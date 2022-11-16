# -*- coding: utf-8 -*-
# from odoo import http


# class DizitCrm(http.Controller):
#     @http.route('/dizit_crm/dizit_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dizit_crm/dizit_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dizit_crm.listing', {
#             'root': '/dizit_crm/dizit_crm',
#             'objects': http.request.env['dizit_crm.dizit_crm'].search([]),
#         })

#     @http.route('/dizit_crm/dizit_crm/objects/<model("dizit_crm.dizit_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dizit_crm.object', {
#             'object': obj
#         })
