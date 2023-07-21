from odoo import api, fields, models, _

class PosConfigExt(models.Model):
    _inherit = 'pos.config'

    branch_id = fields.Many2one('res.branch', string='Branch', default=lambda self: self.env.user.branch_id.id)
