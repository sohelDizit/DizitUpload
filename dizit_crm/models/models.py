# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class Person(models.Model):
    _name = 'dizit_crm.person'
    _description = 'dizit_crm.person'

    name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date(string='D.O.B')
    weight = fields.Float()
    blood_type= fields.Selection(
        string='Blood Type',
        selection=[('1', 'A+'), ('2', 'A-'),
                   ('3', 'B+'), ('4', 'B-'),
                   ('5', 'O+'), ('6', 'O-'),
                   ('7', 'AB+'), ('8', 'AB-')])
    email = fields.Char()
    #height_type= fields.Integer()
    height_feet= fields.Float()
    height_inches= fields.Float()
    gender=fields.Selection(
        string='Gender',
        selection=[('1', 'Male'), ('2', 'Female'),
                   ('3', 'Other')],required=True)
    #user_level=fields.Integer()

    village_or_house=fields.Char()
    police_station = fields.Many2one("dizit_crm.police_station", string="Police Station")
    district = fields.Many2one("dizit_crm.district", string="District")
    division = fields.Many2one("dizit_crm.division", string="Division")
    category = fields.Many2one("dizit_crm.customercategory", string="Customer Category")

    contacts= fields.Char(required=True)
    emmergency_contacts=fields.Char()
    emmergency_contacts_name=fields.Char()
    emmergency_contacts_relation=fields.Char()

    image = fields.Binary("Image", attachment=True,)
    insurance_company = fields.Many2one("dizit_crm.insurance", string="Insurance")
    insurance_number= fields.Char()
    insurance_scheme= fields.Char()
    status= fields.Selection(
        string='Gender',
        selection=[('1', 'Prospective'), ('2', 'New'),
                   ('3', 'Registered')])

    cid= fields.Char(string="Customer ID")
    ticket_ids = fields.Many2many("dizit_crm.ticketing", string="Tickets")
    history_ids = fields.Many2many("dizit_crm.patient_history", string="History")
    appointment_ids = fields.Many2many("dizit_crm.appointment", string="Appointment")

    @api.model_create_multi
    def create(self, vals_list):
        person= super(Person, self).create(vals_list)
        for appo in person.appointment_ids:
            appo.write({'parent_id': person.id})

        for tkt in person.ticket_ids:
            tkt.write({'parent_id': person.id})

        return person

    def write(self, vals):        
        id=self.id
        person= super(Person, self).write(vals)
        for appo in self.appointment_ids:
            appo.write({'parent_id': self.id})

        for tkt in self.ticket_ids:
            tkt.write({'parent_id': self.id})    

        return person








class PoliceStation(models.Model):
    _name = 'dizit_crm.police_station'
    _description = 'dizit_crm.police_station'

    name=fields.Char(required=True)
    description = fields.Text()

class District(models.Model):
    _name = 'dizit_crm.district'
    _description = 'dizit_crm.district'
    name=fields.Char(required=True)
    description = fields.Text()

class Division(models.Model):
    _name = 'dizit_crm.division'
    _description = 'dizit_crm.division'
    name=fields.Char(required=True)
    description = fields.Text()

class Insurance(models.Model):
    _name = 'dizit_crm.insurance'
    _description = 'dizit_crm.insurance'
    name=fields.Char(required=True)
    description = fields.Text()

class Ticketing(models.Model):
    _name = 'dizit_crm.ticketing'
    _description = 'dizit_crm.ticketing'
    name=fields.Char(required=True,string='Subject')
    description = fields.Text()
    time = fields.Datetime(string="Starting ON",required=True)
    parent_id= fields.Many2one("dizit_crm.person", string="Person")
    parent_contact=fields.Char(compute="_get_parent_contact",string='Contact')
    parent_name= fields.Char(compute="_get_parent_contact",string='Name')

    def _get_parent_contact(self):
        for sup in self:
            if sup.parent_contact:
                sup.parent_contact=sup.parent_id.contacts
                sup.parent_name=sup.parent_id.name
                print(sup.parent_name)

class HistoryType(models.Model):
    _name = 'dizit_crm.history_type'
    _description = 'dizit_crm.history_type'
    name=fields.Char(required=True,string='Subject')    
    description = fields.Text()

class PatientHistory(models.Model):
    _name = 'dizit_crm.patient_history'
    _description = 'dizit_crm.patient_history'
    type = fields.Many2one("dizit_crm.history_type", string="Type")
    attachment = fields.Binary("Upload file")
    description = fields.Text()
    type_name= fields.Char(compute="_get_parent_info",string='Type Name')


    def _get_parent_info(self):        
        for sup in self:
            if sup.type:
                sup.type_name = sup.type.name
                   
class Department(models.Model):
    _name = 'dizit_crm.department'
    _description = 'dizit_crm.department'
    name=fields.Char(required=True)
    description = fields.Text()

class Doctor(models.Model):
    _name = 'dizit_crm.doctor'
    _description = 'dizit_crm.doctor'
    name=fields.Char(required=True)
    image = fields.Binary("Image", attachment=True,)
    department_ids = fields.Many2many("dizit_crm.department", string="Departments")
    description = fields.Text()


class Appointment(models.Model):
    _name = 'dizit_crm.appointment'
    _description = 'dizit_crm.appointment'
    name=fields.Char(required=True,string='Subject')
    department=fields.Many2one("dizit_crm.department",string='Department')
    doctor=fields.Many2one("dizit_crm.doctor",string='doctor')
    time = fields.Datetime(string="Starting ON",required=True)
    description = fields.Text()
    parent_id= fields.Many2one("dizit_crm.person", string="Person")
    parent_contact=fields.Char(compute="_get_parent_contact",string='Contact',search = '_search_by_contact')
    parent_name= fields.Char(compute="_get_parent_contact",string='Name')

    def _get_parent_contact(self):  
        print(self)    
        for sup in self:
            if sup.parent_id:
                sup.parent_contact=sup.parent_id.contacts
                sup.parent_name=sup.parent_id.name
                
    def _search_by_contact(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        ids =  self.env['dizit_crm.appointment'].search([('parent_id.contacts', operator, value)])
        return [('id', 'in' , ids.ids)]

class CustomerCategory(models.Model):
    _name = 'dizit_crm.customercategory'
    _description = 'dizit_crm.customercategory'
    name=fields.Char(required=True)
    description = fields.Text()

