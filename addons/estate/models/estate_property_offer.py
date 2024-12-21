# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'ESTATE PROPERTY OFFER Model'
    
    price = fields.Float(string = "Price")
    status = fields.Selection(
        string = 'Status',
        selection = [('Pending','Pending'),('Accepted','Accepted'),('Refused','Refused')],
        default='Pending',
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner',copy=False, index=True, required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7) 
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The price for an offer should be over 0.')
    ]
    
    @api.depends('create_date', 'validity') 
    def _compute_date_deadline(self): 
        for record in self: 
            if record.create_date: 
                record.date_deadline = record.create_date + timedelta(days=record.validity) 
            else: 
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity) 
                
    def _inverse_date_deadline(self): 
        for record in self: 
            if record.create_date and record.date_deadline: 
                delta = record.date_deadline - record.create_date.date() 
                record.validity = delta.days 
            else: 
                record.validity = 7
                
    def accept_offer(self):
        self._refuse_all()
        for record in self:
            record.status = "Accepted"
            record.property_id.buyer = record.partner_id
    
    def refuse_offer(self):
        for record in self:
            record.status = "Refused"
            
    def _refuse_all(self): 
        all_offers = self.env['estate.property.offer'].search([]) 
        for offer in all_offers: 
            offer.status = "Refused"
    
   
