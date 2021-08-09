from odoo import fields,models,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(string="Status", selection=[('accepted','Accepted'),('refused','Refused')], copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('check_eprice', 'CHECK(price > 0)',
         'Offer price must be positive'),
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.from_string(record.create_date) + relativedelta(days=+record.validity)
            else:
                record.date_deadline = fields.Date.from_string(fields.Date.today()) + relativedelta(days=+record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = int((fields.Date.from_string(record.date_deadline) - fields.Date.from_string(record.create_date)).days)
            else:
                record.validity = int((fields.Date.from_string(record.date_deadline) - fields.Date.from_string(fields.Date.today())).days)


    def action_confirm(self):
        self.ensure_one()
        if self.property_id.buyer_id:
            raise UserError('Can not accept more than 1 offer')
            return True
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_cancel(self):
        self.ensure_one()
        self.status = 'refused'
        return True
