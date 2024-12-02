# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'ESTATE PROPERTY TYPE Model'
    
    name = fields.Char(string="Property type", required=True)
    
    
   
