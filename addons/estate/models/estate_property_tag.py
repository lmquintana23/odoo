# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'ESTATE PROPERTY TAG Model'
    
    name = fields.Char(required=True)
    
    
   
