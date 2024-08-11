from odoo import api, fields, models, _
from datetime import timedelta

from odoo.exceptions import ValidationError # type: ignore


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string="Description", compute='_compute_name')
    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status"
    )
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity (days)")  # Default validity period, adjust as needed
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
    creation_date = fields.Date(string="Create Date", default=fields.Date.today)  # Use today’s date as default

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False  # Explicitly set to False if no creation_date or validity

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    # Example of a model cleaning method that deletes refused offers.
    """ @api.model
    def _clean_offers(self):
        refused_offers = self.search([('status', '=', 'refused')])
        refused_offers.unlink() """

    # Uncomment and adjust the following method for batch creation if needed
    
    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)
    
    def action_accept_offer(self):
        self.status = 'accepted'

    def action_decline_offer(self):
        self.status = 'refused'

    """ @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError(_("Deadline cannot be before creation date"))
             """
   


    """ def write(self, vals):
        print(vals)
        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
            #('name', '=', vals.get('name')),
        ], limit=1, order='name desc')
        print(res_partner_ids)
        return super(PropertyOffer, self).write(vals) """
    
    """ def write(self, vals):
        print(vals)
        res_partner_ids = self.env['res.partner'].browse([10,14])
        print(res_partner_ids.name)
        return super(PropertyOffer, self).write(vals) """
    
    """ def write(self, vals):
        print(self)
        print(self.env.cr)
        print(self.env.uid)
        print(self.env.context)
        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
            #('name', '=', vals.get('name')),
        ]).filtered(lambda x: x.phone == '(870)-931-0505') #mapped('phone')
        print(res_partner_ids)
        return super(PropertyOffer, self).write(vals)
     """
    
