# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMove, self).default_get(default_fields)
        branch_id = False

        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'branch_id' : branch_id
        })
        return res

    branch_id = fields.Many2one('res.branch', string="Branch")

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        selected_brach = self.branch_id
        if selected_brach:
            user_id = self.env['res.users'].browse(self.env.uid)
            user_branch = user_id.sudo().branch_id
            if user_branch and user_branch.id != selected_brach.id:
                raise UserError("Please select active branch only. Other may create the Multi branch issue. \n\ne.g: If you wish to add other branch then Switch branch from the header and set that.")

############custom codee
    @api.model
    def create(self, vals):
        """Overridden create method to update the lines."""
        #print("vals-------AccountMove-------",vals,self.env.context,self.env.context.get('active_model'))
        if self.env.context.get('active_model') == "stock.quant":
            brch_id = False
            #print("self.env.context.get('active_id') ====",self.env.context.get('active_id'))
            stock_quant_rec = self.env['stock.quant'].browse(self.env.context.get('active_id'))
            if vals.get("stock_move_id",False):
                stock_move_rec = self.env['stock.move'].browse(vals.get("stock_move_id"))
                brch_id = stock_move_rec.location_dest_id.branch_id.id
            if not brch_id:
                product_rec = self.env['product.product'].browse(vals.get("product_id"))
                if product_rec.branch_id:
                    brch_id = product_rec.branch_id.id
                else:
                    raise UserError("Branch is missing!!")

            #print("stock_quant_rec ------------------",stock_quant_rec,stock_quant_rec.branch_id)
            #print("brch_id==============",brch_id)
            if brch_id:
                vals.update({"branch_id":brch_id})
        if self.env.context.get('active_model') == "account.move" and not vals.get("branch_id",False):
            #print("branch_miss",self.env.context.get('active_id'))
            # if self.env.context.get('active_ids') and len(self.env.context.get('active_ids'))>1:
            #     raise UserError("Process individual records!!")

            if self.env.context.get('active_id'):
                move_rec = self.env['account.move'].browse(self.env.context.get('active_id'))
                vals.update({"branch_id":move_rec.branch_id.id})

            


        new_move = super(AccountMove, self).create(vals)
        if new_move and new_move.branch_id:
            if new_move.line_ids:
                new_move.line_ids.write(
                    {"branch_id": new_move.branch_id and new_move.branch_id.id or False}
                )
            if new_move.invoice_line_ids:
                new_move.invoice_line_ids.write(
                    {"branch_id": new_move.branch_id and new_move.branch_id.id or False}
                )
        return new_move

    # def write(self, vals):
    #     """Overridden write method to update the lines."""
    #     res = super(AccountMove, self).write(vals)
    #     if vals.get("branch_id", False):
    #         for inv in self:
    #             if inv and inv.branch_id:
    #                 if inv.line_ids:
    #                     inv.line_ids.write(
    #                         {"branch_id": inv.branch_id and inv.branch_id.id or False}
    #                     )
    #                 if inv.invoice_line_ids:
    #                     inv.invoice_line_ids.write(
    #                         {"branch_id": inv.branch_id and inv.branch_id.id or False}
    #                     )
    #     return res 
#############ends here

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMoveLine, self).default_get(default_fields)
        branch_id = False

        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id

        if self.move_id.branch_id :
            branch_id = self.move_id.branch_id.id
        res.update({'branch_id' : branch_id})
        return res

    branch_id = fields.Many2one('res.branch', string="Branch",related="move_id.branch_id",store=True)



class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountJournal, self).default_get(default_fields)
        branch_id = False

        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'branch_id' : branch_id
        })
        return res

    branch_id = fields.Many2one('res.branch', string="Branch")
