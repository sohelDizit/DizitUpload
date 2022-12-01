# -*- coding: utf-8 -*-
# from odoo import http


# class SupplyChainManagement(http.Controller):
#     @http.route('/supply_chain_management/supply_chain_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/supply_chain_management/supply_chain_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('supply_chain_management.listing', {
#             'root': '/supply_chain_management/supply_chain_management',
#             'objects': http.request.env['supply_chain_management.supply_chain_management'].search([]),
#         })

#     @http.route('/supply_chain_management/supply_chain_management/objects/<model("supply_chain_management.supply_chain_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('supply_chain_management.object', {
#             'object': obj
#         })
