# -*- coding: utf-8 -*-
                       
from odoo import models, fields, api
import datetime



class scm(models.Model):
    _name = 'scm.scm'
    _description = 'scm.scm'

    name = fields.Char(required=True)
    capacity = fields.Float(store=True)
    short_name = fields.Char(required=True,string="Short Name")
    product_id = fields.Many2one("scm.supply_chain_product", string="Product")
    description = fields.Text(string="Address")



class supply_chain_delivery_point(models.Model):
    _name = 'scm.supply_chain_delivery_point'
    _description = 'scm.supply_chain_delivery_point'

    name = fields.Char(required=True)
    capacity = fields.Float(store=True,string="Capacity(Ton)")
    description = fields.Text()

class supply_chain_transport(models.Model):
    _name = 'scm.supply_chain_transport'
    _description = 'scm.supply_chain_transport'

    name = fields.Char(required=True,string="Car Name")
    CarOwnerName = fields.Char(string="Owner Name")
    PhoneNumber = fields.Char(required=True,string="Phone Number")
    CarDetails = fields.Text(string="Car Details")




class supply_chain_TCB_supply(models.Model):
    _name = 'scm.tcb_supply'
    _description = 'scm.tcb_supply'

    name = fields.Char(required=True,string="Name")
    Terget = fields.Float(store=True)
    Supplies = fields.Many2many("scm.supply_delivery", string="Supplies")
    received_ratio = fields.Integer(compute="_received_ratio_compute", string='Received Ratio')
    notShipped = fields.Integer(compute="_received_ratio_compute", string='Not Shipped')
    shipped = fields.Integer(compute="_received_ratio_compute", string='Shipped')

    def _received_ratio_compute(self):
        self.received_ratio=0
        self.shipped=0
        self.notShipped=0
        for sup  in self.Supplies:
            self.received_ratio=self.received_ratio+sup.Quantity
            if sup.EndingTime:
                self.shipped=self.shipped+sup.Quantity
            else:
                self.notShipped=self.notShipped+sup.Quantity

    @api.model_create_multi
    def create(self, vals_list):
        chain= super(supply_chain_TCB_supply, self).create(vals_list)
        for slp in chain.Supplies:
            slp.write({'parent_id': chain.id})
        return chain

    def write(self, vals):        
        id=self.id
        ret= super(supply_chain_TCB_supply, self).write(vals)
        for slp in self.Supplies:
            account_ids = self.env['scm.supply_delivery'].search([('id', '=', int(slp))])
            account_ids.write({'parent_id': id})
        return ret

    
class supply_chain_delivery(models.Model):
    _name = 'scm.supply_delivery'
    _description = 'scm.supply_delivery'

    name = fields.Char(required=True,string="Name")                                                                                                                
    Source = fields.Many2one("scm.scm", string="Source")
    Destination = fields.Many2one("scm.supply_chain_delivery_point", string="Destination")
    Car = fields.Many2one("scm.supply_chain_transport", string="Car")
    Quantity = fields.Float(store=True)
    Beg = fields.Float(store=True)
    Date = fields.Date(string='Date')
    StartingTime= fields.Datetime(string="Starting Time")
    EndingTime= fields.Datetime(string="Ending Time")
    Description = fields.Text()
    parent_id= fields.Many2one("scm.tcb_supply",required=False,string="Parent")
    EndingTimeCompute = fields.Datetime(compute="_compute_field", string='Ending Date')
    color = fields.Integer(compute="_compute_field",string="color")    

    def _compute_field(self):
        for record in self:
            record.color='3'
            if record.EndingTime:
                record.EndingTimeCompute = record.EndingTime
                record.color='3'
            else:
                # record.EndingTimeCompute=record.StartingTime
                record.EndingTimeCompute=datetime.datetime.today().date()
                record.color='0'


class supply_chain_upazila(models.Model):
    _name = 'scm.supply_chain_upazila'
    _description = 'scm.supply_chain_upazila'
    name = fields.Char(required=True)
    district_id = fields.Many2one("scm.supply_chain_district", string="District")

class supply_chain_district(models.Model):
    _name = 'scm.supply_chain_district'
    _description = 'scm.supply_chain_district'
    name = fields.Char(required=True)

class supply_chain_product(models.Model):
    _name = 'scm.supply_chain_product'
    _description = 'scm.supply_chain_product'
    name = fields.Char(required=True)
    image = fields.Binary(string="Image")


class supply_chain_representation(models.Model):
    _name = 'scm.supply_representation'
    _description = 'scm.representation'
    name = fields.Char(required=True)
    Date = fields.Date(string='Forecasting Date')
    quantity = fields.Float(store=True)
    transport_req = fields.Float(store=True,string='Transport Request')
    Source = fields.Many2one("scm.scm", string="Source",required=True)
    car_tracing = fields.Many2many("scm.representation_history", string="History")
    rep_hist = fields.Many2many("scm.representative_destination", string="destination History")

    @api.model_create_multi
    def create(self, vals_list):
        chain= super(supply_chain_representation, self).create(vals_list)
        for slp in chain.car_tracing:
            slp.write({'representation_id': chain.id,'Source':chain.Source})
        return chain

    def write(self, vals):        
        id=self.id
        ret= super(supply_chain_representation, self).write(vals)
        for slp in self.car_tracing:
            slp.write({'representation_id': id,'Source':self.Source})
        return ret




class representation_history(models.Model):
    _name = 'scm.representation_history'
    _description = 'scm.representation_history'
    name = fields.Char(required=True)
    Car = fields.Many2one("scm.supply_chain_transport", string="Car",required=True)
    challan_of_supply = fields.Boolean('Challan of Supply')
    challan_of_track = fields.Boolean('Challan of Track')
    payment = fields.Boolean('Payment')
    reason = fields.Text("Reason")
    Source = fields.Many2one("scm.scm", string="Source")
    Destination = fields.Many2one("scm.supply_chain_delivery_point", string="Destination",required=True)
    status= fields.Selection([
        ('Rent', 'Rent'),
        ('Move', 'Move'), 
        ('Reached', 'Reached'),
        ('Unloading', 'Unloading'), 
        ('Complete', 'Complete'),
        ('Return', 'Return')],default='0')
    parent_id= fields.Many2one("scm.representation_history", string="Parent")
    representation_id=fields.Many2one("scm.supply_representation", string="Representation")
    Date = fields.Datetime(string='Date')


class representative_destination(models.Model):
    _name = 'scm.representative_destination'
    _description = 'scm.representative_destination'
    Source = fields.Many2one("scm.scm", string="Source")
    number_of_car=fields.Integer()
    #representation_id=fields.Many2one("scm.supply_representation", string="Representation")





    #@api.model_create_multi
    #def create(self, vals_list):
    #    print("from create")
    #    for vals in vals_list:
    #        print(dir(vals))
    #        print("==========================================================")
    #        print(dir(self))
    #        print(vals["Name"])
    #        parent_id = self._context.get('parent_id')
    #        parent_model = self.env.context.get('parent_model')     
    #        print("==========================================================")
    #        print(parent_model)
    #        print(parent_id)
    #    return super(supply_chain_delivery, self).create(vals_list)

    #def write(self, vals):        
    #    print("from write")
    #    return super(supply_chain_TCB_supply, self).write(vals)

class SupplyChainDeliveryReport(models.AbstractModel):
    _name = 'report.scm.supply_chain_delivery_report'
     
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env[model.model].browse(docids)
        return {
              'doc_ids': docids,
              'doc_model': model.model,
              'docs': docs,
              'data': data,
        }       