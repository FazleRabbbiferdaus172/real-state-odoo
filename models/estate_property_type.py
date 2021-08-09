from odoo import fields,models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _order = "sequence,name"

    name = fields.Char('Type',required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property type house.Higher the better")

    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")

    _sql_constraints = [('type_unique', 'unique(name)', 'Type already exists.')]
    