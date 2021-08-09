from odoo import fields,models,api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _order = "sequence,name"

    name = fields.Char('Type',required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property type house.Higher the better")
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(string="Offer Count",compute="_compute_offer_count")
    _sql_constraints = [('type_unique', 'unique(name)', 'Type already exists.')]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped('id'))



    