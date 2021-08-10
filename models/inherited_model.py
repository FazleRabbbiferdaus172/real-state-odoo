from odoo import fields, models

class Users(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="seller_id", domain=[('active', '=', True)])