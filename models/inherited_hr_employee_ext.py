from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrEmployeeExt(models.Model):
    _inherit = 'hr.employee'

    branch_id = fields.Many2one('res.branch', string='Branch', default=lambda self: self.env.user.branch_id.id)
