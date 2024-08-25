from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class EmployeeChange(models.Model):
    _name = 'hr.employee.change'
    _description = 'Employee Change Request'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    name = fields.Char(related='employee_id.name', string='Employee Name', store=True)
    job_title = fields.Char(string='Proposed Job Title')
    work_phone = fields.Char(string='Proposed Work Phone')
    work_email = fields.Char(string='Proposed Work Email')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('implemented', 'Implemented')
    ], default='draft', string='Status', readonly=True)
    reason = fields.Text(string='Reason for Change')
    request_date = fields.Date(string='Request Date', default=fields.Date.today, readonly=True)
    implementation_date = fields.Date(string='Implementation Date')
    is_urgent = fields.Boolean(string='Urgent', default=False)
    changes_summary = fields.Text(string="Changes Summary", compute='_compute_changes_summary')
    admin_comment = fields.Text(string='Admin Comment')
    change_detail_ids = fields.One2many('hr.employee.change.detail', 'change_id', string='Change Details')
    approver_ids = fields.Many2many('res.users', string='Approvers')
    related_document = fields.Reference(selection=[
        ('project.project', 'Project'),
        ('project.task', 'Task'),
        ('hr.employee', 'Employee'),
    ], string='Related Document')

    @api.depends('job_title', 'work_phone', 'work_email')
    def _compute_changes_summary(self):
        for rec in self:
            summary = []
            if rec.job_title:
                summary.append(f"Job Title: {rec.job_title}")
            if rec.work_phone:
                summary.append(f"Work Phone: {rec.work_phone}")
            if rec.work_email:
                summary.append(f"Work Email: {rec.work_email}")
            rec.changes_summary = ', '.join(summary) if summary else 'No changes specified.'

    @api.model
    def create(self, vals):
        result = super(EmployeeChange, self).create(vals)
        
        # Attempt to find the email template
        template = self.env.ref('hr_employee_change.email_template_employee_change_submitted', raise_if_not_found=False)
        
        if template:
            template.send_mail(result.id)
        else:
            # Log a message if the template is not found
            _logger.warning("Email template for 'Employee Change Request Submitted' not found.")
        
        return result

    def action_submit(self):
        self.write({'state': 'submitted'})
        self.employee_id.message_post(body='Change request submitted for approval.')
        template = self.env.ref('hr_employee_change.email_template_admin_notification', raise_if_not_found=False)
        if template:
            template.send_mail(self.id)
        else:
            _logger.warning("Email template for 'Admin Notification for Employee Change Request' not found.")

    def action_approve(self):
        for change in self:
            if change.job_title:
                change.employee_id.job_title = change.job_title
            if change.work_phone:
                change.employee_id.work_phone = change.work_phone
            if change.work_email:
                change.employee_id.work_email = change.work_email
            change.employee_id.message_post(body=f"Change request approved for {change.name}.")
        self.write({'state': 'approved'})
        template = self.env.ref('hr_employee_change.email_template_employee_approved', raise_if_not_found=False)
        if template:
            template.send_mail(self.id)
        else:
            _logger.warning("Email template for 'Employee Change Request Approved' not found.")

    def action_implement(self):
        for change in self:
            if change.state != 'approved':
                raise ValidationError("Only approved changes can be implemented.")
            change.write({'state': 'implemented', 'implementation_date': fields.Date.today()})
            change.employee_id.message_post(body=f"Changes implemented for {change.name}.")
            template = self.env.ref('hr_employee_change.email_template_employee_implemented', raise_if_not_found=False)
            if template:
                template.send_mail(self.id)
            else:
                _logger.warning("Email template for 'Employee Change Request Implemented' not found.")

    def action_reject(self):
        for change in self:
            change.employee_id.message_post(body=f"Change request rejected for {change.name}.")
        self.write({'state': 'rejected'})
        template = self.env.ref('hr_employee_change.email_template_employee_rejected', raise_if_not_found=False)
        if template:
            template.send_mail(self.id)
        else:
            _logger.warning("Email template for 'Employee Change Request Rejected' not found.")

    def action_draft(self):
        self.write({'state': 'draft'})
