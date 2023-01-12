# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

   

    @api.model
    def default_get(self,fields):
        res = super(SaleOrder, self).default_get(fields)
        branch_id = warehouse_id = False
        if self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        #print("defaultget branch_id --------1--",branch_id)
        if branch_id:
            branched_warehouse = self.env['stock.warehouse'].search([('branch_id','=',branch_id)])
            #print("defaultget branched_warehouse ----------",branched_warehouse)
            if branched_warehouse:
                warehouse_id = branched_warehouse.ids[0]
        else:
            warehouse_id = self._default_warehouse_id()
            warehouse_id = warehouse_id.id

        res.update({
            'branch_id' : branch_id,
            'warehouse_id' : warehouse_id
            })

        return res

    branch_id = fields.Many2one('res.branch', string="Branch")

    
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['branch_id'] = self.branch_id.id
        return res


    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        selected_brach = self.branch_id
        res = {}
        if selected_brach:

            branched_warehouse = self.env['stock.warehouse'].search([('branch_id','=',selected_brach.id)])
            #print("defaultget branched_warehouse ----------",branched_warehouse)
            if branched_warehouse:
                warehouse_id = branched_warehouse.ids[0]
                self.warehouse_id = warehouse_id
                #res.update({'warehouse_id': warehouse_id})

            user_id = self.env['res.users'].browse(self.env.uid)
            user_branch = user_id.sudo().branch_id
            if user_branch and user_branch.id != selected_brach.id:
                raise UserError("Please select active branch only. Other may create the Multi branch issue. \n\ne.g: If you wish to add other branch then Switch branch from the header and set that.")

            return res

