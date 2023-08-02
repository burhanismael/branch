# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
import antigravity


class ResUsers(models.Model):
    _inherit = 'res.users'

    branch_ids = fields.Many2many('res.branch', relation='user_branch_ids_rel', column1='user_id', column2='branch_id',string="Allowed Branches")
    branch_id = fields.Many2one('res.branch', string= 'Branch')
    branches_ids = fields.Many2many('res.branch', relation='user_branches_rel', column1='user_id', column2='branch_id')
    # @api.onchange('branch_id')
    # def _onchange_active_branch(self):
    #     for rec in self:
    #         rec.branches_ids = [int(item) for item in request.httprequest.cookies['bids'].split(',')]
    def write(self, values):
        if 'branch_id' in values or 'branch_ids' in values:
            self.env['ir.model.access'].call_cache_clearing_methods()
            self.branches_ids = [int(item) if type(item)==int else False for item in request.httprequest.cookies['bids'].split(',')]
        user = super(ResUsers, self).write(values)
        return user



