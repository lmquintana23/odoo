# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'ESTATE PROPERTY OFFER Model'
    
    price = fields.Float(string = "Price")
    status = fields.Selection(
        string = 'Status',
        selection = [('Accepted','Accepted'),('Refused','Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner',copy=False, index=True, required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    
    
    
   
