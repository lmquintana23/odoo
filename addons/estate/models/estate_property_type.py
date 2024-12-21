# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'ESTATE PROPERTY TYPE Model'
    
    name = fields.Char(string="Property type", required=True)
    property_ids = fields.One2many('estate.property','type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Property offers")
    
    
   
