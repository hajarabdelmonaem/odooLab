from odoo import models, fields
from odoo import api
import re
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatient(models.Model):
    _name = "hms.patient"
    _rec_name = "fname"
    fname = fields.Char("First Name", required=True)
    lname = fields.Char("Last Name", required=True)
    birth_date = fields.Date("Birth Date")
    history = fields.Html("History")
    cr_ratio = fields.Float("Cr Ratio")
    patient_email = fields.Char("Email")
    blood_type = fields.Selection([
        ('A', "A"),
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('B-', 'B-'),
    ])
    state = fields.Selection([
        ("Undetermined", "Undetermined"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Serious", "Serious")
    ], default="Undetermined")
    pcr = fields.Boolean(default=False)
    image = fields.Binary(string="image")
    address = fields.Char("Address")
    # age = fields.Integer("Age")
    age = fields.Integer(compute='_compute_age', string="Patient Age")
    dept_id = fields.Many2one(comodel_name="hms.department")
    doctors_id = fields.Many2many(comodel_name="hms.doctor")
    logs_id = fields.One2many(comodel_name="hms.logs",inverse_name="patient_id")
    is_dept_selected = fields.Boolean(default=False)
    myflag = fields.Boolean(default=False)


    _sql_constraints = [
        ("Unique Email", "UNIQUE(patient_email)", "Sorry This Email Already Exist...")
    ]


    @api.constrains("patient_email")
    def validate_mail(self):
        if self.patient_email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                             self.patient_email)
        if match == None:
            raise ValidationError('Not a valid E-mail ID')


    @api.depends("birth_date")
    def _compute_age(self):
        for record in self:
            today = date.today()
            if record.birth_date:
                record.age = int(int(today.year) - int(record.birth_date.year))

    @api.multi
    def change_status(self):
        current_status = self.state
        new_state = ""
        if self.state == "Undetermined":
            self.state = "Good"
            new_state = "Good"
        elif self.state == "Good":
            self.state = "Fair"
            new_state = "Fair"
        elif self.state == "Fair":
            self.state = "Serious"
            new_state = "Serious"
        else:
            self.state = "Undetermined"
            new_state = "Undetermined"

        result = self.env['hms.logs'].create(
            {'description': "Changed State from " + current_status + "To " + new_state})
        return result

    @api.onchange('dept_id')
    def select_dept(self):
        if (self.myflag):
            self.is_dept_selected = True
        self.myflag = True

    # Makes pcr Checked if age < 30
    @api.onchange('age')
    def _onchange_age(self):
        if (self.age < 30 and self.age != 0):
            self.pcr = True
            return ({
                'warning': {'title': 'Note', 'message': 'Note That PCR IS Checked Now !!'}
            })