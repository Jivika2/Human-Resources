from odoo import models, fields, api

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    change_request_ids = fields.One2many('hr.employee.change', 'employee_id', string='Change Requests')
    total_change_requests = fields.Integer(string='Total Change Requests', compute='_compute_total_change_requests')
    assigned_projects = fields.Many2many('project.project', string='Assigned Projects')
    work_location = fields.Char(string='Work Location')

    @api.depends('change_request_ids')
    def _compute_total_change_requests(self):
        for employee in self:
            employee.total_change_requests = len(employee.change_request_ids)

    def action_submit_change_request(self):
        for employee in self:
            change_request = self.env['hr.employee.change'].create({
                'employee_id': employee.id,
                'job_title': self.env.context.get('job_title', employee.job_title),
                'work_phone': self.env.context.get('work_phone', employee.work_phone),
                'work_email': self.env.context.get('work_email', employee.work_email),
                'reason': self.env.context.get('reason', ''),
            })
            employee.message_post(body='Change request submitted for approval.')

    def action_employee_change(self):
        self.ensure_one()  # Ensure the method works on a single record
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Change Requests",
            'domain': [('employee_id', '=', self.id)],
            'view_mode': 'tree,form',
            'res_model': 'hr.employee.change',
            'target': 'current',  # Use 'new' if you want it in a new window
        }
