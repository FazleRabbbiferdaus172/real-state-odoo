# -*- coding: utf-8 -*-
from odoo import fields,models,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_compare,float_is_zero

class Property(models.Model):
    _name = "estate.property"
    _description = "Property Model"
    _order = "id desc"

    
    name = fields.Char('Title',required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', default=lambda self: fields.Date.from_string(fields.Date.today()) + relativedelta(months=+3) ,copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area(sqm)')
    facades = fields.Integer('facades')
    garage = fields.Boolean('Garage?')
    garden = fields.Boolean('Garden?')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'),('east','East'),('west','West'),('south','South')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        required=True,
        copy=False,
        default='new',
        selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')]
    )

    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(comodel_name="res.users", default=lambda self: self.env.user,string="Salesman")
    property_tag_id = fields.Many2many(comodel_name="estate.property.tag", string="Tag")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")
    total_area = fields.Integer(string='Total Area', compute="_compute_total_area")
    best_price = fields.Float('Best offer', compute="_compute_best_price")


    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Expected price must be positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'Selling price must be positive'),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids.mapped('price') else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        self.ensure_one()
        if self.state != 'canceled':
            self.state = 'sold'
        elif self.state == 'canceled':
            raise UserError('Canceled property can not be sold')
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state != 'sold':
            self.state = 'canceled'
        elif self.state == 'sold':
            raise UserError('Sold property can not be canceled')
        return True


    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price,2) and float_compare(record.selling_price,record.expected_price * .9,2) == -1:
                raise ValidationError('Selling price can not be less than 90% of expected price.')


    @api.onchange("selling_price")
    def _onchange_selling_price(self):
        self._check_selling_price()

    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        self._check_selling_price()