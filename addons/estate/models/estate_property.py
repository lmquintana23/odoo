# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo import api, fields, models, exceptions
import odoo.tools.float_utils as float_u 


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'ESTATE PROPERTY Model'
    
    AVAILABILITY = datetime.now() + relativedelta(months=3)
    
    
    name = fields.Char(string="Title", size=40, required=True, default="Unknow")
    description = fields.Text(string="Description", default="Give a description")
    postcode = fields.Char(size=10)
    date_availability = fields.Date(string="Available From", default=AVAILABILITY, copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False, compute="_selling_price_compute") 
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
        selection = [('New','New'),('Offer Received','Offer Received'),('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Canceled','Canceled')],
        default="New",
        copy=False,
        required=True
    )
    type_id = fields.Many2one(string="Property type", comodel_name='estate.property.type')
    tag_ids = fields.Many2many(string="Property tags", comodel_name='estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Property offers")
    best_price = fields.Integer(string="Best Offer",compute="_best_offer")
    buyer = fields.Many2one('res.partner', string='Buyer',copy=False, index=True)
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    
    """
    ****************************************************
    SQL Constrains
    ****************************************************
    """        
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The Expected Price should be over 0.')
    ]
    
    """
    ****************************************************
    Python Constrains
    ****************************************************
    """
    # Add a constraint so that the selling price cannot be lower than 90% of the expected price.
    # Tip: the selling price is zero until an offer is validated. 
    # You will need to fine tune your check to take this into account.
   
    """
    ****************************************************
    @api Methods
    ****************************************************
    """ 
    @api.depends("living_area","garden_area")
    def _total_area_compute(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.status")
    def _selling_price_compute(self):
        self.selling_price = 0
        min_offer = 0
        for record in self:
            for offer in record.offer_ids:
                if offer.status == "Accepted":
                    min_offer = record.expected_price * 0.9
                    if float_u.float_compare(min_offer,offer.price,2) < 0:
                        record.selling_price = offer.price
                    else:
                        raise ValidationError("The selling price must be over the 90% of expected price.")
                    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = None
    
    """
    ****************************************************
    Methods
    ****************************************************
    """
    def _best_offer(self):
        if self.offer_ids:
            self.best_price = max(self.offer_ids.mapped("price"))
        else:
            self.best_price = 0
            
    def sold_action(self):
        for record in self:
            if record.state != "Canceled" and record.state != "Sold": 
                record.state = "Sold"
            else:
                raise exceptions.ValidationError("You cannot sell a canceled or sold property.")
        
        return True
            
    def cancel_action(self):
        for record in self:
            if record.state != "Sold" and record.state != "Canceled": 
                record.state = "Canceled"
            else:
                raise exceptions.ValidationError("You cannot cancel a canceled or sold property.")
            
        return True 
    

        
   
