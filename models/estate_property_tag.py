from odoo import fields,models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _order = "name"

    name = fields.Char('Tag', required=True)
    color = fields.Integer()

    _sql_constraints = [('tag_unique', 'unique(name)', 'Tag already exists.')]