from odoo import models, fields
from odoo import api
from odoo.exceptions import ValidationError, UserError


class HospitalCustomer(models.Model):
    _inherit = "res.partner"
    related_patient_id = fields.Many2one(comodel_name="hms.patient")

    @api.constrains("email")
    def validate_customer_patient_email(self):
        print(print(self.env['hms.patient'].search([("patient_email", "=", self.email)], limit=1)))
        if len(self.env['hms.patient'].search([("patient_email", "=", self.email)], limit=1)) != 0:
            raise ValidationError('The email already exist')


    @api.multi
    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError("You can't delete this customer")

        super().unlink()