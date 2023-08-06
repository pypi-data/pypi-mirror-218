from odoo import models, api, fields

class MailTemplateCategory(models.Model):

    _name = 'mail.template.category'
    _inherit='res.partner.category'
    _order = 'name'
    _parent_store = True
