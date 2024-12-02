# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'ESTATE PROPERTY Model'
    
    AVAILABILITY = datetime.now() + relativedelta(months=3)
    
    
    name = fields.Char(string="Title", size=40, required=True, default="Unknow")
    description = fields.Text(string="Description", default="Give a description")
    postcode = fields.Char(size=10)
    date_availability = fields.Date(string="Available From", default=AVAILABILITY, copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) 
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(string="Total Area (sqm)",compute="_total_area_compute")
    facades = fields.Integer()    
    garage = fields.Boolean()
    garden = fields.Boolean()
    
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('North','North'),('South','South'),('East','East'),('West','West')],
        help = "Where the garden is faced."
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string = 'State',
        selection = [('New','New'),('Offer Received','Offer Received'),('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Cancelled','Cancelled')],
        default="New",
        copy=False,
        required=True
    )
    type_id = fields.Many2one(string="Property type", comodel_name='estate.property.type')
    tag_ids = fields.Many2many(string="Property tags", comodel_name='estate.property.tag')
    #offer_ids = fields.Many2one(string="Property offers", comodel_name='estate.property.offer')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Property offers")
    best_price = fields.Integer(string="Best Offer",compute="_best_offer")
    buyer = fields.Many2one('res.partner', string='Buyer',copy=False, index=True)
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    
    @api.depends("living_area","garden_area")
    def _total_area_compute(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    #@api.depends("living_area","garden_area")
    def _best_offer(self):
        if self.offer_ids:
            self.best_price = max(self.offer_ids.mapped("price"))
            
        
   
