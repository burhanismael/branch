from odoo import models, fields, api, _


class InheritedAccountAccount(models.Model):
    _inherit = 'account.account'

    branch_id = fields.Many2one('res.branch', default=lambda self: self.env.user.branch_id.id)

