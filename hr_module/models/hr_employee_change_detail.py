
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class EmployeeChangeDetail(models.Model):
    _name = 'hr.employee.change.detail'
    _description = 'Employee Change Detail'

    change_id = fields.Many2one('hr.employee.change', string='Change Request', required=True)
    field_name = fields.Char(string='Field Name', required=True)
    old_value = fields.Char(string='Old Value')
    new_value = fields.Char(string='New Value')
