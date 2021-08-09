from odoo import fields,models

class PropertyType(models.Model):
    _name = "estate.property.type"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")

    _sql_constraints = [('type_unique', 'unique(name)', 'Type already exists.')]
    