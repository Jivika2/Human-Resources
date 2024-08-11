from odoo import models, fields, api


class Property(models.Model):
    _name = 'estate.property'
    _description = "Real state properties"


    name = fields.Char(string="Name" , required=True)
    state = fields.Selection([('new', 'New'), ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'), ('sold', 'Sold'),('cancel','Cancelled')],
          default='new', string="State")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string= " Postcode")
    date_availability = fields.Date(string="Available Form", readonly=True)
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price")
    best_offer = fields.Float(string="Best Offer")
    beadrooms = fields.Integer(string="Beadrooms")
    living_area = fields.Integer(string="Living Area(sqqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Total Area(sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orintation", default='north')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    total_area = fields.Integer(string="Total Area", compute='_compute_total_area')
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    def action_accept(self):
        self.state='sold'

    def action_refused(self):
        self.state='cancel'
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')

    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.offer'
        }

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area



class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Types'

    name = fields.Char(string="Name", required=True)




class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tags"


    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")